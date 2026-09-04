# SDK-webRTC-发布音视频流

> SDK-webRTC-发布音视频流

> 更新时间: 2026-05-25T16:36:34.000+08:00

> 文档ID: 1907 | 来源树: 音视频

---

# ERTC Web 发布音视频流

> 本教程基于 ERTC Web SDK 2.x 版本

本章主要介绍如何发布自己的音视频流，所谓“发布”，也就是打开麦克风和摄像头，让自己的声音和视频能够被房间中其他用户听到和看到。

### 步骤 1：加入房间

可以参考文档 加入房间

### 步骤 2：开启摄像头

调用 ertc.startLocalVideo() 方法开启摄像头，并发布到房间。

```
await ertc.startLocalVideo();
```

### 步骤 3：开启麦克风

```
await ertc.startLocalAudio();
```

### 步骤 4：本地播放

监听 EVENT.LOCAL\_STREAM\_AVAILABLE 事件，获取本地流对象

```
ertc.on(ERTC.EVENT.LOCAL_STREAM_AVAILABLE, (msg) => {
  <!-- 本地流获取的事件会被多次触发，建议只做流播放处理，不处理其他副作用逻辑 -->
  const domId = msg.streamType === ERTC.STREAM_TYPE.SCREEN ? "local-video-screen" : "local-video";

  ertc.playStream({ domId, stream: stream, }).then((info) => {
    console.log('本地播放')
  });
});
```

### 步骤 6：暂停恢复摄像头、麦克风

```
使用 ertc.pauseLocalVideo 暂停摄像头
使用 ertc.resumeLocalVideo 恢复摄像头
使用 ertc.pauseLocalAudio 暂停麦克风
使用 ertc.resumeLocalAudio 恢复麦克风
```

### 步骤 6：关闭摄像头、麦克风

```
使用 ertc.stopLocalVideo、ertc.stopLocalAudio 关闭摄像头和麦克风
```