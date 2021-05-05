# SmartHome

自用智能家居控制系统。简化、模仿 [Home Assistant](https://www.home-assistant.io/) 的拙作，但核心诉求是一致的：本地化部署、保护隐私。

## 框架

前端：[React.js](https://reactjs.org/) + [Spectre.css](https://picturepan2.github.io/spectre/)

后端：[Flask](https://flask.palletsprojects.com/en/1.1.x/)

数据模型：`model/devices.json`。四层抽象：家—房间—设备—属性。

其它主要依赖：

+ [python-miio](https://pypi.org/project/python-miio/)，[小米Iot 设备协议规范](https://iot.mi.com/new/doc/design/spec/overall) 的 Python 实现。
+ [APScheduler](https://github.com/agronholm/apscheduler)，时间调度，用来完成定时控制。

## 部署

> 这部分不是重点，仅摘要记录，做备忘。

设备：树莓派 3B

Python：3.7.3

HTTP 服务器：nginx

网关：Gunicorn

### 大致操作步骤

0. 安装所有依赖库；

1. 复制 SmartHome 工程到树莓派；

2. 写启动脚本 `boot.sh`：

```bash
sudo /etc/init.d/nginx start
cd /home/pi/SmartHome
gunicorn -w 4 -b 127.0.0.1:5000 index:app
```

3. 开机启动：
```bash
nano /etc/rc.local

# Append this to rc.local above exit 0
su pi -c "exec /home/pi/StartHome/boot.sh"
```

4. 配置 nginx：
```bash
nano /etc/nginx/sites-available/default
```

完成后的完整配置应该是这样的（去掉了默认的注释）：

```bash
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        # HERE CHANGED
        root /home/pi/SmartHome;

        index index.html index.htm index.nginx-debian.html;

        server_name _;
        # HERE CHANGED
        location / {
                proxy_pass http://127.0.0.1:5000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                include /etc/nginx/mime.types;
        }
}
```

## 设备

> 下半年搬了新家再更新

+ [Nanoleaf 灯带](https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4011-23338211014.47.443055f28ALXh9&id=633986326481&rn=ad8c40aabbb71b7c7dce05c0a2c54c59&abbucket=12&sku_properties=13381687:10122;122276201:10122)。可调节亮度、颜色、色温。