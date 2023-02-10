from sanic import Blueprint, response

from defines import PROTOCOL_MIOT, PROTOCOL_MIDEA
from devices import get_all_device_models, refresh_miot_device, refresh_midea_device, set_miot_property, \
    set_midea_property

devices_blueprint = Blueprint('devices_blueprint', url_prefix='/api/devices')


@devices_blueprint.get('/')
async def get_all_devices(_request):
    return response.json(get_all_device_models())


@devices_blueprint.get('/<ip:path>')
async def get_device(_request, ip: str):
    protocol = get_all_device_models()[ip]['protocol']
    if protocol == PROTOCOL_MIOT:
        return response.json(refresh_miot_device(ip))
    elif protocol == PROTOCOL_MIDEA:
        return response.json(refresh_midea_device(ip))


@devices_blueprint.post('/<ip:path>')
async def set_device(request, ip: str):
    value = request.json['value']
    protocol = get_all_device_models()[ip]['protocol']
    if protocol == PROTOCOL_MIOT:
        siid = request.json['siid']
        piid = request.json['piid']
        set_miot_property(ip, siid, piid, value)
        return response.json(refresh_miot_device(ip))
    elif protocol == PROTOCOL_MIDEA:
        pid = request.json['id']
        set_midea_property(ip, pid, value)
        return response.json(refresh_midea_device(ip))
