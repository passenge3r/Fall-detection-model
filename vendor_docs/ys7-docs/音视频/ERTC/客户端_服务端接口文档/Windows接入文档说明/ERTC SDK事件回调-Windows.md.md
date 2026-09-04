# ERTC SDK事件回调-Windows.md

> 更新时间: 2026-05-25T16:36:30.000+08:00

> 文档ID: 1918 | 来源树: 音视频

---

# ERTC 各种事件回调

#### Updated Time 2023/08/30

## ERtcCallback简介

ERtcCallback是ERTCEngine对应的回调事件，您可以通过此回调，来监听自己感兴趣的回调事件

### 回调事件概览

| API | 描述 |
| --- | --- |
| 错误码回调 |  |
| onError | 错误码回调 |
| 房间相关事件回调 |  |
| onEnterRoomSuccess | 本地用户成功加入房间 |
| onExitRoom | 离开房间的事件 |
| 用户相关事件回调 |  |
| onRemoteUserEnterRoom | 远端用户成功加入房间 |
| onRemoteUserLeaveRoom | 远端用户退出房间 |
| 音视频相关回调 |  |
| onUserVideoAvailable | 远端用户打开或关闭视频流的回调 |
| onUserAudioAvailable | 远端用户推流或关闭音频流的回调 |
| onUserSubStreamAvailable | 远端用户开启或关闭屏幕共享的回调 |
| onFirstLocalVideoFrame | 本地视频预览回调 |
| onFirstRemoteVideoFrame | 远端视频预览回调 |
| onScreenCaptureStarted | 屏幕分享开启的事件回调 |
| onUserVoiceVolume | 音量回调 |
| 网络和技术指标统计回调 |  |
| onNetworkQuality | 网络质量回调 |
| onLocalVideoStats | 本地视频实时数据回调 |
| onLocalAudioStats | 本地音频实时数据回调 |
| onRemoteAudioStats | 远端音频实时数据回调 |
| onRemoteVideoStats | 远端视频实时数据回调 |
| onSpeedTestResult | 网络测速结果回调 |
| 自定义消息的接收事件回调 |  |
| onRecvCustomMsg | 收到自定义消息的事件回调 |

### 回调事件详情

### onError

房间内各种错误码回调

`virtual void onError(int errCode, const char* msg) {};`

### onEnterRoomSuccess

用户加入房间成功，加入房间成功后将收到回调

`virtual void onEnterRoomSuccess() {};`

说明：result 加入房间耗时

### onExitRoom

用户退出房间，非主动退出房间才会收到该回调

`virtual void onExitRoom(int reason) {};`

说明：reason 退出房间原因

### onRemoteUserEnterRoom

远端用户进入房间成功回调，进入房间时将会收到所有已在房间内用户加入房间的回调

`virtual void onRemoteUserEnterRoom(const char* userId) {};`

说明：userId 用户id

### onRemoteUserLeaveRoom

远端用户离开房间

`virtual void onRemoteUserLeaveRoom(const char* userId, int reason) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*|用户ID|
|reason|int|0表示用户主动退出房间，1表示用户超时退出|

### onUserVideoAvailable

远端用户打开或关闭视频流的回调

`virtual void onUserVideoAvailable(const char* userId, bool available) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*|用户ID|
|available|bool|available true-视频可用 false-视频不可用|

### onUserAudioAvailable

远端用户推流或关闭音频流的回调

`virtual void onUserAudioAvailable(const char* userId, bool available) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*|用户ID|
|available|bool|available true-音频可用 false-音频不可用|

### onUserSubStreamAvailable

远端用户开启或关闭屏幕共享的回调

`virtual void onUserSubStreamAvailable(const char* userId, int available) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*|用户ID|
|available|int|available 1-开启屏幕共享 0-关闭屏幕共享|

### onFirstLocalVideoFrame

本地视频预览回调

`virtual void onFirstLocalVideoFrame(const int width, const int height) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|width|int|视频宽度，单位像素|
|height|int| 视频高度，单位像素|

### onFirstRemoteVideoFrame

远端视频预览回调，订阅视频后将会收到该回调

`virtual void onFirstRemoteVideoFrame(const char* userId, const int width, const int height) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*|用户ID|
|width|int|视频宽度，单位像素|
|height|int| 视频高度，单位像素|

### onUserVoiceVolume

音量回调，用户需要调用 enableAudioVolumeEvaluation 开启才会产生回调

`virtual void onUserVoiceVolume(ERTCVolumeInfo* userVolumes, uint32_t userVolumesCount, uint32_t totalVolume) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userVolumes|ERTCVolumeInfo\*|列表，最多返回音量最大的三个用户|
|userVolumesCount|uint32\_t|userVolumes数组中个数|
|totalVolume|uint32\_t| 所有远端用户的总音量大小|

### onNetworkQuality

网络质量回调

`virtual void onNetworkQuality(const char* userId, int upQuality) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\*| userId 用户id, 当id为自己的userId时，表示本地网络质量，否则表示其它用户的|
|upQuality|int |上行网络质量|

### onRecvCustomMsg

当房间中的某个用户使用 {sendCustomMsg} 发送自定义 消息时，房间中的其它用户可以通过 onUserCustomMsg 事件回调接收到该条消息。

`virtual void onRecvCustomMsg(const char* userId, const uint8_t* message, uint32_t messageSize) {};`

参数列表如下
| 参数 |类型| 含义|
|:-----------|:----|:----|
|userId|const char\* |用户ID|
|message|uint8\_t\*| 消息数据|
|messageSize|uint32\_t| 消息数据大小|

### onLocalVideoStats

本地视频实时数据

`virtual void onLocalVideoStats(const ERTCLocalVideoStats* stats) {};`

说明：stats 本地视频相关数据

### onRemoteVideoStats

远端视频实时数据

`virtual void onRemoteVideoStats(const ERTCRemoteVideoStats* stats) {};`

说明：stats 远端视频相关数据

### onLocalAudioStats

本地音频实时数据

`virtual void onLocalAudioStats(const ERTCLocalAudioStats* stats) {};`

说明：stats 本地音频相关数据

### onRemoteAudioStats

远端视频实时数据

`virtual void onRemoteAudioStats(const ERTCRemoteAudioStats* stats) {};`

说明：stats 远端音频相关数据

### onSpeedTestResult

网络测速结果

`virtual void onSpeedTestResult(const ERTCSpeedTestResult* result) {};`

说明：result 测速结果