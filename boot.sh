sudo /etc/init.d/nginx start
cd /home/pi/SmartHome
python3 -m sanic server.app --host=127.0.0.1 --port=9876 --workers=4
