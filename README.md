# SmartHome

自用智能家居控制系统。简化、模仿 [Home Assistant](https://www.home-assistant.io/) 的拙作，但核心诉求是一致的：本地化部署、保护隐私。

## ChangeLog

2022.01.15:

1. 拆分设备描述文件，每一个设备单独一个 json 文件；
2. 首页启动时不再获取全部设备最新状态，延迟到用户浏览具体设备时更新。

## 框架

前端：[React.js](https://reactjs.org/) + ~~[Spectre.css](https://picturepan2.github.io/spectre/)~~ [AntD](https://ant.design/components/overview-cn/)

后端：~~Flask~~ [Sanic](https://sanicframework.org/en/)

**数据模型：`model/devices.json`**

常用属性：

+ `ui`：设备对应的 svg 图片 url。

+ `color`：`shape` 的填充色。

+ `properties`：可调节的设备参数集。`"name": "开关"` 是预置属性，关联设备的开关状态。通常所有设备都应该有且唯一，可以通过查询 `name` 获取设备是否正在运行。

+ `timers`：定时任务。内含一组 `properties` 子集，达到设定时间时批量应用设备参数新值。定时器规则描述完全遵从 APScheduler 参数，从而可以解包后直接透传到 APScheduler 接口。

+ `scenes`：预设场景。同样用作批量应用一组设备参数的新值。

+ 设备参数描述属性：根据不同设备能力各自不同，但格式统一：必须是 `properties` 数组下的一个对象；必须有 `id` 和 `value` 两个固定属性。`id` 要求全局唯一；`value` 标识设备参数当前值。

其它主要依赖：

+ [python-miio](https://pypi.org/project/python-miio/)，[小米Iot 设备协议规范](https://iot.mi.com/new/doc/design/spec/overall) 的 Python 实现。
+ [midea-msmart](https://github.com/mac-zhou/midea-msmart)，社区实现的美的空调控制协议的 Python 实现。
+ [APScheduler](https://github.com/agronholm/apscheduler)，时间调度，用来完成定时控制。

## UI、UX 设计

首页以 SVG 绘制出户型图后，通过数据模型动态放置所有设备到 SVG 图相应位置。点击设备后跳转到设备编辑页面。

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
python3 -m sanic server.app --host=127.0.0.1 --port=9876 --workers=4
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
                proxy_pass http://127.0.0.1:9876;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                include /etc/nginx/mime.types;
        }
}
```

## 设备

> ~~下半年搬了新家再更新~~

+ [Nanoleaf 灯带](https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4011-23338211014.47.443055f28ALXh9&id=633986326481&rn=ad8c40aabbb71b7c7dce05c0a2c54c59&abbucket=12&sku_properties=13381687:10122;122276201:10122)。可调节亮度、颜色、色温。
+ [小米空调](https://detail.tmall.com/item.htm?id=641086203155&spm=a1z09.2.0.0.791a2e8d6AeEvp&_u=rotdgsn6a13&skuId=4602713733084)
+ [美的空调](https://detail.tmall.com/item.htm?spm=a220o.1000855.1000983.1.222a367cjYyr4N&id=621252234232&standard=1)
+ [Aqara A1 窗帘电机](https://detail.tmall.com/item.htm?id=617317348784&spm=a1z09.2.0.0.791a2e8d6AeEvp&_u=rotdgsn33f1)

## 问题

1. 美的空调在断电重连时会重新分配 token 和 key。应该将 midea-discover 设备发现功能集成到 msmart。