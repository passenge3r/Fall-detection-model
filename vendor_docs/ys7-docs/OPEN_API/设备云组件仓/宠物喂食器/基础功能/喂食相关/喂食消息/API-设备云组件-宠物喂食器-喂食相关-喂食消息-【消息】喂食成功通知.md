# API-设备云组件-宠物喂食器-喂食相关-喂食消息-【消息】喂食成功通知

> API-设备云组件-宠物喂食器-喂食相关-喂食消息-【消息】喂食成功通知

> 更新时间: 2026-05-25T16:39:44.000+08:00

> 文档ID: 1592 | 来源树: OPEN_API

---

## 【消息】喂食成功通知（FeedSuccessNotify）

- 事件标识

FeedSuccessNotify

- 消息类型

OTAP消息（ys.iot）

- 消息体（成功喂食后即会产生相关消息）

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| basic. ipV4Address | 事件基础信息 | string |  |  | N |
| basic. dateTime | 时间 | string |  |  | Y |
| basic. UUID | 上传事件唯一标识 | string | [0,64] |  | Y |
| basic. continue | 续有相同UUID的报文(用于补充图片) | boolean |  | 默认为false，后续不会有相同UUID的报文。不带图片或则带图片的事件无实时性要求，该节点可以不要。 | N |
| basic. timestamp | 消息时间戳 | number |  | 消息时间戳，UTC 1970-01-01 0时开始的毫秒数。行业设备可以不带 | N |
| notification. relationId | 互联互通消息ID | strin | [0,64] |  | N |
| notification. status | 事件状态 | number |  | 1发生，2停止，该字段目前无实际效果，但予以保留 | N |
| notification. action | 事件状态 | number |  | 8：不推送 | N |
| notification. location | 设备安装位置附加信息 | string |  |  | N |
| notification. pictures. cloudtype | 云存储类型 | integer |  | 存储节点编号，根据图片上传信息响应中的同名字段填写。当采用简单存储协议时，为固定值 -1 | Y |
| notification. pictures. bucket | 云存储bucket名称 | string |  | 根据图片上传信息响应中的同名字段填写。存储桶信息，采用简单存储协议时，为空 | Y |
| notification. pictures. type | 文件格式 | string |  | 图片格式 | N |
| notification. pictures. length | 图片长度 | integer |  | 单位：字节 | N |
| notification. pictures. crypt | 加密类型 | integer |  | 加密类型：2平台加密，1设备加密，0不加密。注意一条消息中的所有图片必须采用相同的加密方式与加密密钥。 | N |
| notification. pictures. fileid | 存储KEY | string |  | 存储KEY,根据图片上传信息响应中的同名字段填写 | Y |
| notification. pictures. tinyvideo | 报警小视频 | int |  | 0-没有报警小视频；1-有报警小视频 | N |
| notification. pictures. checksum | 校验和 | string | [0,32] | 对应老协议CapturePicture:CheckSum，如为设备加密，则是设备密钥的checksum，如为平台加密，则为平台加密的密钥部分信息。如没有加密则为空 | N |
| notification. pictures. lifecycle | 云图片的存储周期 | integer |  | 云图片的存储周期 ，根据图片上传信息响应中的同名字段填写。该字段仅作记录，不会实际影响图片的存储周期。单位：天 | N |
| payload. value | 自定义内容 | boolean |  | Success-成功 NoFoodOut-未出粮 Jam-卡粮 | Y |

- 示例

```
{
  "notification": {
    "action": 0,
    "location": "string",
    "relationId": "string",
    "pictures": [
      {
        "bucket": "string",
        "lifecycle": 0,
        "crypt": 0,
        "cloudtype": 0,
        "length": 0,
        "checksum": "string",
        "type": "string",
        "tinyvideo": 0,
        "fileid": "string"
      }
    ],
    "status": 1
  },
  "payload": {
    "value": true
  },
  "basic": {
    "dateTime": "stringstringstringstrings",
    "continue": false,
    "ipV4Address": "8.8.8.8",
    "UUID": "string",
    "timestamp": 0
  }
}
```

,