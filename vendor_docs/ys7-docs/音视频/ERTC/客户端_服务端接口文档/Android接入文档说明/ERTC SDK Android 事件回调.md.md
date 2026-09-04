# ERTC SDK Android 事件回调.md

> ERTC SDK Android 事件回调

> 更新时间: 2026-05-25T16:36:31.000+08:00

> 文档ID: 1826 | 来源树: 音视频

---

# **ERTC-SDK Android事件回调**

#### Updated Time 2023/08/30

## 1. RTCListener简介

RTCListener是ERTCEngine对应的回调事件，您可以通过此回调，来监听自己感兴趣的回调事件

```
// 待初始化成功后，设置事件回调
ertcEngine.setRTCListener(new RTCListener() {
	// 回调
	...................................
});
```

### 回调事件概览

| API | 描述 |
| --- | --- |
| 错误码回调 |  |
| onError | 错误码回调 |
| 加入房间回调 |  |
| onEnterRoomSuccess | 本地用户成功加入房间 |
| onRemoteUserEnterRoom | 远端用户成功加入房间 |
| 退出房间回调 |  |
| onExitRoom | 本地用户退出房间 |
| onRemoteUserLeaveRoom | 远端用户退出房间 |
| 音视频相关回调 |  |
| onFirstLocalVideoFrame | 本地视频首帧显示回调 |
| onFirstRemoteVideoFrame | 远端视频首帧显示回调，订阅视频后将会收到该回调 |
| onUserVideoAvailable | 远端用户推流或关闭视频流的回调 |
| onUserAudioAvailable | 远端用户推流或关闭音频流的回调 |
| onVolumeEvaluation | 音量回调，用户需要调用 enableAudioVolumeEvaluation 开启才会产生回调 |
| onNetworkQuality | 网络质量回调 |
| onShareStateChanged | 分享状态回调 |
| onRecvCustomMsg | 收到自定义消息的事件回调 |
| onDisplayLoadingState | 回调视频卡顿的时长 |
| onForceStopShareScreen | 强制停止屏幕共享回调 |

### 回调事件详情

### 1.onError

错误码回调详见：RTCError

`public void onError(int errorCode)`

### 2.onEnterRoomSuccess

用户加入房间成功，加入房间成功后将收到回调

`public void onEnterRoomSuccess()`

### 3.onRemoteUserEnterRoom

远端用户进入房间成功回调，进入房间时将会收到所有已在房间内用户加入房间的回调

`public void onRemoteUserEnterRoom(String userId)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |

### 4.onExitRoom

用户退出房间，非主动退出房间才会收到该回调

`public void onExitRoom(int reason)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| reason | int | 1-服务器禁止 2-房间解散 |

### 5.onRemoteUserLeaveRoom

远端用户退出房间回调

`public void onRemoteUserLeaveRoom (String userId, int reason)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| reason | String | 离开房间原因 0-主动 1-服务器禁止 2-房间解散 |

### 6.onFirstLocalVideoFrame

本地视频首帧显示回调

`public void onFirstLocalVideoFrame(int width, int height)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| width | int | 视频宽 |
| height | int | 视频高 |

### 7.onFirstRemoteVideoFrame

远端视频首帧显示回调，订阅视频后将会收到该回调

`public void onFirstRemoteVideoFrame(String userId, int width, int height)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| width | int | 视频宽 |
| height | int | 视频高 |

### 8.onUserVideoAvailable

远端用户推流或关闭视频流的回调

`public void onUserVideoAvailable(String userId, boolean available, int streamType)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| available | boolean | true-视频可用 false-视频不可用 |
| streamType | int | 码流类型 ERTC\_VIDEO\_STREAM\_TYPE\_BIG ERTC\_VIDEO\_STREAM\_TYPE\_SMALL |

### 9.onUserAudioAvailable

远端用户推流或关闭音频流的回调

`public void onUserAudioAvailable(String userId, boolean available)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| available | boolean | true-音频可用 false-音频不可用 |

### 10.onVolumeEvaluation

音量回调，用户需要调用 enableAudioVolumeEvaluation 开启才会产生回调

`public void onVolumeEvaluation(List<RTCConstant.AudioVolumeInfo> audioVolumeInfoList, int total)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| audioVolumeInfoList | RTCConstant.AudioVolumeInfo | 最多返回音量最大的三个用户 |
| total | int | 混音后的音量大小 |

### 11.onNetworkQuality

网络质量回调

`public void onNetworkQuality(String userId, int upNetQuality, int downNetQuality)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| upNetQuality | int | 上行质量等级详见：ERTC\_QUALITY\_UNKNOWN |
| downNetQuality | int | 下行质量等级详见：ERTC\_QUALITY\_UNKNOWN |

### 12.onShareStateChanged

分享状态回调

`public void onShareStateChanged(String userId, boolean enable)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| enable | int | true-开始共享 false-结束共享 |

### 13.onRecvCustomMsg

收到自定义消息的事件回调

`public void onRecvCustomMsg(String userId, byte[] message, int messageSize)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| message | byte[] | 消息数据 |
| messageSize | int | 消息长度 |

### 14.onDisplayLoadingState

回调视频卡顿的时长

`public void onDisplayLoadingState(String userId, long unDisplayTime)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| unDisplayTime | long | 画面卡顿时长单位毫秒，超过2秒可以显示Loading，小于2秒可以隐藏Loading |

### 15.onForceStopShareScreen

管理员强制停止屏幕共享

`public void onForceStopShareScreen()`

## 2. RTCStatsListener简介

RTCStatsListener是ERTCEngine对音视频质量的回调

```
// 待初始化成功后，设置事件回调
ertcEngine.setRtcStatsListener(new RTCStatsListener() {
	// 回调
	...................................
});
```

### 1.onLocalVideoStats

统计本地视频实时数据

`public void onLocalVideoStats(ERTCLocalVideoStats localVideoStats)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| localVideoStats | ERTCLocalVideoStats | 本地视频实时数据 |

### 2.onLocalAudioStats

统计本地音频实时数据

`public void onLocalAudioStats(ERTCLocalAudioStats localAudioStats)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| localAudioStats | ERTCLocalAudioStats | 本地音频实时数据 |

### 3.onRemoteVideoStats

统计本地音频实时数据

`public void onRemoteVideoStats(ERTCRemoteVideoStats remoteVideoStats)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| remoteVideoStats | ERTCRemoteVideoStats | 本地音频实时数据 |

### 4.onRemoteAudioStats

统计本地音频实时数据

`public void onRemoteAudioStats(ERTCRemoteAudioStats remoteAudioStats)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| remoteAudioStats | ERTCRemoteAudioStats | 本地音频实时数据 |

## 3. RTCSpeedTestListener简介

RTCSpeedTestListener是ERTCEngine对网速测试的回调

```
// 待初始化成功后，设置事件回调
ertcEngine.setSpeedTestListener(new RTCSpeedTestListener() {
	// 回调
	...................................
});
```

### 1.onSpeedTestResult

通话前测速结果

`public void onSpeedTestResult(RTCConstant.SpeedTestResult result)`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| result | RTCConstant.SpeedTestResult | 测试结果 |