# SDK-webRTC-开启屏幕共享

> SDK-webRTC-开启屏幕共享

> 更新时间: 2026-05-25T16:36:35.000+08:00

> 文档ID: 1909 | 来源树: 音视频

---

# ERTC Web 开启屏幕共享

> 本教程基于 ERTC Web SDK 2.x 版本

本章主要介绍如何在 ERTC Web SDK 实现屏幕分享功能。

### 实现流程

1. “发布端”开启屏幕分享。

```
ertc.startScreenShare()
```

2. “订阅端”播放屏幕分享。

```
// 监听 EVENT.STREAM_ADDED 事件，记录有远端音频的 userId 和 streamType
ertc.on(ERTC.EVENT.STREAM_ADDED, (msg) => {
  // 订阅屏幕共享流
  if([ERTC.STREAM_TYPE.SCREEN].includes(msg.streamtype)) {
    ertc
      .subscribeStream({ userId: msg.customId, type: msg.streamtype })
      .then((res) => {
        console.log(`自动订阅成功，用户：${msg.customId}，流类型：${msg.streamtype}`),
      })
      .catch((err) => {
        console.log(`自动订阅失败，用户：${msg.customId}，流类型：${msg.streamtype}，原因：${json(err)}`)
      });
  }
});

// 获取屏幕流并播放
ertc.on(ERTC.EVENT.REMOTE_STREAM_AVAILABLE, (msg) => {
  <!-- 判断屏幕共享流 -->
  if (msg.streamType === ERTC.STREAM_TYPE.SCREEN) {
    ertc
      .playStream({ domId: `${userId}-dom`, stream: msg.stream })
      .then((info) => {
        console.log(`获取到${msg.userId}的远端音视频流`)
      });
  }
})
```

3. “发布端”停止屏幕共享

```
使用 ertc.stopScreenShare 停止屏幕共享
```