import os
import smtplib
import ssl

from apscheduler.schedulers.background import BackgroundScheduler
from sanic import Sanic

from devices import load_device_configs, get_timers
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


@app.main_process_start
async def main_start(_app):
    load_device_configs()
    scheduler = BackgroundScheduler()
    for timer in get_timers():
        scheduler.add_job(device_control_job, args=(timer['ip'], timer['protocol'], timer['properties']), **timer['trigger'])
    scheduler.start()
    _app.ctx.scheduler = scheduler


if __name__ == '__main__':
    app.run()
