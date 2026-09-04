# SDK-webRTC-音频变声

> SDK-webRTC-音频变声

> 更新时间: 2026-05-25T16:36:36.000+08:00

> 文档ID: 2855 | 来源树: 音视频

---

# ERTC Web 音频变声

> 本教程基于 ERTC Web SDK 2.1.x 版本

在社交娱乐行业的互动场景中，常常伴随着变声功能的需求。本章介绍了如何使用ERTC的变声能力，实现发送端声音改变。

### 兼容性

|  | chrome | firefox | edge | safari | opera |
| --- | --- | --- | --- | --- | --- |
| windows | 72 | 80 | 80 | - | 90 |
| mac | 72 | 99 | 80 | 14.1.1 | 90 |

### 步骤 1：加入房间

可以参考文档 加入房间

### 步骤 2：设置变声

```
await ertc.setVoiceChangeConfig({ pluginStatus: "on" });
```

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 | 默认值 |
| --- | --- | --- | --- | --- | --- | --- |
| pluginStatus | 是否开启变声 | 一般在麦克风开启前设置，如果在通话中，会自动断开后重新推流造成短暂延迟 | string | on | 否 | off |
| voiceType | 变声类型 | 大叔音（1）、小丑音（2） | number | 1 | 否 | - |

### 步骤 3：开启麦克风

```
await ertc.startLocalAudio();
```