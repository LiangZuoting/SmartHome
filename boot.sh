sudo /etc/init.d/nginx start
cd /home/pi/SmartHome/backend
python3 -m sanic main.app --host=127.0.0.1 --port=9876 --workers=1
