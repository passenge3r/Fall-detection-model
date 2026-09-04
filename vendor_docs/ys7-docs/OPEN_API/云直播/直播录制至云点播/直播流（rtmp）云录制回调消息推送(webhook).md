# 直播流（rtmp）云录制回调消息推送(webhook)

> 直播流（rtmp）云录制回调消息推送(webhook)

> 更新时间: 2026-05-25T16:43:48.000+08:00

> 文档ID: 4427 | 来源树: OPEN_API

---

# 直播流（rtmp）云录制回调消息推送(webhook)

> RTMP推流录制时，产生回调，开发者需保存该信息进行录制文件id的回调查询

## 前提

1.RTMP推流开启录制：[查看接口](https://open.ys7.com/help/4060)
2.开通webhook消息推送，[查看文档](https://open.ys7.com/help/558)

## 消息类型

ys.live.stream.event

备注：开发者接收该消息类型，需要先去 云信令-消息推送 产品里新建该类型，需要联系[小助手](https://resource.eziot.com/group1/M00/00/F3/CtwQE2VtTSuAN0y0AAAmQb_3exk350.png)后台手动开通。

## 消息格式

### 消息Header

| 名称 | 类型 | 设备信息 |
| --- | --- | --- |
| type | String | 消息类型 |
| deviceId | String | 设备id |
| channelNo | int | 设备通道 |
| userId | String | 消息回调目标开发者用户id |
| messageTime | Long | 消息投递时间 |

### 消息体body

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| version | Integer | 版本:0 |
| eventType | String | 消息类型 :streamCloudRecord(云录制记录) |
| timestamp | Long | 时间戳1723186139966 （13位） |
| streamId | String | 直播流ID |
| eventBody | Object | 事件体 |
| eventBody.data | Object | 事件体具体内容 |
| eventBody.ext | string | 事件体额外字段 |
| eventBody.data.recordStatus | int | 录制状态：1成功 |
| eventBody.data.streamId | String | 直播流id |
| eventBody.data.fileNodeId | String | 文件录制id ，获取文件下载地址（GET）<https://open.ys7.com/help/4402> |
| eventBody.data.startTime | Long | 录制开始时间（10位时间戳） |
| eventBody.data.stopTime | Long | 录制结束时间（10位时间戳） |
| eventBody.data.extJson | String | 额外信息 |

## 消息示例

```
        {
        "body": {
        "eventBody": {
        "data": {
        "eventType": "streamCloudRecord",
        "extJson": "",
        "fileNodeId": "fsd123d",
        "recordStatus": 1,
        "startTime": 1751699336,
        "stopTime": 1751699751,
        "streamId": "859883935554039808"
        },
        "ext": ""
        },
        "eventType": "streamCloudRecord",
        "streamId": "859883935554039808",
        "timestamp": 1751699363996,
        "version": 0
        },
        "header": {
        "channelNo": 1,
        "deviceId": "Bj123d",
        "messageTime": 1751699363996,
        "type": "ys.live.stream.event",
        "userId": "9277f88fc2eb46e49e17895ca41dab2a"
        }
        }

        ```
```