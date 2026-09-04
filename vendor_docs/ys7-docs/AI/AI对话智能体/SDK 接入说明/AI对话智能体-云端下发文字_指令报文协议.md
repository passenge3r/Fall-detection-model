# AI对话智能体-云端下发文字/指令报文协议

> 更新时间: 2026-06-25T16:36:42.000+08:00

> 文档ID: 5273 | 来源树: AI

---

# 云端下发文字/指令报文协议

通过 ERTC SDK 的 `sendCustomMsg` / `onRecvCustomMsg` 自定义信令通道传输，JSON 格式。

---

# 前提

请参考文档：<https://open.ys7.com/help/4952>集成ERTC SDK

# 云端 → 设备端（下行消息）

## 1. ASR 识别文本推送

用户说话时，ASR 流式识别结果实时下发给设备端。

- **cmdType**: `READ`
- **data.type**: `1`（用户语音识别）

```
{
  "cmdType": "READ",
  "requestId": "264b8458-2445-4439-bbf5-364761569800",
  "textId": "a4412043e0324663be15c055f86a46fb",
  "data": {
    "text": "调试音频",
    "type": 1,
    "finished": false,
    "command": null
  }
}
```

**流式推送过程示例：**

```
{"cmdType":"READ","data":{"text":"","type":1,"finished":false,"command":null},...}
{"cmdType":"READ","data":{"text":"调","type":1,"finished":false,"command":null},...}
{"cmdType":"READ","data":{"text":"调试","type":1,"finished":false,"command":null},...}
{"cmdType":"READ","data":{"text":"调试音频","type":1,"finished":false,"command":null},...}
{"cmdType":"READ","data":{"text":"调试音频","type":1,"finished":true,"command":null},...}
```

> 注意：`text` 为累积文本（非增量），每条都是当前完整识别结果。`finished=true` 表示用户本句话说完。

---

## 2. 云端回复文本推送

云端大模型生成的文字回复（对应 TTS 语音内容的文字版），流式推送。

- **cmdType**: `READ`
- **data.type**: `2`（系统/大模型回复）

```
{
  "cmdType": "READ",
  "requestId": "264b8458-2445-4439-bbf5-364761569800",
  "textId": "a4412043e0324663be15c055f86a46fb",
  "data": {
    "text": "好的，我来帮您调试音频。",
    "type": 2,
    "finished": true,
    "command": null
  }
}
```

---

## 3. 指令下发

大模型从用户语音中提取出设备控制指令时下发。

- **cmdType**: `COMMAND`
- **data.type**: `2`（系统指令）

```
{
  "cmdType": "COMMAND",
  "requestId": "264b8458-2445-4439-bbf5-364761569800",
  "textId": "a4412043e0324663be15c055f86a46fb",
  "data": {
    "text": null,
    "type": 2,
    "finished": true,
    "command": "[{\"name\":\"cook_niunaiyanmaizhou\",\"params\":{}}]"
  }
}
```

**command 字段格式（JSON 数组字符串）：**

```
[
  {
    "name": "cook_niunaiyanmaizhou",
    "params": {}
  }
]
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | String | 指令名称 |
| `params` | Object | 指令参数（键值对） |