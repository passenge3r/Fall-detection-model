# ERTC-voip相关- 通话状态消息通知

> ERTC-voip相关- 通话状态消息通知

> 更新时间: 2026-05-25T16:36:44.000+08:00

> 文档ID: 4299 | 来源树: 音视频

---

# 通话状态消息通知

webhook消息类型：ys.open.rtc

![](https://resource.eziot.com/group1/M00/01/8B/CtwQEmgAhqKAVb1GAAhcgY0aPpI494.png)

消息示例：

```
{
    "header": {
        "userId": "49d35ca942614baeaec1f8ef0151c7e1",
        "deviceId": "111222333",
        "channelNo": 1,
        "type": "ys.open.rtc",
        "messageTime": 1705910578401
    },
    "body": {
        "version": 2,
        "type": "stopLiveResponse",
        "timestamp": 1705909537774,
        "requestId": "b3bf0717ac10491da35589858a83f52f",
        "userId": "49d35ca942614baeaec1f8ef0151c7e1",
        "roomId": "111222333",
        "result": {
            "code": 1, //通话状态码
            "msg": "拨打电话中", //通话状态信息
            "status": 1,//通话状态码
            "duration": 20 //通话时长
        }
    }
}
```

通话状态枚举
![](https://resource.eziot.com/group1/M00/01/8B/CtwQE2gAhqSADq86AAT5J_JhBtg172.png)