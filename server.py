#!usr/bin/env python3
import os
from enum import Enum
from miio import MiotDevice, DeviceException
from apscheduler.schedulers.background import BackgroundScheduler
from sanic import Sanic
from sanic.response import json
from sanic.response import file
import ujson
from msmart.device import air_conditioning_device as MideaAC

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
    if protocol == 'miot':
        if ip not in miot_devs:
            if not connect_miot_device(ip):
                error('cannot connect device, skip timer')
                return
            for p in properties:
                set_miot_property(ip, p['siid'], p['piid'], p['value'])
    elif protocol == 'midea':
        if ip not in midea_acs:
            ret, conn = connect_midea_device(ip)
            if not ret:
                error('cannot connect device, skip timer')
        for p in properties:
            # convert int values of json file to its orginal type in msmart,
            # with getattr we can know type msmart wanted.
            # e.g. fan_speed whose getter returns fan_speed_enum and setter accepts fan_speed_enum only.
            setattr(midea_acs[ip], p['id'], type(getattr(midea_acs[ip], p['id']))(p['value']))
        apply_midea(ip)


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
            dev_model[d['ip']] = d
            if 'timers' in d:
                for t in d['timers']:
                    sched.add_job(scheduler_job, args=(d['ip'], d['protocol'], t['properties']),
                                  **t['trigger_args'])


# start scheduler
sched.start()


def connect_miot_device(ip):
    if ip in miot_devs:
        miot_devs.pop(ip)
    d = dev_model[ip]
    try:
        info(f'connecting miot device {d["name"]}')
        miot_devs[ip] = MiotDevice(ip, d['token'], lazy_discover=False)
        d['error'] = None
    except DeviceException as e:
        error(f'{format(e)} {d["name"]}')
        d['error'] = f'cannot connect this device'
        return None
    return miot_devs[ip]


def set_miot_property(ip, siid, piid, value, retry=0):
    try:
        miot_devs[ip].set_property_by(siid, piid, value)
        dev_model[ip]['error'] = None
    except DeviceException as e:
        error(f'{format(e)} try_times={retry}')
        dev_model[ip]['error'] = 'set property error'
        if retry > 2:
            return
        if connect_miot_device(ip) is not None:
            set_miot_property(ip, siid, piid, value, retry + 1)


def get_miot_property(ip, siid, piid, retry=0):
    try:
        ret = miot_devs[ip].get_property_by(siid, piid)
        dev_model[ip]['error'] = None
    except DeviceException as e:
        error(f'{format(e)}')
        dev_model[ip]['error'] = 'get property error'
        if retry > 2:
            return None
        if connect_miot_device(ip) is not None:
            return get_miot_property(ip, siid, piid, retry + 1)
    return ret


def connect_midea_device(ip):
    if ip in midea_acs:
        midea_acs.pop(ip)
    d = dev_model[ip]
    info(f'connecting midea device {d["name"]}')
    ac = MideaAC(ip, int(d['id']), d['port'])
    ret = ac.authenticate(d['key'], d['token'])
    if not ret:
        error(f'authenticate midea error {ip}')
        d['error'] = 'authenticate device failed'
        return ret, None
    d['error'] = None
    midea_acs[ip] = ac
    return ret, ac


def apply_midea(ip, try_times=0):
    ac = midea_acs[ip]
    ac.apply()
    if not ac.active:
        error(f'apply midea error {ip}')
        dev_model[ip]['error'] = 'apply error'
        if try_times > 2:
            return
        connect_midea_device(ip)
        apply_midea(ip, try_times + 1)
    else:
        dev_model[ip]['error'] = None


def refresh_midea(ip, try_times=0):
    ac = midea_acs[ip]
    ac.refresh()
    if not ac.active:
        error(f'refresh midea error {ip}')
        dev_model[ip]['error'] = 'refresh error'
        if try_times > 2:
            return
        connect_midea_device(ip)
        refresh_midea(ip, try_times + 1)
    else:
        dev_model[ip]['error'] = None


@app.get('/')
async def index(request):
    return await file('./templates/index.html', mime_type='text/html')


@app.post('/')
async def update(request):
    data = request.json
    ip = data['ip']
    if ip in miot_devs:
        # post from ipc
        # it should only be SWITCH property posted.
        if 'from' in data and data['from'] == 'monitor':
            ret = get_miot_property(ip, data['siid'], data['piid'])
            if not ret:
                error(f'update cannot be executed for exception')
                dev_model[ip]['error'] = 'get property error'
                return
            status = ret[0]['value']
            if data['value']:
                if sched.get_job(ip):
                    sched.remove_job(ip)
                if not status:
                    set_miot_property(ip, data['siid'], data['piid'], data['value'])
            else:
                if not sched.get_job(ip) and status:
                    # when nobody, closing it 2 minutes later
                    sched.add_job(scheduler_job, args=(ip, data['protocol'], [data]), trigger='interval', minutes=2,
                                  id=ip)
        else:
            set_miot_property(ip, data['siid'], data['piid'], data['value'])
    elif ip in midea_acs:
        d = midea_acs[ip]
        setattr(d, data['id'], type(getattr(d, data['id']))(data['value']))
        apply_midea(ip)
    return json(refresh_device(ip))


@app.get('/devices')
async def get_devices(request):
    return json(dev_model)


@app.get('/device/<ip:path>')  # ip address is a path but not a str
async def get_device(request, ip: str):
    return json(refresh_device(ip))


def refresh_device(ip):
    d = refresh_connected_device(ip)
    if d is not None:
        return d
    d = dev_model[ip]
    protocol = d['protocol']
    if protocol == 'miot':
        if not connect_miot_device(ip):
            return d
        return refresh_connected_device(ip)
    elif protocol == 'midea':
        ret, conn = connect_midea_device(ip)
        if not ret:
            return d
        return refresh_connected_device(ip)
    return d


def refresh_connected_device(ip):
    d = dev_model[ip]
    if ip in miot_devs:
        for prop in d['properties']:
            ret = get_miot_property(ip, prop['siid'], prop['piid'])
            if not ret:
                error(f'cannot get property of device {d["name"]}')
            else:
                prop['value'] = ret[0]['value']
        return d
    if ip in midea_acs:
        refresh_midea(ip)
        for prop in d['properties']:
            v = getattr(midea_acs[ip], prop['id'])
            if isinstance(v, Enum):
                v = v.value
            prop['value'] = v
        return d
    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
