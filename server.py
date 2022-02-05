#!usr/bin/env python3
import os
from enum import Enum
from miio import MiotDevice, DeviceException
from apscheduler.schedulers.background import BackgroundScheduler
from sanic import Sanic
from sanic.response import json, file, empty
import ujson
from json import dumps
from msmart.device import air_conditioning_device as MideaAC
from msmart.scanner import MideaDiscovery
from msmart.const import OPEN_MIDEA_APP_ACCOUNT, OPEN_MIDEA_APP_PASSWORD

DEBUG = False

if DEBUG:
    from sanic.log import logger
else:
    import logging
    from logging.config import dictConfig

    if not os.path.exists('logs'):
        os.mkdir('logs')
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/sanic.log',
            'maxBytes': 4096000,
            'backupCount': 10,
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        }
    })


def info(msg):
    if DEBUG:
        logger.info(msg)
    else:
        logging.info(msg)


def error(msg):
    if DEBUG:
        logger.error(msg)
    else:
        logging.error(msg)


def scheduler_job(ip, protocol, properties):
    """
    top level method, called when timer is triggered
    :param ip:
    :param protocol:
    :param properties:
    :return:
    """
    if protocol == 'miot':
        if connect_miot_device(ip):
            for p in properties:
                if not set_miot_property(ip, p['siid'], p['piid'], p['value']):
                    error(f'scheduler_job failed for could not set_miot_property to {ip}')
                    return
            return
    elif protocol == 'midea':
        if connect_midea_device(ip):
            for p in properties:
                # convert int values of json file to its orginal type in msmart,
                # with getattr we can know type msmart wanted.
                # e.g. fan_speed whose getter returns fan_speed_enum and setter accepts fan_speed_enum only.
                set_midea_property(ip, p['id'], type(getattr(midea_acs[ip], p['id']))(p['value']))
            if not apply_midea(ip):
                error(f'scheduler_job failed for could not set_midea_property to {ip}')
                return
            return
    else:
        error(f'scheduler_job failed for unknown protocol {protocol} on {ip}')
        return
    error(f'scheduler_job failed for could not connect to device {ip}')


app = Sanic(__name__)
info('sanic started...')
app.static('/static', './static')
app.static('/manifest.json', './manifest.json')
app.static('/favicon.ico', './favicon.ico')
app.static('/logo192.png', './logo192.png')
app.static('/logo512.png', './logo512.png')
app.static('/images', './images')
sched = BackgroundScheduler()


dev_model = {}  # devices' config, key is ip address
miot_devs = {}  # miot devices' connection, key is ip address
midea_acs = {}  # midea devices' connection, key is ip address
# load all devices config when boot
devices_dir = './model/devices'
for filename in os.listdir(devices_dir):
    device_path = os.path.join(devices_dir, filename)
    if os.path.isfile(device_path) and filename.endswith('.json'):
        with open(device_path) as f:
            d = ujson.loads(f.read())
            d['json_file'] = device_path  # remember devices' config file path to update
            dev_model[d['ip']] = d
            if 'timers' in d:
                for t in d['timers']:
                    sched.add_job(scheduler_job, args=(d['ip'], d['protocol'], t['properties']),
                                  **t['trigger_args'])


# start scheduler
sched.start()


def connect_miot_device(ip, force=False):
    if ip in miot_devs and not force:
        return miot_devs[ip]
    d = dev_model[ip]
    try:
        miot_devs[ip] = MiotDevice(ip, d['token'], lazy_discover=False)
        d['error'] = None
    except DeviceException as e:
        error(f'{format(e)} {d["name"]}')
        d['error'] = f'cannot connect this device'
        return None
    return miot_devs[ip]


def set_miot_property(ip, siid, piid, value):
    """
    call connect_miot_device before this function to make sure device has been connected
    :param ip: 
    :param siid: 
    :param piid: 
    :param value: 
    :return: 
    """
    try:
        miot_devs[ip].set_property_by(siid, piid, value)
        dev_model[ip]['error'] = None
        return True
    except DeviceException as e:
        error(f'{format(e)}')
        if not connect_miot_device(ip, True):
            error(f'set_miot_property failed for could not connect to {ip}')
            return False
        return set_miot_property(ip, siid, piid, value)


def get_miot_property(ip, siid, piid):
    """
    call connect_miot_device before this function to make sure device has been connected
    :param ip: 
    :param siid: 
    :param piid: 
    :return: 
    """
    try:
        ret = miot_devs[ip].get_property_by(siid, piid)
        dev_model[ip]['error'] = None
    except DeviceException as e:
        error(f'{format(e)}')
        if not connect_miot_device(ip, True):
            error(f'get_miot_property failed for could not connect to {ip}')
            return None
        return get_miot_property(ip, siid, piid)
    return ret


def connect_midea_device(ip, force=False):
    if ip in midea_acs and not force:
        return midea_acs[ip]
    d = dev_model[ip]
    ac = MideaAC(ip, int(d['id']), d['port'])
    ret = ac.authenticate(d['key'], d['token'])
    if not ret:
        error(f'authenticate midea error {ip}')
        d['error'] = 'authenticate device failed'
        return None
    d['error'] = None
    midea_acs[ip] = ac
    return ac


def set_midea_property(ip, pid, value):
    setattr(midea_acs[ip], pid, value)


def get_midea_property(ip, pid):
    return getattr(midea_acs[ip], pid)


def apply_midea(ip):
    """
    call connect_midea_device before this function to make sure device has been connected
    :param ip: 
    :return: 
    """
    ac = midea_acs[ip]
    ac.apply()
    if not ac.active:
        error(f'apply midea error {ip}')
        if not connect_midea_device(ip, True):
            error(f'apply_midea failed for could not connect to {ip}')
            return False
        return apply_midea(ip)
    else:
        dev_model[ip]['error'] = None
        return True


def refresh_midea(ip):
    """
    call connect_midea_device before this function to make sure device has been connected
    :param ip: 
    :return: 
    """
    ac = midea_acs[ip]
    ac.refresh()
    if not ac.active:
        error(f'refresh midea error {ip}')
        if not connect_midea_device(ip, True):
            error(f'refresh_midea failed for could not connect to {ip}')
            return False
        return refresh_midea(ip)
    else:
        dev_model[ip]['error'] = None
        return True


@app.get('/')
async def index(request):
    return await file('./templates/index.html', mime_type='text/html')


@app.post('/')
async def update(request):
    """
    update specific device
    :param request:
    :return: return older config if errors occurred, or return latest status of device
    """
    data = request.json
    ip = data['ip']
    protocol = dev_model[ip]['protocol']
    if protocol == 'miot':
        if not connect_miot_device(ip):
            error(f'update returns early for could not connect to {ip}')
            return json(dev_model[ip])
        # post from ipc
        # it should only be SWITCH property posted.
        if 'from' in data and data['from'] == 'monitor':
            if sched.get_job(ip):
                sched.remove_job(ip)
            if data['value']:
                if not set_miot_property(ip, data['siid'], data['piid'], data['value']):
                    error(f'update returns early for could not set_miot_property to {ip}')
                    return json(dev_model[ip])
            else:
                # when nobody, closing it 2 minutes later
                sched.add_job(scheduler_job, args=(ip, data['protocol'], [data]), trigger='interval', minutes=2,
                              id=ip)
        else:
            if not set_miot_property(ip, data['siid'], data['piid'], data['value']):
                error(f'update returns early for could not set_miot_property to {ip}')
                return json(dev_model[ip])
    elif protocol == 'midea':
        if not connect_midea_device(ip):
            error(f'update returns early for could not connect to {ip}')
            return json(dev_model[ip])
        set_midea_property(ip, data['id'], type(getattr(d, data['id']))(data['value']))
        if not apply_midea(ip):
            error(f'update returns early for apply_midea failed on {ip}')
            return json(dev_model[ip])
    return json(refresh_device(ip))


@app.get('/devices')
async def get_devices(request):
    """
    get all devices' last status
    :param request:
    :return:
    """
    return json(dev_model)


@app.get('/device/<ip:path>')  # ip address is a path but not a str
async def get_device(request, ip: str):
    protocol = dev_model[ip]['protocol']
    if protocol == 'miot':
        if not connect_miot_device(ip):
            error(f'get_device returns early for could not connect to {ip}')
            return json(dev_model[ip])
    elif protocol == 'midea':
        if not connect_midea_device(ip):
            error(f'get_device returns early for could not connect to {ip}')
            return json(dev_model[ip])
    return json(refresh_device(ip))


@app.get('/discover/<ip:path>')
async def discover_device(request, ip: str):
    d = dev_model[ip]
    protocol = d['protocol']
    if protocol == 'midea':
        try:
            discovery = MideaDiscovery(account=OPEN_MIDEA_APP_ACCOUNT, password=OPEN_MIDEA_APP_PASSWORD, amount=1)
            found_devices = await discovery.get_all()
        except Exception:
            pass
        else:
            if found_devices:
                for device in found_devices:
                    if device.ip in dev_model:
                        dev_model[ip]['token'] = device.token
                        dev_model[ip]['key'] = device.key
                        with open(dev_model[ip]['json_file'], mode='w') as f:
                            f.write(dumps(dev_model[ip], indent=4))
                return json(refresh_device(ip))
    return json({'desc': 'error'}, status=500)


def refresh_device(ip):
    d = dev_model[ip]
    protocol = d['protocol']
    if protocol == 'miot':
        for prop in d['properties']:
            ret = get_miot_property(ip, prop['siid'], prop['piid'])
            if not ret:
                error(f'refresh_device returns early for cannot get_miot_property on {d["name"]}')
                return d
            prop['value'] = ret[0]['value']
    elif protocol == 'midea':
        for prop in d['properties']:
            ret = get_midea_property(midea_acs[ip], prop['id'])
            if isinstance(ret, Enum):
                ret = ret.value
            prop['value'] = ret
    return d


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
