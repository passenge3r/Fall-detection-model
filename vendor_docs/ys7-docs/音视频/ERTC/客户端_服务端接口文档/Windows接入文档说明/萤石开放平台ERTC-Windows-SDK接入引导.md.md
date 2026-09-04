# 萤石开放平台ERTC-Windows-SDK接入引导.md

> ERTC接入引导

> 更新时间: 2026-05-25T16:36:30.000+08:00

> 文档ID: 1831 | 来源树: 音视频

---

# **萤石开放平台 ERTC-SDK接入引导**

# 版权声明

**版权所有©杭州萤石软件有限公司2020。保留一切权利。**

本文档的任何部分，包括文字、图片、图形等均归属于杭州萤石软件有限公司及其关联公司（以下简称“本公司”或“萤石”）。未经书面许可，任何单位和个人不得以任何方式摘录、复制、翻译、修改本文档的全部或部分。除非另有约定，萤石不对本文档提供任何明示或默示的声明或保证。

**关于本文档**

本手册仅作为相关产品的指导说明，可能与实际产品存在差异，请以实物为准。因产品版本升级或其他需要，萤石可能对本手册进行更新。
萤石建议您在专业人员的指导下使用本手册。

**责任声明**

在法律允许的最大范围内，本文档是“按照现状”提供，可能存在瑕疵或错误。萤石不对本文档提供任何形式的明示或默示保证，包括但不限于适销性、质量满意度、适合特定目的、不侵犯第三方权利等保证；亦不对使用或是分发本文档导致的任何特殊、附带、偶然或间接的损害进行赔偿，包括但不限于商业利润损失、系统故障、数据或文档丢失产生的损失。

## 1.简介

视频通话 SDK 可实现纯语音通话和视频通话功能。  
产品简介:https://test12open.ys7.com/help/230

## 2.前提条件

接入语言: C++  
控件名称: ERTC.dll  
环境准备:支持 Windows 7 及以上版本  
开发环境:Visual Studio 2015及以上版本，推荐使用 Visual Studio 2015  
支持架构:x86

## 3.设置开发环境

1. 使创建 Windows 项目（MFC 应用程序）
2. 集成 SDK，首先. 配置项目文件（x86）， 然后，配置项目属性（附加包含目录， 附加库目录， 附加依赖项）

## 4.功能介绍

| **功能名称** | **头文件** | **功能说明** |
| --- | --- | --- |
| 全局配置 | ERtcEngine.h | 初始化，设置回调， 获取token |
| 房间管理 | ERTCEngine.h | 进入房间，退出房间 |
| 视频管理 | ERtcEngine.h | 开关本地视频，订阅和取消远端视频，设置编码参数，小码流 |
| 音频管理 | ERtcEngine.h | 开关本地音频，启用音量大小提示 |
| 设备管理 | ERtcDeviceManager.h | 切换摄像头 |
| 屏幕共享 | ERtcEngine.h | 开关屏幕共享，观看屏幕共享 |

## 5. 实现视频通话

### 5.1 初始化流程

```
//获取版本号
const char* sdkVer = getERtcShareInstance()->getSDKVersion();

//初始化
ERTCEngineContext context;
context.appId              = m_strAppId.c_str(); //开发者账号下AppId
context.logConfig.level    = ERTCLogLevelInfo;	 //默认INFO级别日志
context.logConfig.filePath = localPath.c_str();	 //音频数据存储路径，用于问题排查。
int ret = getERtcShareInstance()->initialize(context);

//设置回调
getERtcShareInstance()->setCallback(this);
getERtcShareInstance()->setCallback(nullptr);
```

### 5.2 房间管理流程

```
//5.2.1 rtc_token获取方法, rtc_token的生成算法参考文档 https://test12open.ys7.com/help/1873

//进入房间，onEnterRoomSuccess回调告知进入房间结果
ERTCParams params;
params.roomId = strRoomID.c_str();	//房间号，字符串类型
params.userId = strUserID.c_str();	//用户名，字符串类型
params.token  = rtcToken.c_str();	//rtc-token获取参考 5.2.1
getERtcShareInstance()->enterRoom(params);

//退出房间
getERtcShareInstance()->exitRoom();
```

### 5.3 视频管理流程

```
//设置大码流
ERTCVideoEncParam encParams;
encParams.videoResolution   = ERTCVideoResolution_640_360;
encParams.videoFps          = ERTCVideoFPS_15;
encParams.videoBitrate      = 500;
getERtcShareInstance()->setVideoEncoderParam(encParams);

//设置小码流
ERTCVideoEncParam samllEncParams;
samllEncParams.videoResolution   = ERTCVideoResolution_160_120;
samllEncParams.videoFps          = ERTCVideoFPS_5;
samllEncParams.videoBitrate      = 100;
getSamllVideoEncoderParam(encParams.videoResolution, samllEncParams);
getERtcShareInstance()->enableSmallVideoStream(true, samllEncParams);

//设置填充模式
ERTCRenderParams renderParams;
renderParams.fillMode = m_remoteFillMode;
getERtcShareInstance()->setRemoteRenderParams(userId, renderParams);

//开关本地视频
getERtcShareInstance()->startLocalPreview(hWHD);
getERtcShareInstance()->stopLocalPreview();

//订阅和取消远端视频
getERtcShareInstance()->startRemoteView(userId, streamType, hWHD);
getERtcShareInstance()->stopRemoteView(userId, (ERTCVideoStreamType)streamType);
```

### 5.4 音频管理流程

```
//开关本地音频
getERtcShareInstance()->startLocalAudio();
getERtcShareInstance()->stopLocalAudio();

//设置音量
getERtcShareInstance()->enableAudioVolumeEvaluation(interval);
```

### 5.5 设备管理流程

```
//摄像头切换
ERtcDeviceManager* devMgr = getERtcShareInstance()->getDeviceManager();
if (devMgr == NULL)
{
	return;
}
ERtcDeviceCollection* pDevice = devMgr->getDevicesList(EMediaDeviceTypeCamera);
if (pDevice) {
    for (int i = 0; i < pDevice->getCount(); i++)
    {
        if(type == EMediaDeviceTypeCamera){
            m_cameraCombo.AddString(UTF82Wide(pDevice->getDeviceName(i)).c_str());
        }
        else {
            m_micCombo.AddString(UTF82Wide(pDevice->getDeviceName(i)).c_str());
        }
    }
    pDevice->release();
}
```

### 5.6 屏幕共享

```
//开启自己视频，onScreenCaptureStarted回调告知开启结果
ERTCVideoEncParam param;
memset(&param, 0, sizeof(param));
param.videoFps = ERTCVideoFPS_15;
param.videoBitrate = 1200;

ERTCScreenCaptureSourceInfo sourceInfo;
getERtcShareInstance()->startScreenCapture(hWHD, sourceInfo, &param);

//订阅和取消他人屏幕共享，onUserSubStreamAvailable回调他人屏幕共享开启时，可调用下面接口定义屏幕共享视频
getERtcShareInstance()->startRemoteView(userId, ERTCVideoStreamTypeSub, hWHD); //hWHD为渲染的窗口句柄
getERtcShareInstance()->stopRemoteView(userId, ERTCVideoStreamTypeSub);
```

### 5.7 消息透传

```
std::string msg = "hello wrold";
getERtcShareInstance()->sendCustomMsg((const uint8_t*)msg.c_str(), (const uint32_t)msg.size());
```

### 5.8 事件回调

```
    /**
     * 2.1 进入房间成功与否的事件回调
     */
    virtual void onEnterRoomSuccess() {};
    /**
     * 2.2 离开房间的事件回调
     */
    virtual void onExitRoom(int reason) {};
	 /// Susan White 用户相关事件回调
    /// @{

    /**
     * 3.1 有用户加入当前房间
     */
    virtual void onRemoteUserEnterRoom(const char* userId) {};

    /**
     * 3.2 有用户离开当前房间
     */
    virtual void onRemoteUserLeaveRoom(const char* userId, int reason) {};

    /**
     * 3.3 某远端用户发布/取消了主路视频画面
     */
    virtual void onUserVideoAvailable(const char* userId, bool available) {};

    /**
     * 3.4 某远端用户发布/取消了自己的音频
     */
    virtual void onUserAudioAvailable(const char* userId, bool available) {};

    /**
    * 3.4 某远端用户发布/取消了自己的屏幕分享
    */
    virtual void onUserSubStreamAvailable(const char* userId, int available) {};
	/**
     * 3.10 屏幕分享开启的事件回调
     *
     * 当您通过 {@link startScreenCapture} 等相关接口启动屏幕分享时，SDK 便会抛出此事件回调。
     * @param reason 停止原因，0：用户主动停止；非0：屏幕窗口关闭导致停止；
     */
    virtual void onScreenCaptureStarted(int reason) {};
	        /**
    * 7.1 收到自定义消息的事件回调
    *
    * 当房间中的某个用户使用 {@link sendCustomMsg} 发送自定义消息时，房间中的其它用户可以通过 onRecvCustomMsg 事件回调接收到该条消息。
    *
    * @param userId 用户标识
    * @param message 消息数据
    */
    virtual void onRecvCustomMsg(const char* userId, const uint8_t* message, uint32_t messageSize) {};
```