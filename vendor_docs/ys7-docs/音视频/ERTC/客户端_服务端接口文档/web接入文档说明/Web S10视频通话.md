# Web S10视频通话

> Web S10视频通话

> 更新时间: 2026-05-25T16:36:37.000+08:00

> 文档ID: 4489 | 来源树: 音视频

---

# 屏类摄像头 ERTC视频通话 web SDK 接入引导

> 本教程基于 ertc-web-call SDK 1.x 版本

视频通话功能是萤石屏类设备（比如 S10/RK3 等）产品中的一项重要功能，旨在为用户提供便捷的远程视频通话体验。用户可以web端与摄像头等设备进行实时的视频对话。

## 快速接入方案

S10/RK3等屏类摄像机接入教程，可以参考整体接入实践说明：<https://open.ys7.com/help/4332>

其中API接口及整体流程，可以参考文档进行接入

## Demo使用

线上测试Demo参考：[前往查看](https://openstatic.ys7.com/webrtc_gw_websdk/#/call)

## 快速接入

### 1. 您可以在项目中使用 `npm` 安装 `ertc-web-call`。

```
npm install ertc-web-call
```

### 2. 在项目中引入

```
import ERTCCall from 'ertc-web-call'

const ertcCall = new ERTCCall()
```

### 3. 监听事件

```
// xxx.html
<div>
  <video id="remote-element"></video>
  <video id="local-element"></video>
</div>

// xxx.js

/**
* SDK事件监听
*/
// 监听设备媒体流
ertcCall.on(ERTCCall.EVENT.REMOTE_STREAM_AVAILABLE, ({ streamtype, stream }) => {
  console.log("获取到远端媒体流");
  if ([ERTCCall.STREAM_TYPE.AUDIO_ONLY, ERTCCall.STREAM_TYPE.VIDEO_ONLY].includes(streamtype)) {
    ERTCCall.attachMediaStream("#remote-element", stream);
  }
});

// 监听本地媒体流
ertcCall.on(ERTCCall.EVENT.LOCAL_STREAM_AVAILABLE, ({ streamtype, stream }) => {
  console.log("获取到本地媒体流");
  if (streamtype === ERTCCall.STREAM_TYPE.VIDEO_ONLY) {
    ERTCCall.attachMediaStream("#local-element", stream);
  }
});

// 监听呼叫状态变化
ertcCall.on(ERTCCALL.EVENT.STATUS_CHANGE, (status) => {
  console.log("状态改变", status); // init：未呼叫，calling：正在呼叫中，talking：通话中
  // 更改业务层状态展示
})

// 监听呼叫超时
ertcCall.on(ERTCCALL.EVENT.CALL_TIMEOUT, () => {
  console.log("呼叫超时");
  // 执行业务层逻辑
})


/**
* 业务层设备推送的webhook消息接收
*/
// 设备拒接、设备忙线被占用
callback = () => {
  // callback只是示例代码，指代设备拒接的回调函数，并非sdk内部函数

  ertcCall.reset() // sdk感知不到设备的拒绝和忙线，所以需要在此处重置sdk的呼叫状态
}
```

### 4. 发起呼叫

客户端（web）往web端主动发起呼叫，可能存在拒接、超时的情况。拒接需要通过客户服务端返回，超时默认20000ms，可在事件中监听超时。

```
const initParams = {
  accessToken: "",
  appId: "",
  account: "",
  deviceSerial: "",
  strRoomId: "",
  resourceToken: "",
  deviceResourceToken: "",
  timeout: '',
}

ertcCall.makeCall(initParams).then((res) => {
    message.success("呼叫发起成功");
    console.log("呼叫发起成功:", res);
  }).catch((err) => {
    message.error(`呼叫发起失败`);
    console.log("呼叫发起失败:", err);
  });
```

  

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| accessToken | 开放平台应用鉴权凭证 | 需要在 开放平台控制台 创建实时音视频项目，对应创建的项目 id | string | at.xxxxxxxxxxxx-xxxxxxxxxx-xxxxxxx-a3gi2pj | 是 |
| appId | 应用 id | 您可以在[控制台实时音视频](https://open.ys7.com/console/rtc/projectManage.html) 中找到您的 appId，如果没有，则单击“创建项目”按钮创建一个新的应用 | string | ebadss852xxxxxxxxxxxxxxcb4192d3c781 | 是 |
| account | 用户id | 视频通话用户id/用户名，避免重复，由客户服务端管理生成并传给web | string | "112233" | 是 |
| deviceSerial | 设备序列号 | - | string | - | 是 |
| strRoomId | 房间 id | roomId/房间号/会议ID，视频通话房间号，由客户服务端管理生成并传给web | string | - | 是 |
| resourceToken | 用户资源token | 用于客户端(web)入会权限校验，不是accessToken，由客户服务端管理生成并传给web，参考Java SDK生成：<https://open.ys7.com/help/1873> | string | - | 是 |
| deviceResourceToken | 设备资源token | 服务端使用，用于邀请设备入会，并做权限校验，不是accessToken，由客户服务端管理生成并传给web，参考Java SDK生成：<https://open.ys7.com/help/1873> | string | - | 是 |
| timeout | 呼叫超时时间 | 一般通过接口查询设备超时时间，获取后进行设置，不传则默认20秒 | number | 20000 | 否 |

### 5. 取消呼叫

在呼叫接口发起，到设备端接听/拒接的过程中，可以通过取消呼叫来主动结束呼叫。

```
const initParams = {
  accessToken: "",
  appId: "",
  account: "",
  deviceSerial: "",
  strRoomId: "",
  resourceToken: "",
  deviceResourceToken: "",
}
ertcCall.cancleCall(initParams).then(() => {
    console.log("取消呼叫成功");
  }).catch((err) => {
    console.log("取消呼叫发起失败", err);
  });
```

### 6. 接听

设备端往客户端（web）呼叫，客户服务端接收到通知后，将房间号传给客户端（web），生成 resourceToken 后，调用接听接口，加入房间，实现通话。

```
const initParams = {
  appId: "",
  account: "",
  strRoomId: "",
  resourceToken: "",
}
ertcCall.acceptCall({
    resourceToken,
    appId,
    strRoomId,
    account,
  })
  .then(() => {
    message.success("接听调用成功");
    console.log("🚀 ~ ERTCCALL ~ acceptCall ~ 接听调用成功");
  })
  .catch((err) => {
    message.error(`接听调用失败`);
    console.log("🚀 ~ ERTCCALL ~ acceptCall ~ 接听调用失败", err);
  });
```

### 7. 拒接

设备端往客户端（web）呼叫，客户端拒接。

```
const initParams = {
  accessToken: "",
  appId: "",
  account: "",
  deviceSerial: "",
  strRoomId: "",
  resourceToken: "",
}
ertcCall.rejectCall(initParams)
  .then((res) => {
    console.log("拒接成功");
  })
  .catch((err) => {
    console.log("拒接失败", err);
  });
```

### 8. 挂断

在通话通过中调用，主动挂断电话，双方退出房间。

```
ertcCall.hangup().then(() => {
    console.log("挂断成功");
  }).catch((err) => {
    console.log("挂断失败", err);
  });
```

### 9. 设置音视频参数

设置客户端（web）发送的音视频参数，包括音频参数、视频参数等。在发起呼叫之前调用才生效。

```
ertcCall.setProfile({
  cameraId, // 摄像头deviceId
  microphoneId, // 麦克风deviceId
  width, // 分辨率 宽
  height, // 分辨率 高
  frameRate, // 最大视频帧率
  bitrate, // 最大视频码率，单位：kbps
})
```