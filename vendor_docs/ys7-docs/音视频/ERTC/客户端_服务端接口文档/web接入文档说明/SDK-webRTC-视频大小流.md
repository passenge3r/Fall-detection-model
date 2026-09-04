# SDK-webRTC-视频大小流

> SDK-webRTC-视频大小流

> 更新时间: 2026-05-25T16:36:36.000+08:00

> 文档ID: 2854 | 来源树: 音视频

---

# ERTC Web 开启视频大小流

> 本教程基于 ERTC Web SDK 2.1.x 版本

### 兼容性

|  | chrome | firefox | edge | safari | opera |
| --- | --- | --- | --- | --- | --- |
| windows | 75 | ❌ | 80 | - | 90 |
| mac | 75 | ❌ | 80 | ❌ | 90 |

### 实现步骤

#### 步骤 1：设置大小流

```
const ertc = new ERTC()

ertc.setProfile({ simulcast: true // 是否开启大小流，参数设置需要在加入房间之前设置 })
```

#### 步骤 2：加入房间

可以参考文档 加入房间

#### 步骤 3：开启摄像头

```
await ertc.startLocalVideo();
```

#### 步骤 4：远端订阅小流

```
ertc.on(ERTC.EVENT.STREAM_ADDED, (msg) => {
  // 订阅视频小流
  if([ERTC.STREAM_TYPE.VIDEO_SIMULCAST_LITTLE].includes(msg.streamtype)) {
    ertc
      .subscribeStream({ userId: msg.customId, type: msg.streamtype, view: domId })
      .then((res) => {
        console.log(`自动订阅成功，用户：${msg.customId}，流类型：${msg.streamtype}`),
      })
      .catch((err) => {
        console.log(`自动订阅失败，用户：${msg.customId}，流类型：${msg.streamtype}`)
      });
  }
});
```

### 常见问题

1. 由于技术架构原因，目前火狐与safari浏览器尚不支持大小流的发布，预计在3.x版本进行完善修复。
2. 大小流的开启，需要在enterRoom api调用之前设置才会生效，如果入房后再设置，需要退出重新加入。