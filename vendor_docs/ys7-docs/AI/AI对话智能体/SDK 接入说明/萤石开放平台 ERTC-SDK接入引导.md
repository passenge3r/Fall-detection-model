# 萤石开放平台 ERTC-SDK接入引导

> 萤石开放平台 ERTC-SDK接入引导

> 更新时间: 2026-05-25T16:37:59.000+08:00

> 文档ID: 4952 | 来源树: AI

---

# **萤石开放平台 ERTC-SDK接入引导**

## 1.简介

视频通话 SDK 可实现纯语音通话和视频通话功能，该SDK基于萤石ERTC产品组装，开发者可参考[ERTC相关功能及能力](https://open.ys7.com/help/1874)

## 1.2.版本更新记录

| 版本 | 日期 | 更新内容 |
| --- | --- | --- |
| v4.8.0 | 2025-05 | 新增 `EZRTC_SetAudioInfo` 接口，支持 Opus-16K 采样率配置；新增 `ERTCAudioInfo` 结构体 |
| v4.6.0 | 2025-03 | 支持萤石展厅星石数字人 |
| v4.3.0 | 2024-12 | 支持音频编码格式协商 |

## 2.前提条件

接入语言: C++  
控件名称: libertc  
开发环境:支持 aarch64-ca53-linux-gnu等嵌入式平台

## 3.功能介绍

| **功能名称** | **头文件** | **功能说明** |
| --- | --- | --- |
| 全局配置 | EzRtcInterface.h | 初始化，设置回调， 获取token |
| 房间管理 | EzRtcInterface.h | 进入房间，退出房间 |
| 音频管理 | EzRtcInterface.h | 开关本地音频，启用音量大小提示，配置音频参数 |
| 视频管理 | EzRtcInterface.h | 开关本地视频，订阅和取消远端视频 |
| 消息透传 | EzRtcInterface.h | 发送接收透传消息 |

---

## 4. v4.8.0 新增功能：音频采样率与帧时长配置

### 4.1 功能概述

v4.8.0 版本新增 `EZRTC_SetAudioInfo` 接口，支持在进房前配置音频编码的采样率和帧时长。主要应用场景：

- **Opus-16K 采样率**：适用于低带宽嵌入式设备（如启英泰伦芯片），在保证语音质量的前提下降低带宽消耗
- **自定义帧时长**：支持 10/20/40/60ms 帧时长配置，适配不同芯片的音频采集能力
- **接收端重采样**：支持配置接收端输出采样率，适配本地播放设备能力

### 4.2 新增结构体 ERTCAudioInfo

```
typedef struct ERTCAudioInfo {
    ERTCAudioEncodeType codecType;    ///< 编码类型：AAC/OPUS
    unsigned int inputSampleRate;     ///< 发送采样率：8000/16000/32000/48000（0=使用默认值）
    unsigned int frameDurationMs;     ///< 帧时长ms：10/20/40/60（0=默认20ms）
    unsigned int outputSampleRate;    ///< 接收输出采样率：8000/16000/32000/48000（0=保持原始采样率）
} ERTCAudioInfo;
```

**字段说明：**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| codecType | ERTCAudioEncodeType | 音频编码类型。`ERTCAudioEncodeTypeAAC`(1) 或 `ERTCAudioEncodeTypeOpus`(2) |
| inputSampleRate | unsigned int | 发送端采样率。支持 8000/16000/32000/48000，设为 0 使用默认值（AAC=16000, OPUS=48000） |
| frameDurationMs | unsigned int | 音频帧时长（毫秒）。支持 10/20/40/60，设为 0 使用默认值 20ms |
| outputSampleRate | unsigned int | 接收端输出采样率。支持 8000/16000/32000/48000，设为 0 保持原始采样率不做重采样 |

### 4.3 新增接口

```
/**
 * @brief 设置音频信息（进房前调用）
 * @param[in] info 音频信息指针，包含编码类型、采样率和帧时长
 * @return 0 表示成功，-1 表示失败（参数为空）
 * @note 该接口必须在 EZRTC_EnterRoom 之前调用
 */
ERTC_API int EZRTC_SetAudioInfo(const ERTCAudioInfo* info);

/**
 * @brief 设置音频信息 - 多会话模式（进房前调用）
 * @param[in] handle 会话句柄
 * @param[in] info   音频信息指针
 * @return 0 表示成功，-1 表示失败
 * @note 该接口必须在 EZRTC_MS_EnterRoom 之前调用
 */
ERTC_API int EZRTC_MS_SetAudioInfo(int handle, const ERTCAudioInfo* info);
```

### 4.4 接入要点

> 重要： EZRTC\_SetAudioInfo 必须在 EZRTC\_EnterRoom 之前调用，进房后设置无效。

1. **调用时序**：InitLib → SetAudioInfo → EnterRoom
2. **房间内编码格式一致**：同一房间内所有用户的 `codecType` 必须一致，否则无法正常通信
3. **采样率匹配**：发送端的 `inputSampleRate` 决定了推送音频数据的采样率要求，送入的 PCM/编码数据采样率需与此一致
4. **向后兼容**：不调用此接口时，行为与旧版本完全一致（AAC-16K / OPUS-48K）

### 4.5 代码示例

#### 示例1：Opus-16K 配置（推荐用于低带宽嵌入式设备）

```
// 初始化
EZRTC_InitLib();
EZRTC_SetConfigInfo(ERTCConfigLogLevel, ERTCLogLevelInfo);
EZRTC_SetLogCallback(OnERTCLog, this);

// 【v4.8.0 新增】配置 Opus-16K 音频参数
ERTCAudioInfo audioInfo;
memset(&audioInfo, 0, sizeof(ERTCAudioInfo));
audioInfo.codecType = ERTCAudioEncodeTypeOpus;   // 使用 Opus 编码
audioInfo.inputSampleRate = 16000;               // 发送采样率 16KHz
audioInfo.frameDurationMs = 20;                  // 帧时长 20ms
audioInfo.outputSampleRate = 16000;              // 接收输出也为 16KHz
int ret = EZRTC_SetAudioInfo(&audioInfo);
if (ret != 0) {
    Log("SetAudioInfo failed, ret:%d", ret);
}

// 设置回调
EZRTCCallBack callback;
memset(&callback, 0, sizeof(EZRTCCallBack));
callback.fnOnError = OnError;
callback.fnEnterRoom = OnEnterRoom;
callback.fnExitRoom = OnExitRoom;
callback.fnRemoteUserEnterRoom = OnRemoteUserEnterRoom;
callback.fnRemoteUserLeaveRoom = OnRemoteUserLeaveRoom;
callback.fnUserAudioAvailable = OnUserAudioAvailable;
callback.fnRemoteData = OnRemoteData;
callback.pUserData = this;
EZRTC_AddCallBack(&callback);
EZRTC_SetInputStartCallback(OnInputStart, this);

// 加入房间
ERTCRoomParams params;
memset(&params, 0, sizeof(params));
params.appId = (char*)appId.c_str();
params.roomId = (char*)roomId.c_str();
params.enterSig = (char*)token.c_str();
params.userId = (char*)userID.c_str();
ret = EZRTC_EnterRoom(&params);
```

#### 示例2：AAC-16K 配置（默认行为，无需额外设置）

```
// 不调用 EZRTC_SetAudioInfo，使用默认 AAC-16K 配置
// 等价于：
ERTCAudioInfo audioInfo;
memset(&audioInfo, 0, sizeof(ERTCAudioInfo));
audioInfo.codecType = ERTCAudioEncodeTypeAAC;
audioInfo.inputSampleRate = 16000;
audioInfo.frameDurationMs = 20;
audioInfo.outputSampleRate = 0;  // 0 = 保持原始采样率
EZRTC_SetAudioInfo(&audioInfo);
```

#### 示例3：多会话模式下配置音频参数

```
// 创建会话
int handle = 0;
EZRTC_CreateSession(&handle);

// 【v4.8.0 新增】多会话模式下配置音频参数
ERTCAudioInfo audioInfo;
memset(&audioInfo, 0, sizeof(ERTCAudioInfo));
audioInfo.codecType = ERTCAudioEncodeTypeOpus;
audioInfo.inputSampleRate = 16000;
audioInfo.frameDurationMs = 20;
audioInfo.outputSampleRate = 16000;
EZRTC_MS_SetAudioInfo(handle, &audioInfo);

// 设置回调
EZRTC_MS_SetCallBack(handle, &callback);

// 进入房间
ERTCRoomParams params;
memset(&params, 0, sizeof(params));
params.appId = (char*)appId.c_str();
params.roomId = (char*)roomId.c_str();
params.enterSig = (char*)token.c_str();
params.userId = (char*)userID.c_str();
EZRTC_MS_EnterRoom(handle, &params);
```

#### 示例4：推送 Opus-16K 音频数据

```
// OnInputStart 回调触发后，开始推送音频数据
void OnInputStart(void* userdata)
{
    // 开启本地音频
    EZRTC_MuteLocalAudio(false);
}

// 推送音频数据（Opus编码，16KHz采样率）
// 注意：送入的音频数据采样率需与 inputSampleRate 配置一致
void PushAudioFrame(unsigned char* opusData, int dataLen, unsigned int timestamp)
{
    ERTCInputAudioData data;
    memset(&data, 0, sizeof(ERTCInputAudioData));
    data.eStreamType = EZRTCInputStreamAudio;
    data.pData = opusData;
    data.nDataLen = dataLen;        // 单次送入长度不超过 1024 字节
    data.lTimestamp = timestamp;    // 时间戳（毫秒）
    EZRTC_InputAudioData(&data);
}
```

### 4.6 常见问题

| 问题 | 原因与解决方案 |
| --- | --- |
| SetAudioInfo 返回 -1 | info 参数为 NULL，请检查传入指针 |
| 进房后对端听不到声音 | 检查房间内所有用户的 codecType 是否一致 |
| 音频有杂音或变速 | 检查推送的音频数据采样率是否与 inputSampleRate 配置一致 |
| 接收端播放异常 | outputSampleRate 设置的值需要本地播放设备支持，建议设为 0 或与发送端一致 |

---

## 5. 实现视频通话

### 5.1 初始化流程

```
//初始化
EZRTC_InitLib();

//获取版本号
const char* sdkVer = EZRTC_GetSdkVersion();

//设置日志级别
EZRTC_SetConfigInfo(ERTCConfigLogLevel, ERTCLogLevelWarn); //设置WARN级别

//设置日志回调
EZRTC_SetLogCallback(OnERTCLog, this);

//【v4.8.0 新增】设置音频参数（可选，进房前调用）
ERTCAudioInfo audioInfo;
memset(&audioInfo, 0, sizeof(ERTCAudioInfo));
audioInfo.codecType = ERTCAudioEncodeTypeOpus;  // Opus编码
audioInfo.inputSampleRate = 16000;              // 16KHz采样率
audioInfo.frameDurationMs = 20;                 // 20ms帧时长
audioInfo.outputSampleRate = 16000;             // 接收输出16KHz
EZRTC_SetAudioInfo(&audioInfo);

//设置通用回调
EZRTCCallBack callback;
memset(&callback, 0, sizeof(EZRTCCallBack));
callback.fnOnError = OnError;
callback.fnEnterRoom = OnEnterRoom;
callback.fnExitRoom = OnExitRoom;
callback.fnRemoteUserEnterRoom = OnRemoteUserEnterRoom;
callback.fnRemoteUserLeaveRoom = OnRemoteUserLeaveRoom;
callback.fnUserAudioAvailable = OnUserAudioAvailable;
callback.fnUserVideoAvailable = OnUserVideoAvailable;
callback.fnRemoteData = OnRemoteData;
callback.fnRecvCustomMsg = OnRecvCustomMsg;
callback.pUserData = this;
EZRTC_AddCallBack(&callback);

//设置可推流回调
EZRTC_SetInputStartCallback(OnInputStart, this);    

//反初始化
EZRTC_FiniLib();
```

### 5.2 房间管理流程

```
//加入房间（异步接口，房间成功依赖加入消息通知）
ERTCRoomParams params;
memset(&params, 0, sizeof(params));
params.appId = (char*)appId.c_str();
params.roomId = (char*)roomId.c_str();
//资源token，生成规则和方法操作 https://open.ys7.com/help/1896
params.enterSig = (char*)token.c_str();
params.userId = (char*)userID.c_str();
int ret = EZRTC_EnterRoom(&params);
if (ret != 0)
{
    Log("enter room failed,ret:%d", ret);
    return ;
}

//加入房间成功消息通知
typedef void (*EZRTC_OnEnterRoom)(int result, void* userdata);

//加入房间失败消息通知
typedef void (*EZRTC_OnError)(int result, void* userdata);

//退出房间
EZRTC_ExitRoom();
```

### 5.3 音频管理流程

#### 5.3.1 音频本地接口

```
//【v4.8.0 推荐】使用 EZRTC_SetAudioInfo 替代 EZRTC_SetAudioEncodeType 进行音频配置
//旧接口仍然兼容：
//EZRTC_SetAudioEncodeType(ERTCAudioEncodeTypeOpus);

//新接口（支持采样率和帧时长配置）：
ERTCAudioInfo audioInfo;
memset(&audioInfo, 0, sizeof(ERTCAudioInfo));
audioInfo.codecType = ERTCAudioEncodeTypeOpus;
audioInfo.inputSampleRate = 16000;   // Opus-16K
audioInfo.frameDurationMs = 20;
audioInfo.outputSampleRate = 0;      // 保持原始采样率
EZRTC_SetAudioInfo(&audioInfo);

//开启本地音频(开启:false 关闭:true)
EZRTC_MuteLocalAudio(false);

//塞入音频数据，送入长度不要超过1024 (编码格式和采样率需与SetAudioInfo配置一致)
ERTCInputAudioData data;
data.eStreamType = EZRTCInputStreamAudio;
data.pData = opus-data;
data.nDataLen = opus-data-len;
data.lTimestamp = getcurtime();
EZRTC_InputAudioData(&data)
```

#### 5.3.2 音频远端接口

```
//远端收到音频能力消息，音频默认为自动订阅
typedef void (*EZRTC_OnUserAudioAvailable)(const char *userId, int available,void* userdata);


//订阅后，远端收到音频流数据回调,eDataType = ERTCClientDataAudioStream （默认回调出来的音频数据为混音后pcm数据）
//注意：如果设置了 outputSampleRate，回调的PCM数据将按照该采样率输出
typedef void (*EZRTC_OnRemoteData)(const char* userId, ERTCDataType eDataType, unsigned char* pStreamData, unsigned int uDataLen, void* userdata);
```

### 5.4 视频管理流程

#### 5.4.1 视频本地接口

```
//开启本地视频(开启:false 关闭:true)
EZRTC_MuteLocalVideo(false);

//塞入视频数据，送入长度不要超过1024 (H264或H265编码格式，房间内编码格式一致)
ERTCInputVideoData data;
data.eStreamType = EZRTCInputStreamVideo;
data.pData = h264-data;
data.nDataLen = h264-data-len;
data.lTimestamp = getcurtime();
data.codec = ERTCVideoCodecH264;
EZRTC_InputVideoData(&data)
```

#### 5.4.2 视频远端接口

```
//远端收到视频能力消息,某远端用户发布/取消了主路视频画面
typedef void (*EZRTC_OnUserVideoAvailable)(const char *userId, int available, void* userdata)

//远端订阅和取消远端视频,streamType可指定定义大流或者小流
EZRTC_MuteRemoteVideo(userId, streamType, false);    //订阅
EZRTC_MuteRemoteVideo(userId, streamType, true);    //取消订阅

//订阅后，远端收到流数据回调,,eDataType = ERTCClientDataVideoStream
typedef void (*EZRTC_OnRemoteData)(const char* userId, ERTCDataType eDataType, unsigned char* pStreamData, unsigned int uDataLen, void* userdata);
```

### 5.5 消息透传

```
//发送自定义消息给房间内所有用户
std::string msg = "hello wrold";
EZRTC_SendCustomMsg(msg.c_str(), msg.size());

//远端用户收到自定义消息的事件回调
typedef void (*EZRTC_OnRecvCustomMsg)(const char* userId, const unsigned char* message, unsigned int messageSize, void* userdata);
```

---

## 6. 接口调用时序图

```
┌──────────┐                              ┌──────────┐
│  应用层   │                              │ ERTC SDK │
└────┬─────┘                              └────┬─────┘
     │                                         │
     │─── EZRTC_InitLib() ───────────────────>│
     │                                         │
     │─── EZRTC_SetConfigInfo() ─────────────>│
     │                                         │
     │─── EZRTC_SetLogCallback() ────────────>│
     │                                         │
     │─── EZRTC_SetAudioInfo() ──────────────>│  ← 【v4.8.0 新增，进房前调用】
     │                                         │
     │─── EZRTC_AddCallBack() ───────────────>│
     │                                         │
     │─── EZRTC_SetInputStartCallback() ─────>│
     │                                         │
     │─── EZRTC_EnterRoom() ─────────────────>│
     │                                         │
     │<── OnEnterRoom(0) ─────────────────────│  (进房成功)
     │                                         │
     │<── OnInputStart() ─────────────────────│  (可以开始推流)
     │                                         │
     │─── EZRTC_MuteLocalAudio(false) ───────>│
     │─── EZRTC_InputAudioData() ────────────>│  (循环推送)
     │                                         │
     │─── EZRTC_ExitRoom() ──────────────────>│
     │                                         │
     │─── EZRTC_FiniLib() ───────────────────>│
     │                                         │
```