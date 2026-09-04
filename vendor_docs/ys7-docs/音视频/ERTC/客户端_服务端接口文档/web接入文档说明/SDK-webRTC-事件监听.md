# SDK-webRTC-事件监听

> SDK-webRTC-事件监听

> 更新时间: 2026-05-25T16:36:35.000+08:00

> 文档ID: 1904 | 来源树: 音视频

---

# ERTC Web 事件监听

> 本教程基于 ERTC Web SDK 2.x 版本

通过 ertc.on()、ertc.once() 来监听指定事件。您可以通过这些事件实现管理房间用户列表，以及管理用户的流状态，感知网络状态等功能，下面是事件的详细介绍。

> 事件需要在事件触发之前监听，这样才能收到相应的事件通知，因此建议在 ertc 进房前完成事件监听，这样才能确保不会漏掉事件通知。

### 可监听的事件列表

#### webscoket 返回 error 消息

```
ertc.on(ERTC.EVENT.ERROR, (msg) => {
  console.log(msg)
})
```

#### websocket 连接状态变化

```
ertc.on(ERTC.EVENT.CONNECT_STATE_CHANGE, (msg) => {
  if (msg.code === 0) {
    // sdk连接成功
  } else if (msg.msg === "reconnecting") {
    //sdk正在重连中
  } else if (msg.msg === "fail") {
    // sdk连接失败
  } else if (msg.msg === "destroyed") {
    // sdk连接断开
  }
})
```

#### 其他用户加入房间

```
ertc.on(ERTC.EVENT.CLIENTJOIN, (msg) => {
  // msg.customId 对应用户 userId
  console.log(msg)
})
```

#### 其他用户离开房间

```
ertc.on(ERTC.EVENT.CLIENTLEAVE, (msg) => {
  // msg.customId 对应用户 userId
  console.log(msg.customId)
})
```

#### 其他用户发布流

```
ertc.on(ERTC.EVENT.STREAM_ADDED, (msg) => {
  // 订阅
  ertc
    .subscribeStream({ userId: msg.customId, type: msg.streamtype, view: domId })
    .then((res) => {
      // ...
    })
    .catch((err) => {
      // ...
    });
})
```

#### 其他用户发布流删除

```
ertc.on(ERTC.EVENT.STREAM_REMOVED, (msg) => {
  // msg.customId 对应用户 userId
  console.log(msg.customId, msg.streamType)
})
```

#### 本地流获取

```
ertc.on(ERTC.EVENT.LOCAL_STREAM_AVAILABLE, ({ stream, streamType }) => {
  ertc.playStream({
      domId: 'xxx',
      stream: stream,
    })
    .then((info) => {
      console.log("获取到本地流");
    });
})
```

#### 自身网络质量变化

```
ertc.on(ERTC.EVENT.REPORT_NETWORK_QUALITY, (msg) => {
  console.log(msg.uplink) // 上行网络（质量、抖动、延时、丢包）
  console.log(msg.downlink) // 下行网络
})
 // 网络质量评分 1:优 2: 良 3: 中 4: 差 5: 极差 6: 不可用 0: 未知
```

#### 房间内其他用户网络质量通知

```
ertc.on(ERTC.EVENT.ENTERROOMACK, ({ customId, upquality, downquality }) => {
  // customId 用户网络质量变动触发
 // 网络质量评分 1:优 2: 良 3: 中 4: 差 5: 极差 6: 不可用 0: 未知
})
```

#### 房间内音量变化

```
ertc.on(ERTC.EVENT.AUDIOLEVEL, (msg) => {
  msg.clientList.forEach(({ customId, audioleve }) => {
    // 匹配用户id，显示对应音量大小 0 - 100
  });
})
```

#### 远端视频旋转角度

```
ertc.on(ERTC.EVENT.VIDEO_ROTATION, ({ customId, rotate }) => {
  // customId 对应 userID
  // rotate 视频旋转角度
})
```

#### 房间内用户推流权限变化

```
ertc.on(ERTC.EVENT.CLIENT_PERMISSION, ({ customId, audioPermission, videoPermission, sharePermission }) => {
  // customId 对应 userID
  // permission{Number} 开启：1，关闭：0
  if (customId === 当前用户Id) {
    if (audioPermission === 0) {
      // 被静音
    }
    if (videoPermission === 0) {
      // 被关闭摄像头
    }
    if (sharePermission === 0) {
      // 被关闭屏幕共享
    }
  }
})
```