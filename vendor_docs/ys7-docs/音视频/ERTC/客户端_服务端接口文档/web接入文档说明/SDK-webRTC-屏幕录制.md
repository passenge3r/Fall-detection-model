# SDK-webRTC-屏幕录制

> SDK-webRTC-屏幕录制

> 更新时间: 2026-05-25T16:36:37.000+08:00

> 文档ID: 2853 | 来源树: 音视频

---

# ERTC Web 开启屏幕录制

> 本教程基于 ERTC Web SDK 2.1.x 及以上版本

本章主要介绍如何在 ERTC Web SDK 实现屏幕录制功能。

### 功能说明

### 实现流程

1. “发布端”发起屏幕录制。

```
ertc.screenRecorderStart({
  accessToken: '',
  appId: '',
  roomId: '',
  userId: '',
  onSafari: (next) => {
    // 如果是safari会进入此逻辑,需要和用户交互后，再执行next方法
    Modal.confirm({
      title: "提示",
      content: "请点击确定按钮，开始录屏",
      onOk() {
        next();
      },
    })
  }
})
.then((res) => {
  if (res?.code === 0) {
    // 执行成功，调用云端录制接口，进行真实录制
    // .....
  }
})
.catch((err) => {
  // 错误捕获
});
```

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| accessToken | 资源 token | 由开发者云办法给终端使用，可参考<https://open.ys7.com/help/1873> | string | at.d8yfi7bb1d1p5aw7v8oztfdsa1djra0n46-5mnfk598bc-0annlcz-a3gi2pj | 是 |
| appId | 应用 id | 您可以在 [控制台实时音视频](https://open.ys7.com/console/rtc/projectManage.html) 中找到您的 appId，如果没有，则单击“创建项目”按钮创建一个新的应用 | string | ebadss8529d954813214d3cb4192d3c781 | 是 |
| roomId | 房间 id | 字符串类型的房间号（如果当前已通过enterRoom加入房间，应与当前房间号区分） | string | "12345" | 是 |
| userId | 用户 id | 即用户名，只允许包含大小写英文字母（a-z、A-Z）、数字（0-9）及下划线和连词符。注意 ERTC 不支持同一个 userId 在两台不同的设备上同时进入房间，否则会相互干扰。 | string | "112233" | 是 |
| onSafari | 如果api调用环境为safari浏览器，需在onSafari中回调中与用户进行交互，用户确认后执行next，才能唤醒屏幕采集 | function | (next: function) => void() | 否 |  |

2. “发布端”停止屏幕录制

```
使用 ertc.screenRecorderStop 停止屏幕共享
```