import os

from apscheduler.schedulers.background import BackgroundScheduler
from sanic import Sanic

from devices_manager import DevicesManager

from devices_blueprint import devices_blueprint
from schedules import device_control_job

app = Sanic('SmartHome')
html_root_path = os.path.join(os.path.dirname(os.getcwd()), 'html')
app.static('/', f'{html_root_path}/index.html', name='index')
app.static('/static', f'{html_root_path}/static', name='static')
app.static('/manifest.json', f'{html_root_path}/manifest.json', name='manifest')
app.static('/favicon.ico', f'{html_root_path}/favicon.ico', name='favicon')
app.static('/logo192.png', f'{html_root_path}/logo192.png', name='logo192')
app.static('/logo512.png', f'{html_root_path}/logo512.png', name='logo512')
app.static('/images', f'{html_root_path}/images', name='images')
app.blueprint(devices_blueprint)


@app.before_server_start
async def worker_start(_app, loop):
    _app.ctx.mgr = DevicesManager()
    _app.ctx.mgr.load_device_configs()
    scheduler = BackgroundScheduler()
    for timer in _app.ctx.mgr.get_timers():
        scheduler.add_job(device_control_job, args=(_app.ctx.mgr, timer['ip'], timer['protocol'], timer['properties']), **timer['trigger'])
    scheduler.start()
    _app.ctx.scheduler = scheduler


if __name__ == '__main__':
    app.run(access_log=True)
