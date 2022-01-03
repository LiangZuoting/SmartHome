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

DEBUG = True

if DEBUG:
	from sanic.log import logger
else:
	import logging
	from logging.config import dictConfig
	from logging.handlers import RotatingFileHandler

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


app = Sanic(__name__)
info('sanic started...')
app.static('/static', './static')
app.static('/manifest.json', './manifest.json')
app.static('/favicon.ico', './favicon.ico')
app.static('/logo192.png', './logo192.png')
app.static('/logo512.png', './logo512.png')
app.static('/images', './images')
sched = BackgroundScheduler()


def reconnect_miot_device(ip):
	for dev in dev_model['devices']:
		if dev['ip'] == ip:
			try:
				info(f'reconnecting miot device ${dev["name"]}')
				miot_devs[ip] = MiotDevice(ip, dev['token'], lazy_discover=False)
			except DeviceException as e:
				error(f'${format(e)} ${dev["name"]}')
				return None
			return miot_devs[ip]
	return None


def set_miot_property(ip, siid, piid, value, retry=0):
	try:
		miot_devs[ip].set_property_by(siid, piid, value)
	except DeviceException as e:
		error(f'${format(e)} try_times=${retry}')
		if retry > 2:
			return
		dev = reconnect_miot_device(ip)
		if dev is not None:
			set_miot_property(ip, siid, piid, value, retry + 1)


def get_miot_property(ip, siid, piid, retry=0):
	try:
		ret = miot_devs[ip].get_property_by(siid, piid)
	except DeviceException as e:
		error(f'${format(e)}')
		if retry > 2:
			return None
		dev = reconnect_miot_device(ip)
		if dev is not None:
			return get_miot_property(ip, siid, piid, retry + 1)
	return ret


def reconnect_midea_device(ip):
	for dev in dev_model:
		if dev['ip'] == ip:
			info(f'reconnecting midea device ${dev["name"]}')
			ac = MideaAC(ip, int(dev['id']), dev['port'])
			midea_acs[ip] = ac
			ret = ac.authenticate(dev['key'], dev['token'])
			if not ret:
				error(f'authenticate midea error ${ip}')
				return ret, None
			return ret, ac
	return False, None


def apply_midea(ip, try_times=0):
	ac = midea_acs[ip]
	ac.apply()
	if not ac.active:
		error(f'apply midea error ${ip}')
		if try_times > 2:
			return
		reconnect_midea_device(ip)
		apply_midea(ip, try_times+1)


def refresh_midea(ip, try_times=0):
	ac = midea_acs[ip]
	ac.refresh()
	if not ac.active:
		error(f'refresh midea error ${ip}')
		if try_times > 2:
			return
		reconnect_midea_device(ip)
		refresh_midea(ip, try_times+1)


def scheduler_job(ip, protocol, properties):
	if protocol == 'miot':
		for p in properties:
			set_miot_property(ip, p['siid'], p['piid'], p['value'])
	elif protocol == 'midea':
		for p in properties:
			# convert int values of json file to its orginal type in msmart,
			# with getattr we can know type msmart wanted.
			# e.g. fan_speed whose getter returns fan_speed_enum and setter accepts fan_speed_enum only.
			setattr(midea_acs[ip], p['id'], type(getattr(midea_acs[ip], p['id']))(p['value']))
		apply_midea(ip)


# connecting to devices when boot
dev_model = ujson.loads(open(os.path.join('./model', 'devices.json')).read())
# map from ip to device object
miot_devs = {}
midea_acs = {}
for dev in dev_model['devices']:
	protocol = dev['protocol']
	if protocol == 'miot':
		try:
			miot_devs[dev['ip']] = MiotDevice(dev['ip'], dev['token'], lazy_discover=False)
		except DeviceException as e:
			error(f'${format(e)} ${dev["name"]}')
	elif protocol == 'midea':
		ac = MideaAC(dev['ip'], int(dev['id']), dev['port'])
		midea_acs[dev['ip']] = ac
		ac.authenticate(dev['key'], dev['token'])
	else:
		continue
	if 'timers' in dev:
		for t in dev['timers']:
			sched.add_job(scheduler_job, args=(dev['ip'], dev['protocol'], t['properties']), **t['trigger_args'])
			

# start scheduler
sched.start()


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
					sched.add_job(scheduler_job, args=(ip, data['protocol'], [data]), trigger='interval', minutes=2, id=ip)
		else:
			set_miot_property(ip, data['siid'], data['piid'], data['value'])
	elif ip in midea_acs:
		dev = midea_acs[ip]
		setattr(dev, data['id'], type(getattr(dev, data['id']))(data['value']))
		apply_midea(ip)
	return json(updateAllDevices())
		

@app.get('/model/init')
async def init(request):
	return json(updateAllDevices())


def updateAllDevices():
	try:
		for dev in dev_model['devices']:
			info(f'retrieving ${dev["ip"]} ...')
			if dev['ip'] in miot_devs:
				for prop in dev['properties']:
					ret = get_miot_property(dev['ip'], prop['siid'], prop['piid']) # ret is a json array
					if not ret:
						error(f'skip device ${dev["name"]} for exception')
						break
					prop['value'] = ret[0]['value']
			elif dev['ip'] in midea_acs:
				refresh_midea(dev['ip'])
				for prop in dev['properties']:
					v = getattr(midea_acs[dev['ip']], prop['id'])
					if isinstance(v, Enum):
						v = v.value
					prop['value'] = v
		info(f'init: {dev_model}')
	except DeviceException as e:
		error(format(e))
	return dev_model


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9876)