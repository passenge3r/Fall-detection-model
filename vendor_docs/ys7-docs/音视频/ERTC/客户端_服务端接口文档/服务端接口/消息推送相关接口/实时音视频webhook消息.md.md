# 实时音视频webhook消息.md

> 实时音视频webhook消息

> 更新时间: 2026-05-25T16:36:48.000+08:00

> 文档ID: 4913 | 来源树: 音视频

---

# 实时音视频webhook消息

## 前提

开通webhook消息推送，[查看文档](https://open.ys7.com/help/558)

## 消息类型

> ys.open.rtc.call

备注：开发者接收该消息类型，需要先去 云信令-消息推送 产品里勾选该类型，需要联系[小助手](https://resource.eziot.com/group1/M00/00/F3/CtwQE2VtTSuAN0y0AAAmQb_3exk350.png)开通。

> 不开通会导致无法收到设备呼叫消息

![](https://resource.eziot.com/group2/M00/01/0E/CtwQFmlD5TCADrevAAK6WGubUaY307.png)

## 消息格式

### 消息Header

| 名称 | 类型 | 是否必须 | 设备信息 |
| --- | --- | --- | --- |
| type | String | Yes | 消息类型 |
| userId | String | Yes | 消息回调目标开发者用户id |
| messageTime | Long | Yes | 消息投递时间 |
| deviceId | String | Yes | 设备序列号 |
| channelNo | String | No | 设备通道号 |

### 消息体

| 名称 | 类型 | 是否必须 | 描述 |
| --- | --- | --- | --- |
| version | Integer | No | 版本，目前只有1 |
| strRoomId | String | No | 房间号，action=request时使用，加入房间使用 |
| action | String | Yes | request-设备发起呼叫，cancel-设备取消呼叫，reject-设备拒绝接听，busy-设备繁忙导致无法接听，bellTimeout-设备响铃超时 |
| account | String | No | 联系人id，action=request时使用，加入房间使用 |
| appId | String | No | 应用id，action=request时使用，加入房间使用 |
| callId | Integer | No | 某次通话的唯一标识 |
| timestamp | Long | Yes | 时间戳 |

## 消息示例

```
{
    "body": {
        "account": "15869035000",
        "action": "request",
        "appId": "2c6041dcc1134c75887cd10ecf8d5e55",
        "callId": "a9143d25e9ba488199963186604efe56",
        "strRoomId": "1111",
        "timestamp": 1758871377508,
        "version": 1
    },
    "header": {
        "channelNo": 1,
        "deviceId": "BD1231873",
        "messageTime": 1758871377508,
        "type": "ys.open.rtc.call",
        "userId": "d0001a7eb052411d81bfaf62c4b79259"
    }
}
```