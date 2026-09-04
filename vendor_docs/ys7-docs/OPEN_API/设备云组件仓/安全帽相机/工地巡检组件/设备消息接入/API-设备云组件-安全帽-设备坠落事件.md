# API-设备云组件-安全帽-设备坠落事件

> API-设备云组件-安全帽-设备坠落事件

> 更新时间: 2026-05-25T16:38:54.000+08:00

> 文档ID: 1498 | 来源树: OPEN_API

---

## 设备坠落事件

此类型基线设备并不支持，如有需要，可以联系open-team@ezvizlife.com申请设备定制。

- 事件标识

deviceDrop

- 消息类型

ISAPI上行消息

- 消息体

```
{
 "ipAddress":  "172.6.64.7", 
 /*ro, req, string, 报警设备IPv4地址, range:[1,32]*/
 "ipv6Address":  "1080:0:0:0:8:800:200C:417A", 
 /*ro, opt, string, 报警设备IPv6地址, range:[1,128]*/
 "portNo":  80, 
 /*ro, opt, int, 报警设备端口号, range:[1,65535]*/
 "protocol":  "HTTP", 
 /*ro, opt, enum, 传输通信协议类型, subType:string, [HTTP#HTTP,HTTPS#HTTPS,EHome#EHome], desc:传输通信协议HTTP/HTTPS/EHome（萤石透传ISAPI 的时候赋值HTTP或HTTPS；ISUP透传ISAPI 的时候赋值 EHome）protocolType作为历史遗留由平台兼容*/
 "macAddress":  "01:17:24:45:D9:F4", 
 /*ro, opt, string, MAC地址, range:[1,128]*/
 "channelID":  1, 
 /*ro, opt, int, 触发报警的设备通道号, desc:触发的视频通道号（1、    在SDK透传ISAPI协议的时候，上传的是 私有协议对应的视频通道号；（2、    在萤石透传ISAPI协议的时候，上传的是 萤石协议对应的视频通道号；（3、    在ISUP透传ISAPI协议的时候，上传的是 ISUP协议对应的视频通道号；*/
 "dateTime":  "2004-05-03T17:30:08+08:00", 
 /*ro, req, datetime, 报警触发时间*/
 "activePostCount":  1, 
 /*ro, opt, int, 同一个报警已经上传的次数, desc:事件触发频次脉冲事件 定义：事件持续触发（按照设备的检测频率），例如：移动侦测。瞬时事件 定义：区分目标，一个目标触发一次，例如：人脸识别activePostCount  在脉冲事件 类型触发的时候，用于区分是否是同一触发源触发的事件。例如：移动侦测，按照设备检测频率会一直上传；如果触发源发生了变化，这个时候计数就可以重新开始了。这个可以作为事件触发频次的方式来集成；*/
 "eventType":  "deviceDrop", 
 /*ro, req, enum, 事件类型, subType:string, [deviceDrop#设备跌落报警]*/
 "eventState":  "active", 
 /*ro, req, enum, 持续性时间状态, subType:string, [active#有效事件,inactive#无效事件], desc:针对持续性事件active – 表示有效事件（开始 或者 无过程状态也使用该字段）；inactive – 表示无效事件（结束）；remark:在心跳类型下，该字段赋值（表示心跳数据,10s上传一次）；*/
 "eventDescription":  "Device Drop", 
 /*ro, req, string, 事件描述*/
 "channelName":  "ABC", 
 /*ro, opt, string, 通道名称（监控点名称）, desc:与/ISAPI/Streaming/channels/<ID>的<channelName>一致*/
 "deviceID":  "test0123", 
 /*ro, opt, string, 即PUID, range:[1,64]*/
 "isDataRetransmission":  true, 
 /*ro, opt, bool, 重传数据标记, desc:由于网络异常等因素;导致的实时检测的数据上传失败;后设备异常因素恢复后重新上传当时的采集分析数据*/
 "deviceDrop": [ 
 /*ro, opt, array, 事件检测结果。, subType:object*/
  {
   "location": { 
   /*ro, opt, object, 设备本地位置信息*/
    "longitudeType":  "E", 
    /*ro, req, enum, 经度, subType:string, [E#东经,W#西经]*/
    "latitudeType":  "S", 
    /*ro, req, enum, 纬度, subType:string, [S#南纬,N#北纬]*/
    "longitude": { 
    /*ro, req, object, 经度*/
     "degree":  80, 
     /*ro, req, int, 度, range:[0,180]*/
     "minute":  13, 
     /*ro, req, int, 分, range:[0,59]*/
     "sec":  0.000000 
     /*ro, req, float, 秒, range:[0.000000,60.000000], desc:精确到小数点后6位*/
    },
    "latitude": { 
    /*ro, req, object, 纬度*/
     "degree":  80, 
     /*ro, req, int, 度, range:[0,180]*/
     "minute":  13, 
     /*ro, req, int, 分, range:[0,59]*/
     "sec":  0.000000 
     /*ro, req, float, 秒, range:[0.000000,60.000000], desc:精确到小数点后6位*/
    }
   }
  }
 ]
}
```