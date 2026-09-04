# API-设备云组件仓-智能电梯网络摄像机-设备消息接入-电梯运行状态实时上报事件

> API-设备云组件仓-智能电梯网络摄像机-设备消息接入-电梯运行状态实时上报事件

> 更新时间: 2026-05-25T16:39:07.000+08:00

> 文档ID: 1608 | 来源树: OPEN_API

---

# 电梯运行状态定时上报事件

- 电瓶车进入、困人等异常事件实时上报。

## 消息类型

- ISAPI上行消息

## 事件标识

- elevatorRunningStatus

## 消息体

```
{
	"ipAddress":  "172.6.64.7",	
	/*ro, req, string, 报警设备IPv4地址*/
	"ipv6Address":  "1080:0:0:0:8:800:200C:417A",	
	/*ro, opt, string, 报警设备IPv6地址*/
	"portNo":  80,	
	/*ro, opt, int, 报警设备端口号*/
	"protocol":  "HTTP",	
	/*ro, opt, enum, 传输通信协议类型, subType:string, [HTTP#HTTP,HTTPS#HTTPS,EHome#EHome], desc:传输通信协议HTTP/HTTPS/EHome（萤石透传ISAPI 的时候赋值HTTP；ISUP透传ISAPI 的时候赋值 EHome）protocolType作为历史遗留由平台兼容*/
	"macAddress":  "01:17:24:45:D9:F4",	
	/*ro, opt, string, MAC地址*/
	"channelID":  1,	
	/*ro, opt, int, 触发报警的设备通道号, desc:触发的视频通道号（1、    在SDK透传ISAPI协议的时候，上传的是 私有协议对应的视频通道号；（2、    在萤石透传ISAPI协议的时候，上传的是 萤石协议对应的视频通道号；（3、    在ISUP透传ISAPI协议的时候，上传的是 ISUP协议对应的视频通道号；*/
	"dateTime":  "2004-05-03T17:30:08+08:00",	
	/*ro, req, datetime, 报警触发时间*/
	"activePostCount":  1,	
	/*ro, opt, int, 同一个报警已经上传的次数, desc:事件触发频次脉冲事件 定义：事件持续触发（按照设备的检测频率），例如：移动侦测。瞬时事件 定义：区分目标，一个目标触发一次，例如：人脸识别activePostCount  在脉冲事件 类型触发的时候，用于区分是否是同一触发源触发的事件。例如：移动侦测，按照设备检测频率会一直上传；如果触发源发生了变化，这个时候计数就可以重新开始了。这个可以作为事件触发频次的方式来集成；*/
	"eventType":  "elevatorRunningStatus",	
	/*ro, req, string, 事件类型*/
	"eventState":  "active",	
	/*ro, req, enum, 事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
	"eventDescription":  "Detector Running Status",	
	/*ro, req, string, 事件描述*/
	"elevatorRunningStatus": {	
	/*ro, opt, object, 电梯运行实时状态*/
		"statusType":  "upward"	
		/*ro, req, enum, 运行距离, subType:string, [upward#上行,down#下行,open#开门,batteryCarIn#电瓶车进入,abnormalLoop#回路异常,overspeed#超速,header#冲顶,openRuning#开门行梯,abnormalVibration#异常振动,stuck#困人,unFlatLayerOpen#非平层开门,outage#断电,temperatureAnomal#温度异常,iblockDoor#挡门报警]*/
	}
}
```