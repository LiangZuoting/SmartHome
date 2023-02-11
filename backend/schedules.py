import asyncio

from defines import PROTOCOL_MIOT, PROTOCOL_MIDEA


def device_control_job(mgr, ip, protocol, properties):
    if protocol == PROTOCOL_MIOT:
        for p in properties:
            mgr.set_miot_property(ip, p['siid'], p['piid'], p['value'])
    elif protocol == PROTOCOL_MIDEA:
        for p in properties:
            asyncio.run(mgr.set_midea_property(ip, p['id'], p['value']))
