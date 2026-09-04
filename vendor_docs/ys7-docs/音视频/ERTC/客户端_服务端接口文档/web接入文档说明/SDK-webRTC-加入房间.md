# SDK-webRTC-加入房间

> SDK-webRTC-加入房间

> 更新时间: 2026-05-25T16:36:34.000+08:00

> 文档ID: 1903 | 来源树: 音视频

---

# ERTC Web 加入房间

> 本教程基于 ERTC Web SDK 2.x 版本

本章主要介绍如何进入 ERTC 房间中，只有在进入音视频房间后，用户才能订阅房间中其他用户的音视频流，或者向房间中的其他用户发布自己的音视频流。

### 实现音视频通话基本逻辑

- 调用 new ERTC() 方法创建 ertc 对象。
- 调用 ertc.enterRoom() 方法进入房间。
- 在进入房间后，可以开启摄像头和麦克风并发布到房间。
  - 调用 ertc.startLocalVideo() 开启摄像头并发布到房间。
  - 调用 ertc.startLocalAudio() 开启麦克风并发布到房间。
- 当一个远端用户发布了音视频后，您需要通过如下方式来播放远端视频：
  - 在进房前监听 ERTC.EVENT.REMOTE\_STREAM\_AVAILABLE 事件， 就能收到所有远端用户的发布视频事件。
  - 在事件回调函数中，调用 ertc.subscribeStream() 方法订阅远端视频。

### 步骤 1：创建 ERTC 实例对象

ERTC 类的实例代表一个本地客户端。ERTC 的对象方法提供了加入通话房间、预览本地摄像头、发布本地摄像头和麦克风、播放远端音视频等功能。
调用 new ERTC() 方法创建 ERTC 对象，关键参数：

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 | 默认值 |
| --- | --- | --- | --- | --- | --- | --- |
| debug | 是否在控制台打印日志 | 一般开发环境用来帮助定位问题 | boolean | false | 否 | false |
| logsExport | 是否支持日志导出 | 依赖debug参数为true，开关开启后，会默认收集最大500kb的日志，可通过window.ERTC\_WEB.exportLogs()进行导出txt文件 | boolean | false | 否 | false |
| domain | 自定义接口请求域名 | 服务非私有化部署，不需要配置 | string | https://open.ys7.com | 否 | false |

```
import ERTC from 'ertc-web'

const ertc = new ERTC()
```

### 步骤 2：加入房间

调用 ertc.enterRoom() 方法进入房间。通常在开始通话按钮的点击回调里进行调用。关键参数：

| 参数 | 参数含义 | 补充说明 | 数据类型 | 示例 | 是否必填 |
| --- | --- | --- | --- | --- | --- |
| accessToken | 资源token | 由开发者云办法给终端使用，可参考<https://open.ys7.com/help/1873> | string | at.d8yfi7bb1d1p5aw7v8oztfdsa1djra0n46-5mnfk598bc-0annlcz-a3gi2pj | 是 |
| appId | 应用id | 您可以在 [控制台实时音视频](https://open.ys7.com/console/rtc/projectManage.html) 中找到您的 appId，如果没有，则单击“创建项目”按钮创建一个新的应用 | string | ebadss8529d954813214d3cb4192d3c781 | 是 |
| roomId | 房间id | 字符串类型的房间号 | string | "12345" | 是 |
| userId | 用户id | 即用户名，只允许包含大小写英文字母（a-z、A-Z）、数字（0-9）及下划线和连词符。注意 ERTC 不支持同一个 userId 在两台不同的设备上同时进入房间，否则会相互干扰。 | string | "112233" | 是 |

```
try {
  const res = await ertc.enterRoom({ accessToken,  appId, roomId, userId });
  if (res.code === 0) {
    console.log('进房成功');
  } else {
    throw new Error(res.message)
  }
} catch (error) {
  console.error('进房失败 ' + error);
}
```