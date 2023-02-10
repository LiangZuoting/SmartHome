import json
import logging
import os

import aiohttp
from miio import MiotDevice, DeviceException

from midea_ac_lan.midea.core.cloud import MideaCloud
from midea_ac_lan.midea.devices.ac.device import MideaACDevice


class DevicesManager:
    def __init__(self):
        self.device_models = {}
        self.miot_devices = {}
        self.midea_devices = {}

    def load_device_configs(self):
        config_path = '../model/devices'
        for f in os.listdir(config_path):
            p = os.path.join(config_path, f)
            e = os.path.splitext(f)
            if os.path.isfile(p) and os.path.splitext(f)[1].lower() == '.json':
                with open(p, encoding='utf-8') as fp:
                    config = json.loads(fp.read())
                    self.device_models[config['ip']] = config

    def get_all_device_models(self):
        return self.device_models

    def get_miot_device(self, ip, force_create=False):
        model = self.device_models[ip]
        if ip not in self.miot_devices or force_create:
            self.miot_devices[ip] = MiotDevice(ip, model['token'], lazy_discover=False)
        return self.miot_devices[ip]

    async def get_midea_device(self, ip, force_create=False):
        if ip not in self.midea_devices or force_create:
            model = self.device_models[ip]
            session = aiohttp.ClientSession()
            cloud = MideaCloud(session, 'your midea account', 'your password', 'cn')
            await cloud.login()
            token, key = await cloud.get_token(model['id'], True)
            d = MideaACDevice('', int(model['id']), ip, model['port'], token, key, 3, '', '')
            d.connect()
            self.midea_devices[ip] = d
            await session.close()
        return self.midea_devices[ip]

    def get_timers(self):
        timers = []
        for model in self.device_models.values():
            for timer in model.get('timers', []):
                for trigger in timer['trigger_args']:
                    timers.append({'ip': model['ip'], 'protocol': model['protocol'], 'properties': timer['properties'],
                                   'trigger': trigger})
        return timers

    def set_miot_property(self, ip, siid, piid, value):
        d = self.get_miot_device(ip)
        try:
            d.set_property_by(siid, piid, value)
        except DeviceException as e:
            logging.error(f'set_miot_property error {format(e)}')
            self.get_miot_device(ip, True)
            self.set_miot_property(ip, siid, piid, value)

    def get_miot_property(self, ip, siid, piid):
        d = self.get_miot_device(ip)
        try:
            return d.get_property_by(siid, piid)
        except DeviceException as e:
            logging.error(f'get_miot_property error {format(e)}')
            self.get_miot_device(ip, True)
            return self.get_miot_property(ip, siid, piid)

    async def set_midea_property(self, ip, pid, value):
        d = await self.get_midea_device(ip)
        try:
            d.set_attribute(pid, value)
        except Exception as e:
            logging.error(f'set_midea_property error {format(e)}')
            await self.get_midea_device(ip)
            await self.set_midea_property(ip, pid, value)

    async def get_midea_property(self, ip, pid):
        d = await self.get_midea_device(ip)
        try:
            return d.get_attribute(pid)
        except Exception as e:
            logging.error(f'get_midea_property error {format(e)}')
            await self.get_midea_device(ip)
            return await self.get_midea_property(ip, pid)

    def refresh_miot_device(self, ip):
        model = self.device_models[ip]
        for p in model['properties']:
            value = self.get_miot_property(ip, p['siid'], p['piid'])
            if not value:
                logging.error(f"refresh_miot_device error {ip} {p['siid']} {p['piid']}")
                continue
            p['value'] = value[0]['value']
        return model

    async def refresh_midea_device(self, ip):
        model = self.device_models[ip]
        for p in model['properties']:
            value = await self.get_midea_property(ip, p['id'])
            p['value'] = value
        return model
