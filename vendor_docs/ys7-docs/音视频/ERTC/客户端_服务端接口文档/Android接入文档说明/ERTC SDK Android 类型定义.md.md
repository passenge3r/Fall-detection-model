# ERTC SDK Android 类型定义.md

> ERTC SDK Android 类型定义

> 更新时间: 2026-05-25T16:36:32.000+08:00

> 文档ID: 1828 | 来源树: 音视频

---

# ERTC SDK Android 类型定义

#### Updated Time 2023/08/30

## 常量定义 RTCConstant

### 1. 码流类型

| 类型 | 描述 |
| --- | --- |
| ERTC\_VIDEO\_STREAM\_TYPE\_NULL | 码流类型,未订阅 |
| ERTC\_VIDEO\_STREAM\_TYPE\_BIG | 码流类型,订阅大流 |
| ERTC\_VIDEO\_STREAM\_TYPE\_SMALL | 码流类型,订阅小流，当发布端未发布小流时会自动订阅大流，当发布端小流发布后，会自动切换成小流 |
| ERTC\_VIDEO\_STREAM\_TYPE\_SHARE | 订阅屏幕共享视频分享流 |

### 2. 填充模式

| 类型 | 描述 |
| --- | --- |
| ERTC\_VIDEO\_RENDER\_MODE\_FILL | 填充模式：即将画面内容居中等比缩放以充满整个显示区域，超出显示区域的部分将会被裁剪掉，此模式下画面可能不完整 |
| ERTC\_VIDEO\_RENDER\_MODE\_FIT | 适应模式：即按画面长边进行缩放以适应显示区域，短边部分会被填充为黑色，此模式下图像完整但可能留有黑边。 |

### 3. 网络质量类型

onNetworkQuality回调质量参数

| 类型 | 描述 |
| --- | --- |
| ERTC\_QUALITY\_UNKNOWN | 网络类型——未定义 |
| ERTC\_QUALITY\_EXCELLENT | 当前网络非常好 |
| ERTC\_QUALITY\_GOOD | 当前网络一般 |
| ERTC\_QUALITY\_POOR | 当前网络较差 |
| ERTC\_QUALITY\_BAD | 当前网络很差 |
| ERTC\_QUALITY\_VBAD | 当前网络不满足 ERTC 的最低要求 |
| ERTC\_QUALITY\_UNSUPPORTED | 暂时无法检测到网络质量 |
| ERTC\_QUALITY\_DETECTING | 网络质量检测已开始还没有完成 |

## 枚举定义

### 1. BavLogLevel

日志等级类型

| 类型 | 描述 |
| --- | --- |
| BAV\_LOG\_LEVEL\_OFF | 关闭 |
| BAV\_LOG\_LEVEL\_ERROR | ERROR级别 |
| BAV\_LOG\_LEVEL\_WARN | WARN级别 |
| BAV\_LOG\_LEVEL\_INFO | INFO级别 |
| BAV\_LOG\_LEVEL\_DEBUG | DEBUG级别 |
| BAV\_LOG\_LEVEL\_TRACE | TRACE级别 |

### 2. Scene

| 类型 | 描述 |
| --- | --- |
| VideoCall | 视频通话 |

### 3. ERTCVideoResolution

| 类型 | 描述 |
| --- | --- |
| ERTCVideoResolution\_120\_120 | 宽高比 1:1；分辨率 120x120；建议码率（VideoCall）80kbps; 建议码率（LIVE）120kbps |
| ERTCVideoResolution\_160\_160 | 宽高比 1:1；分辨率 120x120；建议码率（VideoCall）80kbps; 建议码率（LIVE）120kbps |
| ERTCVideoResolution\_270\_270 | 宽高比 1:1；分辨率 270x270；建议码率（VideoCall）200kbps; 建议码率（LIVE）300kbps |
| ERTCVideoResolution\_480\_480 | 宽高比 1:1；分辨率 480x480；建议码率（VideoCall）350kbps; 建议码率（LIVE）500kbps |
| ERTCVideoResolution\_160\_120 | 宽高比4:3；分辨率 160x120；建议码率（VideoCall）100kbps; 建议码率（LIVE）150kbps |
| ERTCVideoResolution\_240\_180 | 宽高比 4:3；分辨率 240x180；建议码率（VideoCall）150kbps; 建议码率（LIVE）250kbps |
| ERTCVideoResolution\_280\_210 | 宽高比 4:3；分辨率 280x210；建议码率（VideoCall）200kbps; 建议码率（LIVE）300kbps |
| ERTCVideoResolution\_320\_240 | 宽高比 4:3；分辨率 320x240；建议码率（VideoCall）250kbps; 建议码率（LIVE）375kbps |
| ERTCVideoResolution\_400\_300 | 宽高比 4:3；分辨率 400x300；建议码率（VideoCall）300kbps; 建议码率（LIVE）450kbps |
| ERTCVideoResolution\_480\_360 | 宽高比 4:3；分辨率 480x360；建议码率（VideoCall）400kbps; 建议码率（LIVE）600kbps |
| ERTCVideoResolution\_640\_480 | 宽高比 4:3；分辨率 640x480；建议码率（VideoCall）600kbps; 建议码率（LIVE）900kbps |
| ERTCVideoResolution\_960\_720 | 宽高比 4:3；分辨率 960x720；建议码率（VideoCall）1000kbps; 建议码率（LIVE）1500kbps |
| ERTCVideoResolution\_160\_90 | 宽高比 16:9；分辨率 160x90；建议码率（VideoCall）150kbps; 建议码率（LIVE）250kbps |
| ERTCVideoResolution\_256\_144 | 宽高比 16:9；分辨率 256x144；建议码率（VideoCall）200kbps; 建议码率（LIVE）300kbps |
| ERTCVideoResolution\_320\_180 | 宽高比 16:9；分辨率 320x180；建议码率（VideoCall）250kbps; 建议码率（LIVE）400kbps |
| ERTCVideoResolution\_480\_270 | 宽高比 16:9；分辨率 480x270；建议码率（VideoCall）350kbps; 建议码率（LIVE）550kbps |
| ERTCVideoResolution\_640\_360 | 宽高比 16:9；分辨率 640x360；建议码率（VideoCall）500kbps; 建议码率（LIVE）900kbps |
| ERTCVideoResolution\_960\_540 | 宽高比 16:9；分辨率 960x540；建议码率（VideoCall）850kbps; 建议码率（LIVE）1300kbps |
| ERTCVideoResolution\_1280\_720 | 宽高比 16:9；分辨率 1280x720；建议码率（VideoCall）1200kbps; 建议码率（LIVE）1800kbps |
| ERTCVideoResolution\_1920\_1080 | 宽高比 16:9；分辨率 1920x1080；建议码率（VideoCall）2000kbps; 建议码率（LIVE）3000kbps |

## 常用结构

### 1. RTCEngineConfig

初始化数据结构

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| context | Context | 上下文 |
| appId | String | appId |
| accessToken | String | accessToken |
| logPath | String | 日志路径，可以不设置 |
| logLevel | int | 日志等级 参考：com.ez.baselib.utils.LogUtil |

### 1. RTCConstant.EnterParam

入会数据结构

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | String | 用户 |
| roomId | String | 房间号 |
| token | String | token |

### 1. ERTCVideoEncParam

视频编码参数

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| videoResolution | ERTCVideoResolution | 视频分辨率 如需使用竖屏分辨率，请指定 resMode 为 Portrait，例如： 640 × 360 + Portrait = 360 × 640 |
| videoFps | int | 视频采集帧率 15fps或20fps。5fps以下，卡顿感明显。10fps以下，会有轻微卡顿感。20fps以上，会浪费带宽（电影的帧率为24fps） |
| videoBitrate | int | 目标视频码率，单位Kbps，SDK 会按照目标码率进行编码，只有在弱网络环境下才会主动降低视频码率 |

### 2. AudioVolumeInfo

音量信息参数

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | String | 说话者的 userId, 如果 userId 为0则代表是当前用户自己 |
| volume | int | 说话者的音量大小, 取值范围[0 - 100] |

### 3. ERTCLocalVideoStats

本地视频实时数据，质量监听时用

public void setRtcStatsListener(RTCStatsListener rtcStatsListener)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| width | int | 视频宽 |
| height | int | 视频高 |
| sentBitrate | int | 视频传输码率(上行) |
| sentFrameRate | int | 帧率大小 |
| streamType | int | 流类型 0：大码流 1：小码流 2：屏幕共享流 |
| packetCount | int | 发视频总包数 |
| compensateLossRate | int | 补偿后丢包率 |

### 4. ERTCLocalAudioStats

本地音频实时数据，质量监听时用

public void setRtcStatsListener(RTCStatsListener rtcStatsListener)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| sentBitrate | int | 音频传输码率 |
| packetLossRate | int | 音频丢包率 |
| packetCount | int | 发音频总包数 |

### 5. ERTCRemoteVideoStats

远程视频实时数据，质量监听时用

public void setRtcStatsListener(RTCStatsListener rtcStatsListener)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | String | 远端视频用户ID |
| receivedBitrate | int | 远端视频传输码率（下行） |
| receivedFrameRate | int | 远端帧率大小 |
| packetLossRate | int | 远端视频丢包率(下行) |
| totalFrozenTime | int | 远端视频总的卡顿时长 |
| frozenRate | int | 远端视频卡顿比 |
| streamType | int | 流类型 0：大码流 1：小码流 2：屏幕共享流 |
| width | int | 视频宽 |
| height | int | 视频高 |
| packetCount | int | 接收视频总包数 |
| uncompensateLoss | int | 视频补偿前丢包率（％） |

### ERTCRemoteAudioStats

远端音频实时数据，质量监听时用

public void setRtcStatsListener(RTCStatsListener rtcStatsListener)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | String | 远端视频用户ID |
| receivedBitrate | int | 远端音频传输码率（下行） |
| packetLossRate | int | 远端音频丢包率(下行) |
| totalFrozenTime | int | 远端音频总的卡顿时长 |
| frozenRate | int | 远端音频卡顿比 |
| packetCount | int | 接收音频总包数 |
| plcPacketCount | int | 音频帧补偿数量 |
| uncompensateLoss | int | 音频补偿前丢包率（％） |
| totalTime | int | 播放音频总时间 |

### SpeedTestResult

速度测试结果回调数据结构
public void setSpeedTestListener(RTCSpeedTestListener listener)

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| success | boolean | 测试是否成功 |
| quality | int | 内部通过评估算法测算出的网络质量 |
| upLostRate | int | 上行丢包率，取值范围是 [0 - 100]，例如 30% 表示每向服务器发送 10 个数据包可能会在中途丢失 3 个 |
| downLostRate | int | 下行丢包率，取值范围是 [0 - 100]，例如 20% 表示每从服务器收取 10 个数据包可能会在中途丢失 2 个 |
| rtt | int | 延迟（毫秒），指当前设备到 服务器的一次网络往返时间，该值越小越好，正常数值范围是10ms - 100ms |
| availableUpBandwidth | int | 上行带宽（kbps，-1：无效值） |
| availableDownBandwidth | int | 下行带宽（kbps，-1：无效值） |
| stsConnect | int | 流媒体服务器连接情况 |