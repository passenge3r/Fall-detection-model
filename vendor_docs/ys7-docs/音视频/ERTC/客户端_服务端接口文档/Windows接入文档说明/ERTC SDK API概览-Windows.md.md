# ERTC SDK API概览-Windows.md

> 更新时间: 2026-05-25T16:36:30.000+08:00

> 文档ID: 1915 | 来源树: 音视频

---

# ERTC API概览

#### Updated Time 2023/08/30

## ERTCEngine Api简介

| 方法 | 说明 |
| --- | --- |
| 初始化 |  |
| getERtcShareInstance | 创建ERTCEngine实例 |
| destroyERtcShareInstance | 销毁ERtcEngine实例 |
| initialize | 初始化接口 |
| setCallback | 设置ERTC事件回调 |
| setAccessToken | 设置 ERTC AccessToken |
| 房间管理 |  |
| enterRoom | 加入房间 |
| exitRoom | 退出房间 |
| 视频管理 |  |
| startLocalPreview | 开启本地摄像头的预览画面 |
| stopLocalPreview | 停止摄像头预览 |
| enableSmallVideoStream | 开启大小画面双路编码模式 |
| setVideoEncoderParam | 设置视频编码器的编码参数 |
| 视频订阅 |  |
| startRemoteView | 订阅远端用户的视频流，并绑定视频渲染控件 |
| stopRemoteView | 停止订阅远端用户的视频流，并释放渲染控件 |
| setRemoteVideoStreamType | 切换指定远端用户的大小画面 |
| muteAllRemoteVideoStreams | 暂停/恢复订阅所有远端用户的视频流 |
| 音频管理 |  |
| startLocalAudio | 开启本地音频的采集和发布 |
| stopLocalAudio | 停止本地音频的采集和发布 |
| enableAudioVolumeEvaluation | 启用音量大小提示 |
| 屏幕共享管理 |  |
| startScreenCapture | 开始桌面端屏幕分享 |
| stopScreenCapture | 停止屏幕分享 |
| getScreenCaptureSources | 枚举可分享的屏幕和窗口 |
| 网络测试 |  |
| startSpeedTest | 开始进行网速测试 |
| stopSpeedTest | 停止网络测试 |
| 自定义消息 |  |
| sendCustomMsg | 发送自定义消息 |
| 调试相关接口 |  |
| getSDKVersion | 获取 SDK 版本信息 |
| setPlatformAddr | 设置 测试 平台地址 |
| setConfigInfo | 通用配置(比方质量回调间隔) |

## Api详情

### getERtcShareInstance

创建ERTCEngine实例

`ERTC_API static ERtcEngine* getERtcShareInstance();`

### destroyERtcShareInstance

销毁 ERtcEngine 实例

`ERTC_API static void destroyERtcShareInstance();`

### initialize

初始化

`virtual int initialize(const ERTCEngineContext& context) = 0;`

### setCallback

设置事件回调

`virtual void setCallback(ERtcCallback* eventHandler) = 0;`

### enterRoom

进入房间，进入成功后自己端将收到onEnterRoomSuccess, 房间内其它用户将收到onRemoteUserEnterRoom

`virtual int enterRoom(const ERTCParams& param) = 0;`

### exitRoom

退出房间，退出后其它用户端将收到onRemoteUserLeaveRoom

`virtual void exitRoom() = 0;`

### startLocalPreview

开启本地摄像头的预览画面。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 onUserVideoAvailable

`virtual int startLocalPreview(EView view) = 0;`

### stopLocalPreview

停止摄像头预览。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 onUserVideoAvailable

`virtual void stopLocalPreview() = 0;`

### startLocalAudio

开启本地音频的采集和发布，调用成功后其它用户将收到 onUserAudioAvailable

`virtual void startLocalAudio() = 0;`

### stopLocalAudio

停止本地音频的采集和发布，调用成功后其它用户将收到 onUserAudioAvailable

`virtual void stopLocalAudio() = 0;`

### setVideoEncoderParam

设置视频编码参数

`virtual void setVideoEncoderParam(const ERTCVideoEncParam& param) = 0;`

### enableSmallVideoStream

开启大小画面双路编码模式,默认开启大码流，如果开启小码流则是大小码流一起推送

`virtual void enableSmallVideoStream(bool enable, const ERTCVideoEncParam& smallVideoEncParam) = 0;`

### enableAudioVolumeEvaluation

启用音量大小提示 开启此功能后，SDK 会 onUserVoiceVolume 回调中反馈远端音频的音量大小 如需打开此功能，请在 enableLocalAudio 之前调用才可以生效

`virtual void enableAudioVolumeEvaluation(unsigned int interval) = 0;`

说明：interval 设置 onUserVoiceVolume 回调的触发间隔，单位为ms，最小间隔为100ms，如果小于等于 0 则会关闭回调，建议设置为500ms

### startScreenCapture

开启屏幕共享

`virtual void startScreenCapture(EView view, const ERTCScreenCaptureSourceInfo& source, ERTCVideoEncParam* encParam) = 0;`

### stopScreenCapture

停止屏幕分享

`virtual void stopScreenCapture() = 0;`

### sendCustomMsg

发送自定义消息给房间内所有用户

`virtual bool sendCustomMsg(const uint8_t* data, uint32_t dataSize) = 0;`

说明：待发送的消息，单个消息的最大长度被限制为 1KB

### startSpeedTest

开始网络测试

`virtual int startSpeedTest(const ERTCSpeedTestParams& params) = 0;`

### stopSpeedTest

停止网络测试

`virtual void stopSpeedTest() = 0;`

### startRemoteView

订阅远端用户的视频流，并绑定视频渲染控件

`virtual void startRemoteView(const char* userId, ERTCVideoStreamType streamType, EView view) = 0;`

### startRemoteView

停止订阅远端用户的视频流，并释放渲染控件

`virtual void stopRemoteView(const char* userId, ERTCVideoStreamType streamType) = 0;`

### muteAllRemoteVideoStreams

暂停/恢复订阅所有远端用户的视频流

`virtual void muteAllRemoteVideoStreams(bool mute) = 0;`

### getSDKVersion

获取 SDK 版本信息

`virtual const char* getSDKVersion() = 0;`

### setPlatformAddr

设置 测试 平台地址

`virtual void setPlatformAddr(const char* addr) = 0;`

### setConfigInfo

通用配置(比方质量回调间隔)

`virtual void setConfigInfo(ERTCConfigKey key, int value) = 0;`