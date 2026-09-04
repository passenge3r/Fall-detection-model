# index.md

> 更新时间: 2026-05-25T16:43:26.000+08:00

> 文档ID: 3897 | 来源树: OPEN_API

---

## 【消息】｛｛name｝｝（PeopleFallingDownDetection）

- 事件标识

PeopleFallingDownDetection

- 消息类型

OTAP消息（ys.iot）

- 消息体（）

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| -- | -- | -- | -- | -- | -- |
| notification.notification | 通知事件内容 | object |  | 提醒消息基础字段，所有告警提醒类消息必须携带 | N |

- 示例

{"notification":{"action":0.0,"staytime":0.0,"location":"UqdL5tMU4Vy9kio","relationId":"47eF","pictures":[],"status":1},"payload":{"targetHeight":1.8,"peopleFallingDownStatus":"fallingDown","targetId":0,"backgroundImage":{"pictureResolution":{"width":1,"height":1},"filePathType":"URL","filePath":"undefined","uploaded":true},"targetPosition":{"x":50.1,"y":49.1},"radarRelatedVideoResource":[]},"basic":{"dateTime":"2021-01-28T02:00:00.000+08:00","macAddress":"0C-9D-92-99-DD-31","ipV4Address":"10.65.101.171","ipV6Address":"fe80::4883:315d:e4c:75bc","UUID":"079f23cd-0988-459f-96f5-fa1c507dd07c"}}