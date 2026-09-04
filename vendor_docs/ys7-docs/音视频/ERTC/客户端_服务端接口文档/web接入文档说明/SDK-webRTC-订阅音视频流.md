# SDK-webRTC-订阅音视频流

> SDK-webRTC-订阅音视频流

> 更新时间: 2026-05-25T16:36:34.000+08:00

> 文档ID: 1910 | 来源树: 音视频

---

# ERTC Web 订阅音视频流

> 本教程基于 ERTC Web SDK 2.1.x 版本

本章主要介绍如何订阅房间中其他用户的音视频流，也就是如何播放其他用户的音频和视频。为了方便起见，我们在接下来的文档中，会将“房间中的其他用户”统称为“远端用户”。

### 步骤 1：加入房间

可以参考文档 加入房间

### 步骤 2：订阅视频流

监听 EVENT.STREAM\_ADDED 事件，记录有远端音频的 userId 和 streamType

```
ertc.on(ERTC.EVENT.STREAM_ADDED, (msg) => {
  // 订阅音频流、视频大流
  if([ERTC.STREAM_TYPE.VIDEO_ONLY, ERTC.STREAM_TYPE.AUDIO_ONLY].includes(msg.streamtype)) {
    ertc
      .subscribeStream({ userId: msg.customId, type: msg.streamtype, view: elementId })
      .then((res) => {
        console.log(`自动订阅成功，用户：${msg.customId}，流类型：${msg.streamtype}`),
      })
      .catch((err) => {
        console.log(`自动订阅失败，用户：${msg.customId}，流类型：${msg.streamtype}，原因：${json(err)}`)
      });
  }
});
```

### 步骤 3：取消订阅远端流

```
使用 ertc.unsubscribe({ userId, type }) 取消订阅用户的某个流
```