# SDK-webRTC-API概览

> SDK-webRTC-API概览

> 更新时间: 2026-05-25T16:36:34.000+08:00

> 文档ID: 1902 | 来源树: 音视频

---

# ERTC Web API 概览

> 本教程基于 ERTC Web SDK 2.x 版本

### 浏览器兼容性

ERTC Web SDK 基于 WebRTC 实现，目前在浏览器各端的支持如下，部分功能的兼容性如有不同，会在功能详情中特殊说明：

|  | chrome | firefox | edge | safari | opera |
| --- | --- | --- | --- | --- | --- |
| windows | 72 | 80 | 80 | - | 90 |
| mac | 72 | 99 | 80 | 14.1.1 | 90 |

### 静态属性

| 属性 | 描述 | 类型 | 数值 | 版本支持 |
| --- | --- | --- | --- | --- |
| STREAM\_TYPE | 流类型枚举 | Object | {  VIDEO\_ONLY: 1, // 视频大流  AUDIO\_ONLY: 2, // 音频流  VIDEO\_SIMULCAST\_LITTLE: 4, // 视频小流  SCREEN: 8, // 屏幕共享流  } | - |
| EVENT | 事件列表 | Object | {  CONNECT\_STATE\_CHANGE: 'CONNECT\_STATE\_CHANGE', // websocket连接状态变化  USERS\_CHANGE: "USERS\_CHANGE", // 用户列表变化  LOCAL\_STREAM\_AVAILABLE: "EVENT\_LOCAL\_STREAM\_AVAILABLE", // 本地流可用通知  REMOTE\_STREAM\_AVAILABLE: "EVENT\_REMOTE\_STREAM\_AVAILABLE", // 远端流可用通知  REPORT\_NETWORK\_QUALITY: "REPORT\_NETWORK\_QUALITY", // 当前用户网络质量上报通知（每2s上报一次）  ERROR: "error", // 错误上报  VIDEO\_ROTATION: "video-rotation", // 远端视频旋转角度变化通知  AUDIOLEVEL: "audioleve", // 房间内音量变化通知  ENTERROOMACK: "enterRoomack", // 当前用户加入房间结果通知  EXITROOMACK: "exitRoomack", // 当前用户退出房间结果通知  CLIENTJOIN: "clientJoin", // 房间内新加入用户通知  CLIENTLEAVE: "clientLeave", // 房间内用户离开通知  STREAM\_ADDED: "stream-added", // 其他用户推流通知  STREAM\_REMOVED: "stream-removed", // 其他用户停止推流通知  PUBLISHSCREENSTREAMACK: "publishscreenstreamack", // 屏幕共享流发布结果通知  NETWORKQUALITY: "networkquality", // 其他用户网络质量变化通知  CLIENT\_PERMISSION: "client-permission", // 房间内所有用户发布权限变化通知  SUB\_PERMISSION: "sub-permission", // 当前用户订阅权限变化通知  PUBLISHLOCALSTREAMACK: "publishlocalstreamack", // 当前用户推流结果通知  UNPUBLISHLOCALSTREAMACK: "unpublishlocalstreamack", // 当前用户取消推流结果通知  SUBREMOTEACK: "subremoteack", // 订阅结果通知  UNSUBREMOTEACK: "unsubremoteack", // 取消订阅结果通知   } | - |

### 实例方法

| API | 描述 | 入参 | 返回 | 版本支持 |
| --- | --- | --- | --- | --- |
| enterRoom | 进入一个音视频通话房间 | { accessToken, appId, roomId, userId } | Promise | - |
| leaveRoom | 退出当前房间 | - | Promise | - |
| startLocalAudio | 开启本地麦克风采集，并发布到当前的房间中 | - | Promise | - |
| stopLocalAudio | 停止本地麦克风的采集与发布 | - | Promise | - |
| pauseLocalAudio | 暂停本地麦克风的采集与发布 | - | Promise | - |
| resumeLocalAudio | 恢复本地麦克风的采集与发布 | - | Promise | - |
| startLocalVideo | 开启本地摄像头采集，并发布到当前的房间中 | - | Promise | - |
| stopLocalVideo | 停止本地摄像头采集与发布 | - | Promise | - |
| pauseLocalVideo | 暂停本地摄像头采集与发布 | - | Promise | - |
| resumeLocalVideo | 恢复本地摄像头采集与发布 | - | Promise | - |
| startScreenShare | 开启屏幕共享，并发布到当前的房间中 | - | Promise | - |
| stopScreenShare | 停止屏幕共享与发布 | - | Promise | - |
| subscribeStream | 订阅远端流 | { userId, type, elementId } | Promise | - |
| unsubscribe | 取消订阅远端流 | { userId, type } | Promise | - |
| pausePullPeerStream | 暂停订阅 | { userId, type } | Promise | - |
| resumePullPeerStream | 恢复订阅 | { userId, type } | Promise | - |
| setProfile | 设置音视频参数（frameRate 与 bitrate 对屏幕共享流同样生效） | { cameraId, microphoneId, width, height, frameRate, bitrate, simulcast } | - | - |
| on | 监听 ERTC 事件 | - | - | - |
| once | 监听 ERTC 事件（单次执行后取消监听） | - | - | - |
| remove | 取消事件监听 | - | - | - |
| getVersion | 获取 npm 版本号 | - | Promise | - |
| getCamerasList | 获取摄像头列表（在用户未授权摄像头或麦克风访问权限前，获取可能为空， 因此建议在用户授权访问后再调用该接口获取设备详情。） | - | Promise | - |
| getMicrophonesList | 获取麦克风列表 | - | Promise | - |
| getSpeakersList | 获取扬声器列表 | - | Promise | - |
| isSupported | 获取浏览器支持情况（H264，媒体采集，当前域名是否合法） | - | Promise | 2.1.0 |
| getCameraPermission | 获取摄像头权限 | - | Promise | 2.1.0 |
| getMicrophonePermission | 获取麦克风权限 | - | Promise | 2.1.0 |