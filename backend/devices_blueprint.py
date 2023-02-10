from sanic import Blueprint, response

from defines import PROTOCOL_MIOT, PROTOCOL_MIDEA

devices_blueprint = Blueprint('devices_blueprint', url_prefix='/api/devices')


@devices_blueprint.get('/')
async def get_all_devices(request):
    return response.json(request.app.ctx.mgr.get_all_device_models())


@devices_blueprint.get('/<ip:path>')
async def get_device(request, ip: str):
    mgr = request.app.ctx.mgr
    protocol = mgr.get_all_device_models()[ip]['protocol']
    if protocol == PROTOCOL_MIOT:
        return response.json(mgr.refresh_miot_device(ip))
    elif protocol == PROTOCOL_MIDEA:
        return response.json(await mgr.refresh_midea_device(ip))


@devices_blueprint.post('/<ip:path>')
async def set_device(request, ip: str):
    mgr = request.app.ctx.mgr
    value = request.json['value']
    protocol = mgr.get_all_device_models()[ip]['protocol']
    if protocol == PROTOCOL_MIOT:
        siid = request.json['siid']
        piid = request.json['piid']
        mgr.set_miot_property(ip, siid, piid, value)
        return response.json(mgr.refresh_miot_device(ip))
    elif protocol == PROTOCOL_MIDEA:
        pid = request.json['id']
        mgr.set_midea_property(ip, pid, value)
        return response.json(await mgr.refresh_midea_device(ip))
