# ERTC SDK API概览-iOS.md

> 音视频SDK接口概览

> 更新时间: 2026-05-25T16:36:32.000+08:00

> 文档ID: 1820 | 来源树: 音视频

---

# ERTC API概览

#### Updated Time 2023/11/29

## ERTCEngine Api简介

| 方法 | 说明 |
| --- | --- |
| 初始化 |  |
| createWithConfig | 创建ERTCEngine实例 |
| destroySharedIntance | 释放之前通过createWithConfig创建的对象 |
| 房间管理 |  |
| enterRoom | 加入房间 |
| exitRoom | 退出房间 |
| 音频管理 |  |
| enableLocalAudio | 是否开启本地音频模块并推流 |
| enableAudioVolumeEvaluation | 启用音量大小提示 |
| closeRoomSound | 是否关闭房间声音 |
| 视频管理 |  |
| enableLocalVideo | 是否开启本地采集并推流 |
| setVideoEncoderParam | 设置视频编码参数 |
| enableLocalSmallVideo | 是否开启小码流 |
| setLocalPreview | 设置本地预览窗口 |
| switchCamera | 切换前后置摄像头 |
| setHardDecodePriority | 是否硬件解码优先 |
| isHardDecode | 获取当前用户的解码方式 |
| 视频订阅 |  |
| subscribe | 订阅/取消订阅某个用户的视频流 |
| setRemoteView | 设置远端用户的播放画面 |
| setLocalPreviewScaleType | 设置本地预览视图的填充方式 |
| setRemoteViewScaleType | 设置远端视图的填充方式 |
| muteAllRemoteVideoStreams | 是否接收所有人视频流 |
| setFilter | 设置滤镜 |
| refreshRemoteView | 刷新窗口 |
| 屏幕共享管理 |  |
| startScreenShareWithName | 开启屏幕共享 |
| stopScreenShare | 结束屏幕共享 |
| forceCloseOtherScreenShare | 强制关闭其他人的屏幕共享 |
| setDisplayRegionOfUserId | 设置电子放大接口 |
| viewScaleOfUserId | 获取之前的缩放的倍数 |
| zoomMoveView | 移动/拖动播放视图 |
| 网络测试 |  |
| startSpeedTestWithUpBandwidth | 网络测试 |
| stopSpeedTest | 停止网络测试 |
| 自定义消息 |  |
| sendCustomMsg | 发送自定义消息 |
| 音视频数据回调管理 |  |
| setQualityInterval | 质量监测回调时间设置 |
| 网络状态管理 |  |
| setNetworkChange | 网络状态变化信息同步 |

## Api详情

### createWithConfig

创建ERTCEngine实例

`+ (void)createWithConfig:(ERTCEngineConfig *)config instanceBlock:(InstanceBlock)block`

参数列表如下

#### ERTCEngineConfig

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| enableAACEncode | BOOL | 是否开启 AAC 编码，默认关闭(可选) |

#### InstanceBlock

定义 typedef void(^InstanceBlock)(ERTCEngine \* \_Nullable instance,NSError \* \_Nullable error);

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| instance | ERTCEngine | 返回的实例 |
| error | NSError | 返回的错误 |

### destroySharedIntance

释放之前通过createWithConfig创建的对象

`+ (void)destroySharedIntance`

### enterRoom

进入房间，进入成功后自己端将收到onEnterRoomSuccess, 房间内其它用户将收到onRemoteUserEnterRoom

`- (void)enterRoom:(ERTCParam *)param withScene:(ERTCAppScene)scene`

参数列表如下

#### ERTCParam

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| userId | NSString | 用户ID， 外部用户自行约定，需保持唯一性 |
| roomId | NSString | 房间id, 限制长度32位 |
| token | NSString | 资源访问token,由开发者云颁发给终端使用 |
| apiUrl | NSString | 萤石云平台地址 |
| appID | NSString | 应用标识/应用 ID）是萤石云后台用来区分不同 ERTC 应用的唯一标识，在 ERTC 控制台 创建应用时自动生成 |

#### ERTCAppScene

默认填 ERTCAppScene\_VideoCall

### exitRoom

退出房间，退出后其它用户端将收到onRemoteUserLeaveRoom

`- (void)exitRoom`

### enableLocalVideo

是否开启本地采集并推流。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 onUserVideoAvailable

`- (void)enableLocalVideo:(BOOL)enable`

### enableLocalAudio

开启本地音频模块并推流，调用成功后其它用户将收到 onUserAudioAvailable

`- (void)enableLocalAudio:(BOOL)enable`

### setVideoEncoderParam

设置视频编码参数，不设置则默认为640\*480，需要在任何视频操作前设置

`-(void)setVideoEncoderParam:(ERTCVideoEncParam *)param`

参数列表如下

#### ERTCVideoEncParam

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| videoResolution | ERTCVideoResolution | 视频分辨率 |
| resMode | ERTCVideoResolutionMode | 横竖屏模式 |
| videoFps | ERTCVideoFPS | 视频采集帧率(15fps或20fps。5fps以下，卡顿感明显。10fps以下，会有轻微卡顿感。20fps以上，会浪费带宽（电影的帧率为24fps）) |
| videoBitrate | int | 视频码率(标视频码率，单位Kbps，SDK 会按照目标码率进行编码，只有在弱网络环境下才会主动降低视频码率) |

### enableLocalSmallVideo

是否开启小码流模块,默认开启大码流，如果开启小码流则是大小码流一起推送

`- (void)enableLocalSmallVideo:(BOOL)enable withQuality:(ERTCVideoEncParam *)smallVideoEncParam`

### setLocalPreview

设置本地预览窗口，必须开启本地采集后调用，预览成功后自己将收到 onFirstLocalVideoFrame

`- (void)setLocalPreview:(nullable ERTCView *)view`

### enableAudioVolumeEvaluation

启用音量大小提示 开启此功能后，SDK 会 onUserVoiceVolume 回调中反馈远端音频的音量大小 如需打开此功能，请在 enableLocalAudio 之前调用才可以生效

`- (void)enableAudioVolumeEvaluation:(NSUInteger)interval`

说明：interval 设置 onUserVoiceVolume 回调的触发间隔，单位为ms，最小间隔为100ms，如果小于等于 0 则会关闭回调，建议设置为300ms

### switchCamera

切换前后置摄像头

`- (void)switchCamera`

### startScreenShareWithName

开启屏幕共享

`- (void)startScreenShareWithName:(NSString *)name withResultBlock:(void (^)(NSInteger ret))resultBlock andEndedBlock:(dispatch_block_t)didFinishBlock`

### stopScreenShare

结束屏幕共享

`- (void)stopScreenShare`

### sendCustomMsg

发送自定义消息给房间内所有用户

`- (int)sendCustomMsg:(NSData *_Nonnull)data`

说明：待发送的消息，单个消息的最大长度被限制为 1KB

### startSpeedTestWithUpBandwidth

开始网络测试

`- (void)startSpeedTestWithUpBandwidth:(int)upBandwidth downBandwidth:(int)downBandwidth testInterval:(int)testInterval`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| upBandwidth | int | 上行带宽 |
| downBandwidth | int | 下行带宽 |
| testInterval | int | 统计间隔 |

### stopSpeedTest

停止网络测试

`- (void)stopSpeedTest`

### openOpusEncode

开启/关闭Opus编码，sdk音频默认使用 opus编码

`- (void)openOpusEncode:(BOOL)open`

### setLocalPreview

设置本地的预览窗口，支持设置多个，必须在主线程调用，如果窗口的大小发生变化，可能需要重新设置一遍

`- (void)setLocalPreview:(nullable UIView *)view withRegionID:(NSInteger)regionID`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| view | UIView | 预览View |
| regionID | NSInteger | 窗口ID，可以填0 、1（多窗口设置场景） |

### subscribe

订阅/取消订阅某个用户的视频流

`- (void)subscribe:(BOOL)subscribe forUser:(NSString *)userId withStream:(ERTCVideoStreamType)type`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| subscribe | BOOL | YES-开启订阅 NO-取消订阅 |
| userId | NSString | 用户的ID |
| type | ERTCVideoStreamType | 0：大码流 1：小码流 2：共享流 |

### setRemoteView

设置播放远端用户的播放画面

`- (void)setRemoteView:(nullable UIView *)view forUser:(NSString *)userId withRegionID:(NSInteger)regionID`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| view | UIView | 预览View |
| userId | NSString | 已订阅的用户的ID |
| regionID | NSInteger | 窗口ID，可以填0 、1（多窗口设置场景） |

### setDisplayRegionOfUserId

设置电子放大接口

`- (void)setDisplayRegionOfUserId:(NSString *)userId withRegionID:(NSInteger)regionID atRect:(CGRect)rect`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| rect | CGRect | 上下左右的偏移，以像素为单位 |
| userId | NSString | 已订阅的用户的ID |
| regionID | NSInteger | 窗口ID，可以填0 、1（多窗口设置场景） |

### viewScaleOfUserId

获取之前的缩放的倍数，用于电子放大使用

`- (CGFloat)viewScaleOfUserId:(NSString *)userId withRegionID:(NSInteger)regionID`

### zoomMoveView

移动/拖动播放视图

`- (void)zoomMoveView:(CGSize)viewSize WithUserId:(NSString *)userId withRegionID:(NSInteger)regionID movement:(CGVector)movement`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| viewSize | CGSize | 播放视图的大小 |
| userId | NSString | 已订阅的用户的ID |
| regionID | NSInteger | 窗口ID，可以填0 、1（多窗口设置场景） |
| movement | CGVector | 移动的方向，和viewSize同单位 |

### zoomScaleView

缩放播放视图

`- (void)zoomScaleView:(CGSize)viewSize WithUserId:(NSString *)userId withRegionID:(NSInteger)regionID scale:(CGFloat)scale center:(CGPoint)center`

参数列表如下

| 参数 | 类型 | 含义 |
| --- | --- | --- |
| viewSize | CGSize | 播放视图的大小 |
| userId | NSString | 已订阅的用户的ID |
| regionID | NSInteger | 窗口ID，可以填0 、1（多窗口设置场景） |
| scale | CGFloat | 缩放的倍数 不小于0，且不大于3 |
| center | CGPoint | 缩放的中心位置坐标 |

### setHardDecodePriority

设置是否硬件解码优先，订阅码流之前调用有效

`- (void)setHardDecodePriority:(BOOL)enable`

### isHardDecode

获取当前用户的解码方式

`- (BOOL)isHardDecode:(NSString *)userId`

### setLocalPreviewScaleType

设置本地预览视图的scaleType

`- (void)setLocalPreviewScaleType:(ERTCVideoFillMode)model withRegionID:(NSInteger)regionID`

### setRemoteViewScaleType

设置远端视图的scaleType

`- (void)setRemoteViewScaleType:(ERTCVideoFillMode)model withUserId:(NSString *)userId withRegionID:(NSInteger)regionID`

### setQualityInterval

质量监测回调时间设置

`- (void)setQualityInterval:(int)interval`

### muteAllRemoteVideoStreams

设置是否所有人视频流

`- (void)muteAllRemoteVideoStreams:(BOOL)mute`

### closeRoomSound

关闭房间声音

`- (void)closeRoomSound:(BOOL)open`

### setFilter

设置滤镜

`- (void)setFilter:(ERTCFilterType )type filterLevel:(float)filterLevel;`

### forceCloseOtherScreenShare

强制关闭其他人的屏幕共享

`- (void)forceCloseOtherScreenShare`

### setNetworkChange

网络状态变化信息同步 （ 0-切换 1-断开 2-恢复）

`- (void)setNetworkChange:(NSInteger)state`

### refreshRemoteView

刷新窗口

`- (void)refreshRemoteView:(NSString *)userId`

# ERTCReplayKit API概览

此类是专门针对屏幕共享功能使用的类

## Api详情

### setup

屏幕共享初始化，在broadcastStartedWithSetupInfo方法回调中调用这个方法

`- (void)setup`

### finish

屏幕共享结束，在broadcastFinished方法回调中调用这个方法

`- (void)finish`

### sendVideoBuffer

发送屏幕共享流数据，在processSampleBuffer方法回调中调用这个方法

`- (void)sendVideoBuffer:(CMSampleBufferRef)sampleBuffer`