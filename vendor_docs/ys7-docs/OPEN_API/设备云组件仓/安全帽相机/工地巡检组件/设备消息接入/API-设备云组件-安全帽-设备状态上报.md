# API-设备云组件-安全帽-设备状态上报

> API-设备云组件-安全帽-设备状态上报

> 更新时间: 2026-05-25T16:38:54.000+08:00

> 文档ID: 1500 | 来源树: OPEN_API

---

## 设备状态上报

- 事件标识

deviceStatus

- 消息类型

ISAPI上行消息

- 消息体

```
{
 "ipAddress":  "172.6.64.7", 
 /*ro, req, string, 报警设备IPv4地址*/
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
 "eventType":  "deviceStatus", 
 /*ro, req, string, 事件类型, desc:deviceStatus-设备状态*/
 "eventState":  "active", 
 /*ro, req, enum, 事件状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
 "eventDescription":  "device Status", 
 /*ro, req, string, 事件描述*/
 "deviceID":  "test0123", 
 /*ro, opt, string, 即PUID, range:[1,64], desc:在ISUP协议接入透传ISAPI事件信息中必须返回*/
 "serialNumber":  "test", 
 /*ro, opt, string, 设备序列号, range:[9,48]*/
 "DeviceStatus": { 
 /*ro, opt, object, 设备状态*/
  "MemoryList": [ 
  /*ro, opt, array, 内存数据列表, subType:object, range:[0,100]*/
   {
    "memoryUsage":  100.0, 
    /*ro, req, float, 已用内存大小, range:[0.0,1048576.0], unit:MB, unitType:信息量, desc:保留一位小数*/
    "memoryAvailable":  100.0 
    /*ro, req, float, 可用内存大小, range:[0.0,1048576.0], unit:MB, unitType:信息量, desc:保留一位小数*/
   }
  ],
  "recordStatusList": [ 
  /*ro, opt, array, 录像状态列表, subType:object, range:[0,1]*/
   {
    "channelID":  1, 
    /*ro, req, int, 视频通道号*/
    "recordStatus":  "recording", 
    /*ro, req, enum, 录像状态, subType:string, [notRecorded#未录像,recording#录像中]*/
    "recordremainingDuration":  5 
    /*ro, opt, int, 录制剩余时长, range:[0,10000], unit:min*/
   }
  ],
  "lightStatusList": [ 
  /*ro, opt, array, 灯光状态列表, subType:object, range:[0,2]*/
   {
    "lightType":  "supplementLight", 
    /*ro, req, enum, 灯光类型, subType:object, [supplementLight#补光灯,laserLight#激光灯]*/
    "lightStatus":  "open" 
    /*ro, req, enum, 拨号状态, subType:object, [open#开启,close#关闭]*/
   }
  ],
  "batteryList": [ 
  /*ro, opt, array, 电池状态列表, subType:object, range:[0,1]*/
   {
    "id":  1, 
    /*ro, req, int, 电池id, range:[1,10]*/
    "state":  "discharging", 
    /*ro, req, enum, 网络状态, subType:object, [discharging#未充电(放电中),charing#充电中,idle#空闲,abnormal#异常]*/
    "remainingBattery":  5, 
    /*ro, req, int, 剩余电量, range:[0,10000], unit:mA, unitType:电流*/
   }
  ]
 }
}
```