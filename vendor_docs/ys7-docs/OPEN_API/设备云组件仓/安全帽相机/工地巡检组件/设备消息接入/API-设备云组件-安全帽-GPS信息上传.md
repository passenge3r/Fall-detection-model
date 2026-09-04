# API-设备云组件-安全帽-GPS信息上传

> API-设备云组件-安全帽-GPS信息上传

> 更新时间: 2026-05-25T16:38:54.000+08:00

> 文档ID: 1501 | 来源树: OPEN_API

---

## 按键触发抓图事件GPS信息上传

注意，使用该设备，需要将设备处于室外（室内不上报），并打开定位模式，将其处于GPS、北斗模式、混合模式。

- 事件标识

GPSUpload

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
 "eventType":  "GPSUpload", 
 /*ro, req, enum, 事件类型, subType:string, [GPSUpload#GPS信息上传]*/
 "eventState":  "active", 
 /*ro, req, enum, 事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
 "eventDescription":  "GPS information", 
 /*ro, req, enum, 事件描述, subType:string, [GPS information#GPS信息上传]*/
 "devIndex":  "test", 
 /*ro, opt, string, 报警设备唯一标示 string类型*/
 "channelName":  "test", 
 /*ro, req, string, 设备通道名称, range:[0,64]*/
 "deviceID":  "test", 
 /*ro, opt, string, 设备ID, range:[0,256]*/
 "isDataRetransmission":  true, 
 /*ro, opt, bool, 重传数据标记, desc:由于网络异常等因素;导致的实时检测的数据上传失败;后设备异常因素恢复后重新上传当时的采集分析数据*/
 "GPS": { 
 /*ro, req, object, GPS信息*/
  "divisionEW":  "E", 
  /*ro, req, enum, 东西半球, subType:string, [E#东半球,W#西半球]*/
  "longitude":  100, 
  /*ro, req, int, 经度, desc:经度=实际度*3600*100+实际分*60*100+实际秒*100*/
  "divisionNS":  "N", 
  /*ro, req, enum, 南北半球, subType:string, [N#北半球,S#南半球]*/
  "latitude":  100, 
  /*ro, req, int, 纬度, desc:纬度=实际度*3600*100+实际分*60*100+实际秒*100 integer32类型*/
  "direction":  100, 
  /*ro, opt, int, 车辆方向, desc:车辆方向=实际方向（以度为单位，正北方向为0，顺时针方向计算）*100*/
  "speed":  100, 
  /*ro, opt, int, 速度, desc:速度：厘米/小时*/
  "satellites":  1, 
  /*ro, opt, int, 卫星数量*/
  "precision":  1, 
  /*ro, opt, int, 精度因子*/
  "height":  1, 
  /*ro, opt, int, 高度, unit:cm, unitType:长度*/
  "retransFlag":  1, 
  /*ro, opt, enum, 重传标记, subType:int, [0#本条GPS为实时包,1#本条GPS为重传包]*/
  "timeZone":  "HH::MM", 
  /*ro, opt, string, 时区, desc:时区，在标准时区基础上加减一段时间，跟TimeZoneIdx 含义冲突，优先使用TimeZoneIdx*/
  "timeZoneIdx":  1 
  /*ro, opt, enum, 时区, subType:int, [0#无效,1#(GMT-12:00)日界线西,2#(GMT-11:00) 萨摩亚群岛,3#(GMT-10:00) 夏威夷,4#(GMT-09:00) 阿拉斯加,5#(GMT-08:00) 太平洋时间(美国和加拿大),6#(GMT-07:00) 山地时间 (美国和加拿大),7#(GMT-06:00) 中部时间 (美国和加拿大),8#(GMT-05:00) 东部时间 (美国和加拿大),9#(GMT-04:30) 加拉加斯,10#(GMT-04:00) 大西洋时间 (加拿大),11#(GMT-03:30) 纽芬兰,12#(GMT-03:00) 巴西利亚,13#(GMT-02:00) 中大西洋,14#(GMT-01:00) 佛得角群岛,15#(GMT) 都柏林,16#(GMT+01:00) 阿姆斯特丹,17#(GMT+02:00) 哈拉雷,18#(GMT+03:00) 巴格达,19#(GMT+03:30) 德黑兰,20#(GMT+04:00) 阿布扎比,21#(GMT+04:30) 喀布尔,22#(GMT+05:00) 叶卡捷琳堡,23#(GMT+05:30) 马德拉斯,24#(GMT+05:45) 加德满都,25#(GMT+06:00) 阿斯塔纳,26#(GMT+06:30) 仰光,27#(GMT+07:00) 曼谷,28#(GMT+08:00) 北京,29#(GMT+09:00) 大阪,30#(GMT+09:30) 达尔文,31#(GMT+10:00) 关岛,32#(GMT+11:00) 马加丹,33#(GMT+12:00) 奥克兰,34#(GMT+13:00) 努库阿洛法,35#(GMT+14:00) 圣诞岛], desc:时区*/
 }
}
```