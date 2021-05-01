#!usr/bin/env python3
import os
from flask import Flask, render_template, request, json, send_from_directory, jsonify
from miio import MiotDevice

app = Flask(__name__)

# connecting to devices when boot
dev_model = json.load(open(os.path.join('./model', 'devices.json')))
# map from ip to device object
miot_devs = {}
for room in dev_model['rooms']:
	if 'devices' in room:
		for dev in room['devices']:
			if dev['protocol'] == 'miot':
				miot_devs[dev['ip']] = MiotDevice(dev['ip'], dev['token'], lazy_discover=False)


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/', methods=['POST'])
def update():
	data = request.get_json()
	app.logger.info(f'recv post request {data}')
	if (data['ip'] in miot_devs):
		ret = miot_devs[data['ip']].set_property_by(data['siid'], data['piid'], data['value'])
		app.logger.info(f'set_property_by result {ret}')
	return jsonify(data)
		

@app.route('/model/init')
def init():	
	# get latest status of devices each request
	for room in dev_model['rooms']:
		if 'devices' in room:
			for dev in room['devices']:
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