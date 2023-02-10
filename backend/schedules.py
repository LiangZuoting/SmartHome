from defines import PROTOCOL_MIOT, PROTOCOL_MIDEA
from devices import set_miot_property, set_midea_property


def device_control_job(ip, protocol, properties):
    if protocol == PROTOCOL_MIOT:
        for p in properties:
            set_miot_property(ip, p['siid'], p['piid'], p['value'])
    elif protocol == PROTOCOL_MIDEA:
        for p in properties:
            set_midea_property(ip, p['id'], p['value'])
