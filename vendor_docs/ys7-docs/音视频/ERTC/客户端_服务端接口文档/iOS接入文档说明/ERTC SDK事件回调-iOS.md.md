# ERTC SDK事件回调-iOS.md

> 事件回调信息描述

> 更新时间: 2026-05-25T16:36:33.000+08:00

> 文档ID: 1823 | 来源树: 音视频

---

# ERTC 各种事件回调

#### Updated Time 2023/08/30

## ERTCDelegate简介

ERTCDelegate是ERTCEngine对应的回调事件，您可以通过此回调，来监听自己感兴趣的回调事件

### 回调事件概览

| API | 描述 |
| --- | --- |
| 错误码回调 |  |
| onError | 错误码回调 |
| 加入房间回调 |  |
| onEnterRoomSuccess | 本地用户成功加入房间 |
| onRemoteUserEnterRoom | 远端用户成功加入房间 |
| remoteUserRejoinRoom | 远端用户重新加入房间回调 |
| 退出房间回调 |  |
| onExitRoom | 本地用户退出房间 |
| onRemoteUserLeaveRoom | 远端用户退出房间 |
| 音视频相关回调 |  |
| onUserVideoAvailable | 远端用户打开或关闭视频流的回调 |
| onUserAudioAvailable | 远端用户推流或关闭音频流的回调 |
| onUserScreenShareAvailable | 远端用户开启或关闭屏幕共享的回调 |
| onFirstLocalVideoFrameWithWidth | 本地视频预览回调 |
| onFirstRemoteVideoFrame | 远端视频预览回调 |
| onFirstScreenShareStream | 远端共享流回调 |
| onUserVoiceVolume | 音量回调 |
| onNetworkQualityWithUp | 网络质量回调 |
| onUserCustomMsg | 自定义消息回调 |
| onLocalVideoStats | 本地视频实时数据回调 |
| onLocalAudioStats | 本地音频实时数据回调 |
| onRemoteAudioStats | 远端音频实时数据回调 |
| onRemoteVideoStats | 远端视频实时数据回调 |
| onSpeedTestResult | 网络测速结果回调 |
| onDisplay | 远端视频解码回调 |
| onForceStopShareScreen | 强制停止屏幕共享回调 |

### 回调事件详情

### onError

房间内各种错误码回调

`- (void)onError:(NSInteger)errCode`

### onEnterRoomSuccess

用户加入房间成功，加入房间成功后将收到回调

`- (void)onEnterRoomSuccess:(NSInteger)result`

说明：result 加入房间耗时

### onExitRoom

用户退出房间，非主动退出房间才会收到该回调

`- (void)onExitRoom:(ERTCSelfExitReason)reason`

说明：reason 退出房间原因

### onRemoteUserEnterRoom

远端用户进入房间成功回调，进入房间时将会收到所有已在房间内用户加入房间的回调

`- (void)onRemoteUserEnterRoom:(NSString *)userId`

说明：userId 用户id

### onRemoteUserLeaveRoom

远端用户离开房间

`- (void)onRemoteUserLeaveRoom:(NSString *)userId reason:(NSInteger)reason`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| reason | NSInteger | 0表示用户主动退出房间，1表示用户超时退出 |

### onUserVideoAvailable

远端用户打开或关闭视频流的回调

`- (void)onUserVideoAvailable:(NSString *)userId available:(BOOL)available`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| available | BOOL | available true-视频可用 false-视频不可用 |

### onUserAudioAvailable

远端用户推流或关闭音频流的回调

`- (void)onUserAudioAvailable:(NSString *)userId available:(BOOL)available`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| available | BOOL | available true-音频可用 false-音频不可用 |

### onUserScreenShareAvailable

远端用户开启或关闭屏幕共享的回调

`- (void)onUserScreenShareAvailable:(NSString *)userId available:(BOOL)available`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| available | BOOL | available true-开启屏幕共享 false-关闭屏幕共享 |

### onFirstLocalVideoFrameWithWidth

本地视频预览回调

`- (void)onFirstLocalVideoFrameWithWidth:(int)width height:(int)height`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| width | int | 视频宽度，单位像素 |
| height | int | 视频高度，单位像素 |

### onFirstRemoteVideoFrame

远端视频预览回调，订阅视频后将会收到该回调

`- (void)onFirstRemoteVideoFrame:(NSString *)userId width:(int)width height:(int)height`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| width | int | 视频宽度，单位像素 |
| height | int | 视频高度，单位像素 |

### onFirstScreenShareStream

远端共享流回调,订阅屏幕共享后会收到该回调

`- (void)onFirstScreenShareStream:(int)width height:(int)height`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| width | int | 视频宽度，单位像素 |
| height | int | 视频高度，单位像素 |

### onUserVoiceVolume

音量回调，用户需要调用 enableAudioVolumeEvaluation 开启才会产生回调

`- (void)onUserVoiceVolume:(NSArray<ERTCVolumeInfo *> *)userVolumes totalVolume:(NSInteger)totalVolume`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userVolumes | NSArray<ERTCVolumeInfo \*> | 列表，最多返回音量最大的三个用户 |
| totalVolume | NSInteger | 混音后的整个会场音量大小 |

### onNetworkQualityWithUp

网络质量回调

`- (void)onNetworkQualityWithUp:(ERTCNetworkQuality)upQuality down:(ERTCNetworkQuality)downQuality ofUser:(NSString *)userId`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| upQuality | ERTCNetworkQuality | 上行网络质量 |
| downQuality | ERTCNetworkQuality | 下行网络质量 |
| userId | NSString | userId 用户id, 当id为自己的userId时，表示本地网络质量，否则表示其它用户的 |

### onUserCustomMsg

当房间中的某个用户使用 {sendCustomMsg} 发送自定义 消息时，房间中的其它用户可以通过 onUserCustomMsg 事件回调接收到该条消息。

`- (void)onUserCustomMsg:(NSString *)userId msg:(NSData *)msg`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| msg | NSData | 消息数据 |

### onLocalVideoStats

本地视频实时数据

`- (void)onLocalVideoStats:(ERTCLocalVideoStatistics *)videoStats`

说明：videoStats 本地视频相关数据

### onRemoteVideoStats

远端视频实时数据

`- (void)onRemoteVideoStats:(ERTCRemoteVideoStatistics *)videoStats`

说明：videoStats 远端视频相关数据

### onLocalAudioStats

本地音频实时数据

`- (void)onLocalAudioStats:(ERTCLocalAudioStatistics *)audioStats`

说明：audioStats 本地音频相关数据

### onRemoteAudioStats

远端视频实时数据

`- (void)onRemoteAudioStats:(ERTCRemoteAudioStatistics *)audioStats`

说明：audioStats 远端音频相关数据

### onSpeedTestResult

网络测速结果

`- (void)onSpeedTestResult:(ERTCSpeedTestResult *)result`

说明：result 测速结果

### onDisplay

远端视频解码回调

`- (void)onDisplay:(NSString *)userId dataLength:(int)dataLength`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID |
| dataLength | int | 数据长度 |

### onForceStopShareScreen

强制停止本地用户屏幕共享

`- (void)onForceStopShareScreen`

### remoteUserRejoinRoom

远端用户重新加入房间

`- (void)remoteUserRejoinRoom:(NSString *)userId`

说明：userId 用户id