#!usr/bin/env python3
import os
from flask import Flask, render_template, request, json, send_from_directory, jsonify
from flask.logging import default_handler
from miio import MiotDevice
from apscheduler.schedulers.background import BackgroundScheduler
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
		'filename': 'logs/flask.log',
		'maxBytes': 4096000,
		'backupCount': 10,
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
app = Flask(__name__)
app.logger.info('flask started...')
	
sched = BackgroundScheduler()


def scheduler_job(ip, protocol, properties):
	if protocol == 'miot':
		for p in properties:
			miot_devs[ip].set_property_by(p['siid'], p['piid'], p['value'])


# connecting to devices when boot
dev_model = json.load(open(os.path.join('./model', 'devices.json')))
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


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/', methods=['POST'])
def update():
	data = request.get_json()
	ip = data['ip']
	if (ip in miot_devs):
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
	return jsonify(data)
		

@app.route('/model/init')
def init():	
	# get latest status of devices each request
	for dev in dev_model['devices']:
		if dev['ip'] in miot_devs:
			for prop in dev['properties']:
				ret = miot_devs[dev['ip']].get_property_by(prop['siid'], prop['piid']) # ret is a json array
				prop['value'] = ret[0]['value']
	app.logger.info(f'init: {dev_model}')
	return jsonify(dev_model)


@app.route('/manifest.json')
def manifest():
	return send_from_directory('./', 'manifest.json')


@app.route('/logo192.png')
def logo192():
	return send_from_directory('./', 'logo192.png')


@app.route('/logo512.png')
def logo512():
	return send_from_directory('./', 'logo512.png')


@app.route('/images/ac.svg')
def ac():
	return send_from_directory('./images/', 'ac.svg')


@app.route('/images/ceilinglight.svg')
def ceilinglight():
	return send_from_directory('./images/', 'ceilinglight.svg')


@app.route('/images/lightstrip.svg')
def lightstrip():
	return send_from_directory('./images/', 'lightstrip.svg')