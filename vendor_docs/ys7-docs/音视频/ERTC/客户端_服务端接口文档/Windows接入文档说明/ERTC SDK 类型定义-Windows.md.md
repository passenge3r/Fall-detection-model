# ERTC SDK 类型定义-Windows.md

> 更新时间: 2026-05-25T16:36:30.000+08:00

> 文档ID: 1916 | 来源树: 音视频

---

# ERTC 类型定义

#### Updated Time 2023/11/28

## 枚举定义

### ERTCLogLevel

日志级别

| 类型 | 描述 |
| --- | --- |
| ERTCLogLevelNone | 不输出任何 SDK Log |
| ERTCLogLevelError | 输出ERROR 级别的 Log |
| ERTCLogLevelWarn | 输出WARN 级别的 Log |
| ERTCLogLevelInfo | 输出INFO 级别的 Log |
| ERTCLogLevelDebug | 输出Debug 级别的 Log |
| ERTCLogLevelTrace | 输出TRACE 级别的 Log |

### ERTCVideoStreamType

视频流类型

| 类型 | 描述 |
| --- | --- |
| ERTCVideoStreamTypeBig | 高清大画面，一般用来传输摄像头的视频数据 |
| ERTCVideoStreamTypeSmall | 低清小画面：小画面和大画面的内容相互，但是分辨率和码率都比大画面低，因此清晰度也更低 |
| ERTCVideoStreamTypeSub | 辅流画面：一般用于屏幕分享，同一时间在同一个房间中只允许一个用户发布辅流视频，其他用户必须要等该用户关闭之后才能发布自己的辅流。 |

### ERTCVideoResolution

视频分辨率

| 类型 | 描述 |
| --- | --- |
| ERTCVideoResolution\_120\_120 | 宽高比 1:1；分辨率 120x120；建议码率（VideoCall）80kbps; 建议码率（LIVE）120kbps |
| ERTCVideoResolution\_160\_160 | 宽高比 1:1；分辨率 160x160；建议码率（VideoCall）80kbps; 建议码率（LIVE）120kbps |
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

### ERTCVideoFPS

视频帧率

| 类型 | 描述 |
| --- | --- |
| ERTCVideoFPS\_1 | 1 fps |
| ERTCVideoFPS\_5 | 5 fps |
| ERTCVideoFPS\_10 | 10 fps |
| ERTCVideoFPS\_11 | 11 fps |
| ERTCVideoFPS\_12 | 12 fps |
| ERTCVideoFPS\_13 | 13 fps |
| ERTCVideoFPS\_14 | 14 fps |
| ERTCVideoFPS\_15 | 15 fps |
| ERTCVideoFPS\_16 | 16 fps |
| ERTCVideoFPS\_17 | 17 fps |
| ERTCVideoFPS\_18 | 18 fps |
| ERTCVideoFPS\_19 | 19 fps |
| ERTCVideoFPS\_20 | 20 fps |
| ERTCVideoFPS\_25 | 25 fps |
| ERTCVideoFPS\_30 | 30 fps |
| ERTCVideoFPS\_60 | 60 fps |

### ERTCVideoFillMode

视频画面填充模式

| 类型 | 描述 |
| --- | --- |
| ERTCVideoFillMode\_Fill | 填充模式：即将画面内容居中等比缩放以充满整个显示区域，超出显示区域的部分将会被裁剪掉，此模式下画面可能不完整 |
| ERTCVideoFillMode\_Fit | 适应模式：即按画面长边进行缩放以适应显示区域，短边部分会被填充为黑色，此模式下图像完整但可能留有黑边 |

### ERTCVideoMirrorType

视频的镜像类型

| 类型 | 描述 |
| --- | --- |
| ERTCVideoMirrorType\_Auto | 自动模式 |
| ERTCVideoMirrorType\_Enable | 强制开启镜像 |
| ERTCVideoMirrorType\_Disable | 强制关闭镜像 |

### ERTCQuality

网络质量

| 类型 | 描述 |
| --- | --- |
| ERTCQuality\_Unknown | 未定义 |
| ERTCQuality\_Excellent | 当前网络非常好 |
| ERTCQuality\_Good | 当前网络比较好 |
| ERTCQuality\_Poor | 当前网络一般 |
| ERTCQuality\_Bad | 当前网络较差 |
| ERTCQuality\_Vbad | 当前网络很差 |
| ERTCQuality\_Down | 当前网络不满足 TRTC 的最低要求 |
| ERTCQuality\_Unsupported | 暂时无法检测到网络质量 |
| ERTCQuality\_Detecting | 网络质量检测已开始还没有完成 |

### ERTCConfigKey

配置类型

| 类型 | 描述 |
| --- | --- |
| ERTCConfigQualityInterval | 质量数据上抛时间间隔 |
| ERTCConfigInputVideoFilter | 本地视频采集处理设置，#ERTCVideoFilter |
| ERTCConfigPlayVideoFilter | 远端视频播放处理设置 |
| ERTCConfigServerLineId | 配置服务器线路选择(建议在初始化前设置)，#ERTCServerLineID |

## 常用结构

### ERTCLogConfig

日志配置信息

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| filePath | char\* | 码流文件存储路径 |
| level | ERTCLogLevel | 日志级别 |

### ERTCEngineContext

初始化配置

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| appId | char\* | 应用标识 |
| logConfig | ERTCLogConfig | 日志配置 |

### ERTCParams

进房参数

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | char\* | 用户标识 |
| roomId | char\* | 字符串房间号 |
| token | char\* | 用户签名 |

### ERTCVideoEncParam

视频编码参数

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| videoResolution | ERTCVideoResolution | 视频分辨率 如需使用竖屏分辨率，请指定 resMode 为 Portrait，例如： 640 × 360 + Portrait = 360 × 640 |
| videoFps | ERTCVideoFPS | 视频采集帧率 15fps或20fps。5fps以下，卡顿感明显。10fps以下，会有轻微卡顿感。20fps以上，会浪费带宽（电影的帧率为24fps） |
| videoBitrate | unsigned int | 目标视频码率，单位Kbps，SDK 会按照目标码率进行编码，只有在弱网络环境下才会主动降低视频码率 |

### ERTCVolumeInfo

音量大小

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | string | 说话者的 userId |
| volume | uint32\_t | 说话者的音量大小, 取值范围[0 - 100] |

### ERTCLocalVideoStats

本地视频质量数据

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| sentBitrate | uint32\_t | 视频传输码率(上行) |
| frameRate | uint32\_t | 帧率大小 |
| packetLossRate | uint16\_t | 视频丢包率 |
| streamType | ERTCVideoStreamType | 流类型 0：大码流 1：小码流 2：屏幕共享流 |
| width | uint32\_t | 视频宽 |
| height | uint32\_t | 视频高 |
| totalPacketCount | uint32\_t | 发视频总包数 |
| compensateLossRate | uint16\_t | 补偿后丢包率 |

### ERTCLocalAudioStats

本地音频质量数据

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| sentBitrate | uint32\_t | 音频传输码率 |
| packetLossRate | uint16\_t | 音频丢包率 |
| totalPacketCount | uint32\_t | 发音频总包数 |

### ERTCRemoteVideoStats

远端视频质量数据

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | string | 远端视频用户ID |
| receivedBitrate | uint32\_t | 远端视频传输码率（下行） |
| frameRate | uint32\_t | 远端帧率大小 |
| totalFrozenTime | uint32\_t | 远端视频总的卡顿时长 |
| videoFrozenRate | int32\_t | 远端视频卡顿比 |
| packetLossRate | uint16\_t | 视频丢包率 |
| streamType | ERTCVideoStreamType | 流类型 0：大码流 1：小码流 2：屏幕共享流 |
| width | uint32\_t | 视频宽 |
| height | uint32\_t | 视频高 |
| videoPacketCount | int32\_t | 接收视频总包数 |
| uncompensateLoss | uint16\_t | 视频补偿前丢包率（％） |

### ERTCRemoteAudioStatistics

远端音频实时数据

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| userId | string | 远端音频用户ID |
| receivedBitrate | uint32\_t | 远端音频传输码率（下行） |
| packetLossRate | uint32\_t | 远端音频丢包率(下行) |
| totalFrozenTime | uint32\_t | 远端音频总的卡顿时长 |
| totalFrozenTime | uint32\_t | 远端音频卡顿比 |
| totalPacketCount | int32\_t | 接收音频总包数 |
| plcPacketCount | uint32\_t | 音频帧补偿数量 |
| uncompensateLoss | uint32\_t | 音频补偿前丢包率（％） |
| totalTime | uint32\_t | 播放音频总时间 |

### ERTCSpeedTestParams

测速参数

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| expectedUpBandwidth | uint32\_t | 预期的上行带宽（kbps，取值范围： 10 ～ 5000，为 0 时不测试） |
| expectedDownBandwidth | uint32\_t | 预期的下行带宽（kbps，取值范围： 10 ～ 5000，为 0 时不测试） |
| testInterval | uint32\_t | 测试时间间隔（统计间隔（毫秒）,取值范围1000ms~60000ms） |

### ERTCSpeedTestResult

网络测速结果

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| success | BOOL | 测试是否成功 |
| quality | ERTCQuality | 网络质量 |
| upLostRate | uint32\_t | 上行丢包率，取值范围是 [0 - 100]，例如 30% 表示每向服务器发送 10 个数据包可能会在中途丢失 3 个 |
| downLostRate | uint32\_t | 下行丢包率，取值范围是 [0 - 100]，例如 20% 表示每从服务器收取 10 个数据包可能会在中途丢失 2 个 |
| rtt | int32\_t | 延迟（毫秒），指当前设备到 服务器的一次网络往返时间，该值越小越好，正常数值范围是10ms - 100ms |
| availableUpBandwidth | int | 上行带宽（kbps，-1：无效值） |
| availableDownBandwidth | int | 下行带宽（kbps，-1：无效值） |