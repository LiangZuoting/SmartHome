#!usr/bin/env python3
import os
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


def scheduler_job(ip, protocol, properties):
	if protocol == 'miot':
		for p in properties:
			miot_devs[ip].set_property_by(p['siid'], p['piid'], p['value'])
	elif protocol == 'midea':
		for p in properties:
			setattr(midea_acs[ip], p['id'], p['value'])
		midea_acs[ip].apply()


# connecting to devices when boot
dev_model = ujson.loads(open(os.path.join('./model', 'devices.json')).read())
# map from ip to device object
miot_devs = {}
midea_acs = {}
for dev in dev_model['devices']:
	protocol = dev['protocol']
	if protocol == 'miot':
		miot_devs[dev['ip']] = MiotDevice(dev['ip'], dev['token'], lazy_discover=False)
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
		dev = miot_devs[ip]
		# post from ipc
		# it should only be SWITCH property posted.
		if 'from' in data and data['from'] == 'monitor':
			status = dev.get_property_by(data['siid'], data['piid'])[0]['value']
			if data['value']:
				if sched.get_job(ip):
					sched.remove_job(ip)
				if not status:
					dev.set_property_by(data['siid'], data['piid'], data['value'])
			else:
				if not sched.get_job(ip) and status:
					# when nobody, closing it 2 minutes later
					sched.add_job(scheduler_job, args=(ip, data['protocol'], [data]), trigger='interval', minutes=2, id=ip)
		else:
			dev.set_property_by(data['siid'], data['piid'], data['value'])
	elif ip in midea_acs:
		dev = midea_acs[ip]
		setattr(dev, data['id'], data['value'])
		dev.apply()
	return json(updateAllDevices())
		

@app.get('/model/init')
async def init(request):
	return json(updateAllDevices())


def updateAllDevices():
	try:
		for dev in dev_model['devices']:
			if dev['ip'] in miot_devs:
				for prop in dev['properties']:
					ret = miot_devs[dev['ip']].get_property_by(prop['siid'], prop['piid']) # ret is a json array
					prop['value'] = ret[0]['value']
			elif dev['ip'] in midea_acs:
				midea_acs[dev['ip']].refresh()
				for prop in dev['properties']:
					getattr(midea_acs[dev['ip']], prop['id'])
		info(f'init: {dev_model}')
	except DeviceException as error:
		error(format(error))
	return dev_model


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9876)