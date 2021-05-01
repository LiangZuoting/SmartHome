sudo /etc/init.d/nginx start
cd /home/pi/SmartHome
gunicorn -w 4 -b 127.0.0.1:5000 index:app