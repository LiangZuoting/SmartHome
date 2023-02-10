import json
import logging
import os

import aiohttp
from miio import MiotDevice, DeviceException

from midea_ac_lan.midea.core.cloud import MideaCloud
from midea_ac_lan.midea.devices.ac.device import MideaACDevice

device_models = {}
miot_devices = {}
midea_devices = {}


def load_device_configs():
    config_path = '../model/devices'
    for f in os.listdir(config_path):
        p = os.path.join(config_path, f)
        if os.path.isfile(p) and os.path.splitext(f)[1].lower() == '.json':
            with open(p, encoding='utf-8') as fp:
                config = json.loads(fp.read())
                device_models[config['ip']] = config


def get_all_device_models():
    return device_models


def get_miot_device(ip, force_create=False):
    model = device_models[ip]
    if ip not in miot_devices or force_create:
        miot_devices[ip] = MiotDevice(ip, model['token'], lazy_discover=False)
    return miot_devices[ip]


async def get_midea_device(ip, force_create=False):
    if ip not in midea_devices or force_create:
        model = device_models[ip]
        session = aiohttp.ClientSession()
        cloud = MideaCloud(session, 'your midea account', 'your password', 'cn')
        await cloud.login()
        token, key = await cloud.get_token(model['id'], True)
        d = MideaACDevice('', int(model['id']), token, key, '', None)
        d.connect()
        midea_devices[ip] = d
        await session.close()
    return midea_devices[ip]


def get_timers():
    timers = []
    for model in device_models:
        for timer in model.get('timers', []):
            for trigger in timer['trigger_args']:
                timers.append({'ip': model['ip'], 'protocol': model['protocol'], 'properties': timer['properties'], 'trigger': trigger})
    return timers


def set_miot_property(ip, siid, piid, value):
    d = get_miot_device(ip)
    try:
        d.set_property_by(siid, piid, value)
    except DeviceException as e:
        logging.error(f'set_miot_property error {format(e)}')
        get_miot_device(ip, True)
        set_miot_property(ip, siid, piid, value)


def get_miot_property(ip, siid, piid):
    d = get_miot_device(ip)
    try:
        return d.get_property_by(siid, piid)
    except DeviceException as e:
        logging.error(f'get_miot_property error {format(e)}')
        get_miot_device(ip, True)
        return get_miot_property(ip, siid, piid)


def set_midea_property(ip, pid, value):
    d = get_midea_device(ip)
    try:
        d.set_attribute(pid, value)
    except Exception as e:
        logging.error(f'set_midea_property error {format(e)}')
        get_midea_device(ip)
        set_midea_property(ip, pid, value)


def get_midea_property(ip, pid):
    d = get_midea_device(ip)
    try:
        return d.get_attribute(pid)
    except Exception as e:
        logging.error(f'get_midea_property error {format(e)}')
        get_midea_device(ip)
        return get_midea_property(ip, pid)


def refresh_miot_device(ip):
    model = device_models[ip]
    for p in model['properties']:
        value = get_miot_property(ip, p['siid'], p['piid'])
        if not value:
            logging.error(f"refresh_miot_device error {ip} {p['siid']} {p['piid']}")
            continue
        p['value'] = value[0]['value']
    return model


def refresh_midea_device(ip):
    model = device_models[ip]
    for p in model['properties']:
        value = get_midea_property(ip, p['id'])
        p['value'] = value
    return model
