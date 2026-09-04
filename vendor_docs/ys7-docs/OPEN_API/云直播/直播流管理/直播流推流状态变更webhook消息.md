# 直播流推流状态变更webhook消息

> 直播流推流状态变更webhook消息

> 更新时间: 2026-07-16T13:33:24.000+08:00

> 文档ID: 4070 | 来源树: OPEN_API

---

# 直播流推流状态变更webhook消息

## 前提

开通webhook消息推送，[查看文档](https://open.ys7.com/help/5128)

## 消息类型

ys.stream.manage

备注：开发者接收该消息类型，需要先去 云信令-消息推送 产品里新建该类型，需要联系[小助手](https://resource.eziot.com/group1/M00/00/F3/CtwQE2VtTSuAN0y0AAAmQb_3exk350.png)后台手动开通。

## 消息格式

### 消息Header

| 名称 | 类型 | 设备信息 |
| --- | --- | --- |
| type | String | 消息类型 |
| userId | String | 消息回调目标开发者用户id |
| messageTime | Long | 消息投递时间 |
| deviceId | String | 设备序列号 |
| channelNo | String | 设备通道号 |

### 消息体

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| version | Integer | 版本 |
| type | String | 消息类型 |
| streamId | String | 直播流ID |
| client | String | 客户端标识 |
| status | int | 状态：1-开始播放，2-结束播放，3-开始推流，4-结束推流， 101-启用流，102-禁用流 |
| reason | int | 结束推流原因：1-流ID不存在，2-流禁用、3-不在可用时间区间、4-用户设备关系验证失败、5-通道隐藏、6-4G无限流量卡、7-其他错误 |
| timestamp | Long | 时间戳 |

## 消息示例

```
{
    "body": {
        "version": 1,
        "type": "StreamStatusChange",
        "streamId": "787305182210818048",
        "client": "127.0.0.1:8080",
        "status": 1,
        "timestamp": 1734000656000
    },
    "header": {
        "deviceId": "BB8812187",
        "messageTime": 1723186139966,
        "type": "ys.stream.manage",
        "userId": "fa42d897a26c46f193c45e849c2df237"
    }
}
```