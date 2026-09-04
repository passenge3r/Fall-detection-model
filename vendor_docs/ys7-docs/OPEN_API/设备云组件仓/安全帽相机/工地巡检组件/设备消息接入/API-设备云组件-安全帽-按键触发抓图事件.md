# API-设备云组件-安全帽-按键触发抓图事件

> API-设备云组件-安全帽-按键触发抓图事件

> 更新时间: 2026-05-25T16:38:53.000+08:00

> 文档ID: 1497 | 来源树: OPEN_API

---

## 按键触发抓图事件

注意，请将设备处于正常公网环境下，如使用内网环境，无法上报。

- 事件标识

localButtonSnapshot

- 消息类型

ISAPI上行消息

- 消息体

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
 "eventType":  "localButtonSnapshot", 
 /*ro, req, string, 事件类型, desc:设备本地按键手动触发抓图*/
 "eventState":  "active", 
 /*ro, req, enum, 事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
 "eventDescription":  "local button snapshot", 
 /*ro, req, string, 事件描述, desc:通过设备本地按键手动触发抓图*/
 "deviceID":  "test0123", 
 /*ro, opt, string, 即PUID, range:[1,64], desc:在ehome协议接入透传ISAPI事件信息中必须返回*/
 "LocalButtonSnapshot": { 
 /*ro, opt, object, 设备本地按键触发抓图信息上报*/
  "ButtonSnapshot": { 
  /*ro, opt, object, 设备本地按键触发抓图, desc:设备本地按键手动触发抓取的图片*/
   "resourcesContentType":  "url", 
   /*ro, req, enum, 资源传输类型, subType:string, [url#url方式传输], desc:当设备返回的报警报文中带有额外资源（比如图片）时,该节点必须返回,url-url方式传输*/
   "resourcesContent":  "http://10.13.50.100:6120/pic?=d63i0872ed611i89-5p3009--26b43e17f9eafi5b2*=2d9i0s1*=idp1*=*d176t=a-9m55b3d25b4" 
   /*ro, req, string, 资源标识ID, range:[1,1024], desc:当设备返回的报警报文中带有额外资源（比如图片）时,该节点必须返回;当resourcesContentType为url时,该节点填写具体的url*/
  }
 }
}
```