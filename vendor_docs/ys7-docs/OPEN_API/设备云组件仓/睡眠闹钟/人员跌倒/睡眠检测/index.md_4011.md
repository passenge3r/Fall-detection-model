# index.md

> 更新时间: 2026-05-25T16:43:34.000+08:00

> 文档ID: 4011 | 来源树: OPEN_API

---

## 【消息】｛｛name｝｝（ScheduledDataReporting）

- 事件标识

ScheduledDataReporting

- 消息类型

OTAP消息（ys.iot）

- 消息体（）

| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| 字段名 | 名称 | 数据类型 | 范围 | 描述 | 是否必填 |
| -- | -- | -- | -- | -- | -- |
| basic.basic | null | object |  | 事件基础信息，所有事件都必须携带，不可修改 | N |

- 示例

{"basic":{"dateTime":"167ASPYmFihx5oIFQCAhrchdf2","macAddress":"PPssskIdqmhrCanTyqeT1QmTPsk0jtdYMSDOe","ipV4Address":"bnDL5aYsNqhVbZ0fbaQwipGoX","ipV6Address":"XkszCT26CKZm0nraokQxWkZfFaiiBmHvlLcxZQqDdtT1SD","continue":false,"UUID":"K3i5b7XDVlGXJyQcLvipDpEqkRSm8wkrdOhTodFQoI"},"telemeter":{"values":{"PVMin":49,"DevTime":47,"MotionDetect":34,"StdBreatheRate":25,"PVMean":60,"UpFlag":6,"AvgBreatheAmp":14,"DevBreatheAmp":1,"A1":50,"PVMax":22,"A2":0,"A3":37,"PNum":5,"A4":7,"A5":28,"AvgBreatheRate":16,"MoveValue":6,"BodyDetct":0,"SlpFlag":8},"tags":{}}}