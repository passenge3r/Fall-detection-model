# index.md

> 更新时间: 2026-05-25T16:43:24.000+08:00

> 文档ID: 3881 | 来源树: OPEN_API

---

## 【消息】｛｛name｝｝（HumanMoveIn）

- 事件标识

HumanMoveIn

- 消息类型

OTAP消息（ys.iot）

- 消息体（）

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| -- | -- | -- | -- | -- | -- |
| notification.notification | 提醒消息 | object |  | 提醒消息基础字段，所有告警提醒类消息必须携带 | N |

- 示例

{"notification":{"action":0.0,"location":"2yNG1u450ZqMnbSfKCLEHPL3afRM2cWdPTVkuDv1","relationId":"bee0yGBHdsHvx81fg","pictures":[],"status":1},"basic":{"dateTime":"2021-01-28T02:00:00+08:00","macAddress":"0C-9D-92-99-DD-31","ipV4Address":"10.65.101.171","ipV6Address":"fe80::4883:315d:e4c:75bc","UUID":"079f23cd-0988-459f-96f5-fa1c507dd07c"}}