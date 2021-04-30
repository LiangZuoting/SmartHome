#!usr/bin/env python3
import os
from flask import Flask, render_template, request, json
from miio import MiotDevice

app = Flask(__name__)

# connecting to devices when boot
dev_model = json.load(open(os.path.join('./static', 'devices.json')))
# map from ip to device object
miot_devs = {}
for room in dev_model['rooms']:
	if 'devices' in room:
		for dev in room['devices']:
			if dev['protocol'] == 'miot':
				miot_devs[dev['ip']] = MiotDevice(dev['ip'], dev['token'])


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/', methods=['POST'])
def update():
	data = request.get_json()
	if (data['ip'] in miot_devs):
		miot_devs[data['ip']].set_property_by(data['siid'], data['piid'], data['value'])
		

@app.route('/init')
def init():	
	# get latest status of devices each request
	for room in dev_model['rooms']:
		if 'devices' in room:
			for dev in room['devices']:
				if dev['ip'] in miot_devs:
					for prop in dev['properties']:
						prop['value'] = miot_devs[dev['ip']].get_property_by(prop['siid'], prop['piid'])
	return dev_model