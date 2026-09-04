# ERTC SDK Android API概览.md

> ERTC SDK Android API概览

> 更新时间: 2026-05-25T16:36:31.000+08:00

> 文档ID: 1829 | 来源树: 音视频

---

# ERTC SDK Android API概览

## ERTCEngine Api简介

| 方法 | 说明 |
| --- | --- |
| 初始化 |  |
| init | 创建ERTCEngine实例 |
| destroyEngine | 释放之前通过init创建的对象 |
| getSDKVersion | 获取当前版本号 |
| setLogLevelDebug | 设置日志等级 |
| setRTCListener | 设置事件回调 |
| setRtcStatsListener | 设置音视频实时数据回调 |
| 房间管理 |  |
| enterRoom | 加入房间 |
| exitRoom | 退出房间 |
| dissolveRoom | 解散会议 |
| forceCloseOtherScreenShare | 管理员适用，停止他人的屏幕共享 |
| 音频管理 |  |
| enableLocalAudio | 是否开启本地音频模块并推流 |
| setSpeakerPhoneOn | 是否打开扬声器 |
| enableRoomSound | 会议全场静音 |
| enableHardAec | 是否开启硬件回声消除 |
| enableAudioVolumeEvaluation | 开启与关闭音量回调，仅返回自己和音量最大的三个用户的声音大小 |
| 视频管理 |  |
| enableLocalVideo | 是否开启本地采集并推流。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 |
| enableDualStreamMode | 是否开启双流模式 |
| setVideoEncoderParam | 设置视频编码参数，不设置则默认为640\*480@15fps |
| setSmallVideoEncodeParam | 设定本地视频的编码参数 小码流 |
| setLocalView | 设置本地预览窗口，必须开启本地采集后调用，预览成功后自己将收到 onFirstLocalVideoFrame |
| setRemoteView | 订阅远端码流 |
| setBeautyLocalView | 设置本地预览美颜窗口 |
| switchCamera | 前后置摄像头切换 |
| forceFlipCamera | 强制镜像摄像头 |
| setRemoteVideoStreamType | 切换订阅远端码流类型 |
| setLocalViewChanged | 设置本地预览窗口，如不设置将无法进行摄像头编码 |
| setRemoteViewChanged | 设置远端播放窗口，需要订阅之后再行调用 |
| setHardDecodePriority | 设置是否硬件解码优先，订阅码流之前调用有效 |
| getDecodeEngine | 获取该用户当前解码方式，注意设置成硬解优先后，依然有概率失败并通过软解进行播放 |
| setDisplayRegion | 设置视频显示区域，用于电子放大 |
| setBeautyConfig | 设置美颜参数 |
| setBeautyEnable | 是否开启美颜 |
| setBeautyFilter | 设置滤镜 |
| 视频订阅 |  |
| subScribe | 订阅或取消码流 |
| 屏幕共享管理 |  |
| initShareScreen | 开始屏幕共享，开发者需要在Activity中重写onActivityResult,并在其中调用下方的EZRtc.onActivityResult. |
| setScreenShareWindow | 设置屏幕共享窗口 |
| setScreenShareEncoderParam | 设置屏幕共享视频编码参数，不设置则默认为640\*480@15fps |
| requestShareScreenPermission | 开启屏幕共享，注意需要在Activity的onActivityResult中继续调用此方法下方的onActivityResult |
| onScreenShareActivityResult | 用户申请屏幕共享权限后，用于传下传递 |
| stopScreenShare | 停止屏幕共享 |
| setShareViewScaleEnable | 共享屏幕是否打开电子放大 |
| 网络测试 |  |
| startSpeedTest | 网络测试 |
| stopSpeedTest | 停止网络测试 |
| setSpeedTestListener | 设置网络测试回调 |
| 自定义消息 |  |
| sendCustomMsg | 发送自定义消息 |
| 音视频数据回调管理 |  |
| setQualityInterval | 设置质量回调间隔（>=1000） |

## ERTCEngine Api详情

### 1. init

创建ERTCEngine实例

`public static ERTCEngine init(RTCConstant.RTCEngineConfig config, OnInitListener onInitListener)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| config | RTCEngineConfig | 初始化配置 |
| onInitListener | OnInitListener | 初始化回调 |

### 2. destroyEngine

释放之前通过init创建的对象

`public static void destroyEngine()`

### 3. getSDKVersion

获取当前版本号

`public static String getSDKVersion()`

### 4. setLogLevelDebug

设置日志等级

`public void setLogLevelDebug(RTCConstant.BavLogLevel logLevel)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| logLevel | RTCConstant.BavLogLevel | 日志等级 |

### 5. setRTCListener

设置事件回调

`public void setRTCListener(RTCListener rtcListener)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| rtcListener | RTCListener | 事件回调 |

### 6. setRtcStatsListener

设置事件回调

`public void setRtcStatsListener(RTCStatsListener rtcStatsListener)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| rtcStatsListener | RTCStatsListener | 事件回调 |

### 7. enterRoom

进入房间，进入成功后自己端将收到onEnterRoomSuccess, 房间内其它用户将收到onRemoteUserEnterRoom

`public void enterRoom(RTCConstant.EnterParam param, RTCConstant.Scene scene)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| param | RTCConstant.EnterParam | 进入房间参数 |
| scene | RTCConstant.Scene | 场景 |

### 8. exitRoom

退出房间，退出后其它用户端将收到onRemoteUserLeaveRoom

`public void exitRoom()`

### 9. dissolveRoom

解散会议，此时会议中其它用户将会收到会议解散并被移出的通知

`public void dissolveRoom()`

### 10. forceCloseOtherScreenShare

管理员适用，停止他人的屏幕共享

`public void forceCloseOtherScreenShare()`

### 11. enableLocalAudio

开启本地音频模块并推流，调用成功后其它用户将收到 onUserAudioAvailable

`public void enableLocalAudio(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | 是否开启 |

### 12. setSpeakerPhoneOn

是否打开扬声器

`public void setSpeakerPhoneOn(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | 是否开启 |

### 13. enableRoomSound

会议全场静音

`public void enableRoomSound(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-非静音 / false-静音 |

### 14. enableHardAec

设置是否开启硬件回声消除

`public void enableHardAec(boolean enable)`

### 15. enableAudioVolumeEvaluation

开启与关闭音量回调，仅返回自己和音量最大的三个用户的声音大小

`public void enableAudioVolumeEvaluation(int interval)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| interval | int | 单位毫秒 0表示关闭，其它表示间隔，推荐设置300 |

### 16. enableLocalVideo

是否开启本地采集并推流。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到

`public void enableLocalVideo(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-开启推流 false-关闭推流 |

### 17. enableDualStreamMode

是否开启双流模式

`public void enableDualStreamMode(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-开启 / false-关闭 |

### 18. setVideoEncoderParam

设置视频编码参数，不设置则默认为640\*480@15fps

`public void setVideoEncoderParam(RTCConstant.ERTCVideoEncParam ERTCVideoEncParam, boolean isExChangeWH)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| ERTCVideoEncParam | RTCConstant.ERTCVideoEncParam | 视频编码参数,详见： RTCConstant.ERTCVideoEncParam |
| isExChangeWH | boolean | 是否切换宽高值，高>宽 |

### 19. setSmallVideoEncodeParam

设定本地视频的编码参数 小码流

`public void setSmallVideoEncodeParam(RTCConstant.ERTCVideoEncParam ERTCVideoEncParam, boolean isExChangeWH)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| ERTCVideoEncParam | RTCConstant.ERTCVideoEncParam | 视频编码参数,详见：RTCConstant.ERTCVideoEncParam, 传null时则按大码流同比例缩小 |
| isExChangeWH | boolean | 是否切换宽高值，高>宽 |

### 20. setLocalView

设置本地预览窗口，必须开启本地采集后调用，预览成功后自己将收到 onFirstLocalVideoFrame

`public void setLocalView(VideoCanvasView localView)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| localView | VideoCanvasView | 视频窗口，详见： VideoCanvasView |

### 21. setRemoteView

订阅远端码流

`public void setRemoteView(String userId, int streamType, VideoCanvasView remoteView)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| streamType | int | 码流类型，当小码流不存在时，会自动切成大码流, 取值参考 RTCConstant.ERTC\_VIDEO\_STREAM\_TYPE\_BIG，RTCConstant.ERTC\_VIDEO\_STREAM\_TYPE\_SMALL |
| remoteView | VideoCanvasView | 视频窗口，详见： VideoCanvasView |

### 22. setBeautyLocalView

设置本地预览美颜窗口

`public void setBeautyLocalView(VideoCanvasView localView)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| localView | VideoCanvasView | 视频窗口，详见： VideoCanvasView |

### 23. switchCamera

前后置摄像头切换

`public void switchCamera()`

### 23. forceFlipCamera

强制镜像摄像头

`public void forceFlipCamera(boolean mirror)`
参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| mirror | Boolean | 是否强制镜像 |

### 24. setRemoteVideoStreamType

切换订阅远端码流类型

`public void setRemoteVideoStreamType(String userId, int streamType)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |
| streamType | int | 码流类型，当小码流不存在时，会自动切成大码流, 取值参考 RTCConstant.ERTC\_VIDEO\_STREAM\_TYPE\_BIG，RTCConstant.ERTC\_VIDEO\_STREAM\_TYPE\_SMALL |

### 25. setLocalViewChanged

设置本地预览窗口，如不设置将无法进行摄像头编码

`public void setLocalViewChanged(VideoCanvasView localView)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| localView | VideoCanvasView | 视频窗口，详见： VideoCanvasView |

### 26. setRemoteViewChanged

设置远端播放窗口，需要订阅之后再行调用

`public void setRemoteViewChanged(VideoCanvasView remoteView, String userId)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| remoteView | VideoCanvasView | 视频窗口，详见： VideoCanvasView |
| userId | String | 用户ID |

### 27. setHardDecodePriority

设置是否硬件解码优先，订阅码流之前调用有效

`public void setHardDecodePriority(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-硬解优先 / false-软件优先 |

### 28. getDecodeEngine

获取该用户当前解码方式，注意设置成硬解优先后，依然有概率失败并通过软解进行播放

`public int getDecodeEngine(String userId)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户ID |

### 29. setDisplayRegion

设置视频显示区域，用于电子放大

`public void setDisplayRegion(int left, int top, int right, int bottom)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| left | int | 显示区域 |
| top | int | 显示区域 |
| right | int | 显示区域 |
| bottom | int | 显示区域 |

### 30. setBeautyConfig

设置美颜参数

`public void setBeautyConfig(float whitenessIntensity, float smoothnessIntensity, float ruddyIntensity)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| whitenessIntensity | float | 美白 范围[0.0-1.0] |
| smoothnessIntensity | float | 磨皮 范围[0.0-1.0] |
| ruddyIntensity | float | 红润 范围[0.0-1.0] |

### 31. setBeautyEnable

是否开启美颜

`public void setBeautyEnable(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-开 / false-关 |

### 32. setBeautyFilter

设置滤镜

`public void setBeautyFilter(int filterType, float intensity)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| filterType | int | 滤镜类型 |
| intensity | int | 滤镜浓度 |

### 33. subScribe

订阅或取消码流

`public void subScribe(String userId, int streamType, boolean subscribe)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | String | 用户id |
| streamType | int | 大、小码流等 |
| subscribe | boolean | true-开启订阅 false-取消订阅 |

### 34. initShareScreen

开始屏幕共享，开发者需要在Activity中重写onActivityResult,并在其中调用下方的EZRtc.onActivityResult.

`public void initShareScreen(String shareName, OnApplyResultListener onApplyResultListener)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| shareName | String | 屏幕共享的名称 |
| onApplyResultListener | OnApplyResultListener | 当用户允许权限后，会到服务进行验证当前是否可共享，并将结果以回调形式返回 |

### 35. setScreenShareWindow

设置屏幕共享窗口

`public void setScreenShareWindow(VideoCanvasView shareView)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| shareView | VideoCanvasView | 用于播放的窗口，不使用播放时需设置为null |

### 36. setScreenShareEncoderParam

设置屏幕共享视频编码参数，不设置则默认为640\*480@15fps

`public void setScreenShareEncoderParam(RTCConstant.ERTCVideoEncParam ERTCVideoEncParam)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| ERTCVideoEncParam | RTCConstant.ERTCVideoEncParam | 视频编码参数,详见：RTCConstant.ERTCVideoEncParam |

### 37. requestShareScreenPermission

开启屏幕共享，注意需要在Activity的onActivityResult中继续调用此方法下方的onActivityResult

`public void requestShareScreenPermission(Activity activity, int requestCode)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| activity | Activity | 申请授权的页面 |
| requestCode | int | 请求码 |

### 38. onScreenShareActivityResult

用户申请屏幕共享权限后，用于传下传递

`public void onScreenShareActivityResult(int requestCode, int resultCode, Intent data, Service service)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| requestCode | int | 请求码 |
| resultCode | int | 结果码 |
| data | Intent | 数据Intent |
| service | Service | 服务 |

### 39. stopScreenShare

停止屏幕共享

`public void stopScreenShare()`

### 40. setShareViewScaleEnable

共享屏幕是否打开电子放大

`public void setShareViewScaleEnable(boolean enable)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enable | boolean | true-开 / false-关 |

### 41. startSpeedTest

开始网络测试

`public void startSpeedTest(int upBandwidth, int downBandwidth, int testInterval)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| upBandwidth | int | 预期的上行带宽（kbps，取值范围： 10 ～ 5000，为 0 时不测试） |
| downBandwidth | int | 预期的下行带宽（kbps，取值范围： 10 ～ 5000，为 0 时不测试） |
| testInterval | int | 统计间隔（毫秒） |

### 42. stopSpeedTest

结束网络测试

`public void stopSpeedTest()`

### 43. setSpeedTestListener

设置网络测试回调

`public void setSpeedTestListener(RTCSpeedTestListener listener)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| listener | RTCSpeedTestListener | 网速监听回调 |

### 44. sendCustomMsg

发送自定义消息给房间内用户

`public int sendCustomMsg(String msg)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| msg | String | 消息内容 |

### 45. setQualityInterval

设置质量回调间隔（>=1000）

`public void setQualityInterval(int interval)`

参数详情：

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| interval | int | 质量回调的触发间隔，单位为ms，最小间隔为1000，默认2000 |