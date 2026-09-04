# API-设备云组件-宠物喂食器-余量监测-【消息】余量不足事件

> API-设备云组件-宠物喂食器-余量监测-【消息】余量不足事件

> 更新时间: 2026-05-25T16:39:40.000+08:00

> 文档ID: 1559 | 来源树: OPEN_API

---

## 【消息】余量不足事件

- 事件标识

FoodNotEnough

- 消息类型

OTAP消息（ys.iot）

- 消息体（属于宠物喂食器领域（PetFeeder），当余量不足时，产生告警消息）

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| basic. ipV4Address | 事件基础信息 | string |  |  | N |
| basic. ipV6Address | 设备ipv6地址 | string |  |  | N |
| basic. macAddress | 设备MAC地址 | string | [17,17] |  | N |
| basic. dateTime | 时间 | string |  |  | Y |
| basic. UUID | 上传事件唯一标识 | string | [0,64] |  | Y |
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

- 示例

```
{
  "basic": {
    "ipV4Address": "10.65.101.171",
    "ipV6Address": "fe80::4883:315d:e4c:75bc",
    "macAddress": "0C-9D-92-99-DD-31",
    "dateTime": "2021-01-28T02:00:00+08:00",
    "UUID": "079f23cd-0988-459f-96f5-fa1c507dd07c"
  },
  "notification": {
    "relationId": "stringstringstringstringstringstringstringstringstringstringstri",
    "status": 1,
    "action": 0,
    "location": "string",
    "pictures": [
      {
        "cloudtype": 0,
        "bucket": "string",
        "type": "string",
        "length": 0,
        "crypt": 0,
        "fileid": "string",
        "tinyvideo": 0,
        "checksum": "string",
        "lifecycle": 0
      }
    ]
  }
}
```