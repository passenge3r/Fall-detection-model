# ERTC SDK Android 使用指引.md

> ERTC SDK Android 使用指引

> 更新时间: 2026-05-25T16:36:31.000+08:00

> 文档ID: 1830 | 来源树: 音视频

---

# **ERTC-SDK Android使用指引**

# 版权声明

**版权所有©杭州萤石软件有限公司2023。保留一切权利。**

本文档的任何部分，包括文字、图片、图形等均归属于杭州萤石软件有限公司及其关联公司（以下简称“本公司”或“萤石”）。未经书面许可，任何单位和个人不得以任何方式摘录、复制、翻译、修改本文档的全部或部分。除非另有约定，萤石不对本文档提供任何明示或默示的声明或保证。

**关于本文档**

本手册仅作为相关产品的指导说明，可能与实际产品存在差异，请以实物为准。因产品版本升级或其他需要，萤石可能对本手册进行更新。
萤石建议您在专业人员的指导下使用本手册。

**责任声明**

在法律允许的最大范围内，本文档是“按照现状”提供，可能存在瑕疵或错误。萤石不对本文档提供任何形式的明示或默示保证，包括但不限于适销性、质量满意度、适合特定目的、不侵犯第三方权利等保证；亦不对使用或是分发本文档导致的任何特殊、附带、偶然或间接的损害进行赔偿，包括但不限于商业利润损失、系统故障、数据或文档丢失产生的损失。

## 1.简介

视频通话 SDK 可实现纯语音通话和视频通话功能。

## 2.前提条件

接入语言: JAVA 或 Kotlin  
库名称: ERTCEngine  
环境准备:支持 Android minsdk 21  
开发环境: Android Studio 2.6及以上  
NDK支持架构: armeabi-v7a, arm64-v8a  
依赖库:

- 1. Okhttp 3.14.9 及以上
- 2. Gson 2.x 及以上

## 3.如何集成

#### 3.1权限要求

```
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.BLUETOOTH" />

<uses-feature android:name="android.hardware.camera" />
<uses-feature android:name="android.hardware.camera.autofocus" />
```

#### 3.2混淆规则

```
-keep class com.ez.ertcengine.ERTCEngine { *; }
-keep class com.ez.ertcengine.ERTCEngine$* { *; }
-keep class com.ez.ertcengine.model.* { *; }
-keep public class com.ez.ertcengine.impl.ERTCEngineImpl {
	public protected *;
}
-keep class com.ez.basertc.** { *; }
-keep class com.ez.baselib.** { *; }
-keep class com.ez.network.** { *; }
-keep class * extends com.ez.network.HeaderInfo { *; }
-keep class * extends com.ez.network.BaseInfo { *; }
-keep class * extends com.ez.network.BaseResponse { *; }
-keep class * extends com.ez.network.BaseException { *; }
-keep class com.ez.dclog.** { *; }
-keep class com.ez.ezrtc.model.** { *; }
-keep class com.ez.ezrtc.impl.** { *; }
-keep class com.ez.ezrtc.EzrtcPluginManager { *; }
-dontwarn org.MediaPlayer.PlayM4.**
-keep class org.MediaPlayer.PlayM4.** { *;}
-dontwarn com.sun.jna.**
-keep class com.sun.jna.**{*;}
-keep interface com.ezviz.videotalk.jna.**{*;}
-keep class com.ezviz.videotalk.JNAApi {
	public protected *;
}
-keep class com.ezviz.videotalk.JNAApi$* { *; }
-keep class * extends com.sun.jna.Structure { *; }
-keep class com.mediaplayer.audio.AudioCodecParam { *; }
-keep class com.mediaplayer.audio.AudioCodecParam$* { *; }
-keep class com.mediaplayer.audio.AudioEngineParam { *; }
-keep class com.mediaplayer.audio.AudioEngineParam$* { *; }
-keep class com.ezviz.mediarecoder.configuration.**{*;}
```

## 4.功能介绍

| **功能名称** | **功能说明** |
| --- | --- |
| 全局配置 | 初始化，设置回调 |
| 房间管理 | 进入房间，退出房间 |
| 视频管理 | 开关本地视频，订阅和取消远端视频，设置编码参数，小码流 |
| 音频管理 | 开关本地音频，启用音量大小提示 |
| 设备管理 | 切换摄像头 |

## 5. 实现视频通话

### 5.1 初始化流程

```
// 初始化
RTCConstant.RTCEngineConfig config = new RTCConstant.RTCEngineConfig();
config.appId = ertcTestAppIdDebug;
config.context = context.getApplicationContext();
// 音频编码类型[非必须，默认OPUS]
config.audioCodeType = RTCConstant.ErtcAudioCodeType.OPUS;
// 日志路径[非必须]
config.logLevel = LogUtil.ERTC_LOG_LEVEL_INFO;
config.logPath = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS).getPath();
//  日志回调[非必须]
com.ez.baselib.utils.LogUtil.setErtcLogCallback(new LogUtil.ErtcLogCallback() {
      @Override
       public void onLog(int logLevel, String tag, String content) {
            // TODO 日志回调，可以根据自己的需要打印或写入日志
       }
 });

ERTCEngine ertcEngine;
ERTCEngine.init(config, object : ERTCEngine.OnInitListener{
	override fun onInitialization(engine: ERTCEngine) {
		// 成功之后获取enine实例
		ertcEngine = engine
	}
	override fun onError(code: Int) {
		// 错误
	}
})

// 待初始化成功后，设置事件回调
ertcEngine.setRTCListener(new RTCListener() {
	@Override
	public void onEnterRoomSuccess() {
		// 进入房间成功
	}
	@Override
	public void onExitRoom(int reason) {
		// 退出房间成功
	}
	// 其他回调，详见事件回调文
	...................................
});
```

### 5.2 房间管理流程

```
//进入房间
RTCConstant.EnterParam param = new RTCConstant.EnterParam();
param.userId = userId;
param.roomId = roomId;
param.token= token;
ertcEngine.enterRoom(info, RTCConstant.Scene.VideoCall);

//退出房间
ertcEngine.exitRoom();
```

### 5.3 视频管理流程

```
//设置大码流视频参数
val videoParam = ERTCVideoEncParam()
videoParam.videoResolution = ERTCVideoResolution.ERTCVideoResolution_640_480
videoParam.videoFps = 10
videoParam.videoBitrate = 500 * 1024
ertcEngine?.setVideoEncoderParam(videoParam)

//开关本地视频
ertcEngine?.enableLocalVideo(mVideoEnabled)

//切换摄像头
ertcEngine?.switchCamera()

//设置填充模式及本地预览
videoCanvasView.setRenderType(RTCConstant.ERTC_VIDEO_RENDER_MODE_FILL)
ertcEngine?.setLocalPreview(videoCanvasView)

//开关小码流
val videoParam = ERTCVideoEncParam()
videoParam.videoResolution = ERTCVideoResolution.ERTCVideoResolution_640_480
videoParam.videoFps = 10
videoParam.videoBitrate = 500 * 1024
ertcEngine?.enableLocalSmallVideo(true, videoParam)

//订阅和取消远端视频
videoCanvasView.setRenderType(RTCConstant.ERTC_VIDEO_RENDER_MODE_FILL)
ertcEngine?.setRemoteView(userId, RTCConstant.ERTC_VIDEO_STREAM_TYPE_BIG, videoCanvasView)

//切换订阅视频类型
ertcEngine?.setRemoteVideoStreamType(userId, RTCConstant.ERTC_VIDEO_STREAM_TYPE_SMALL)
```

### 5.4 音频管理流程

```
//开关本地音频
ertcEngine?.enableLocalAudio(true)

//开启与关闭音量回调
ertcEngine?.enableAudioVolumeEvaluation(300)
```

### 5.5 退出会议流程

```
//本地窗口解绑
ertcEngine?.setLocalView(null)
//本地窗口解绑
ertcEngine?.setLocalViewChanged(null)
//共享屏幕窗口解绑
ertcEngine?.setScreenShareWindow(null)
//退出会议
ertcEngine?.exitRoom()
//解除事件监听
ertcEngine?.setRTCListener(null)
ertcEngine?.setRtcStatsListener(null)
```