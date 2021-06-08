#!usr/bin/env python3
import os
import json
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from miio import MiotDevice, DeviceException
from apscheduler.schedulers.background import BackgroundScheduler


if not os.path.exists('logs'):
	os.mkdir('logs')
logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
		'filename': 'logs/fast.log',
		'maxBytes': 4096000,
		'backupCount': 10,
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
logging.info('FastAPI started...')


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")


sched = BackgroundScheduler()


def scheduler_job(ip, protocol, properties):
	if protocol == 'miot':
		for p in properties:
			miot_devs[ip].set_property_by(p['siid'], p['piid'], p['value'])


# connecting to devices when boot
dev_model = json.loads(open(os.path.join('./model', 'devices.json')).read())
# map from ip to device object
miot_devs = {}
for dev in dev_model['devices']:
	if dev['protocol'] == 'miot':
		miot_devs[dev['ip']] = MiotDevice(dev['ip'], dev['token'], lazy_discover=False)
		if 'timers' in dev:
			for t in dev['timers']:
				sched.add_job(scheduler_job, args=(dev['ip'], dev['protocol'], t['properties']), **t['trigger_args'])
			

# start scheduler
sched.start()


@app.get("/")
async def read_root():
    return FileResponse('templates/index.html', media_type='text/html')


@app.get('/model/init')
def init():	
	# get latest status of devices each request
	try:
		for dev in dev_model['devices']:
			if dev['ip'] in miot_devs:
				for prop in dev['properties']:
					ret = miot_devs[dev['ip']].get_property_by(prop['siid'], prop['piid']) # ret is a json array
					prop['value'] = ret[0]['value']
		logging.info(f'init: {dev_model}')
	except DeviceException as error:
		logging.error(format(error))

	return dev_model


@app.get('/manifest.json')
def manifest():
	return json.loads(open('manifest.json').read())


@app.get('/{png}')
def logo(png):
	return FileResponse(png)	