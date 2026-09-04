# FLV SDK 错误码说明

> FLV SDK 错误码说明

> 更新时间: 2026-05-25T16:44:37.000+08:00

> 文档ID: 3709 | 来源树: SDK及示例

---

# FLV SDK Events 说明

### flvjs.Events

可以与`player.flv.on()`/`player.flv.off()`一起使用。它们需要前缀`flvjs.Events`。比如 `flvjs.Events.ERROR`

| 事件 | 描述 |
| --- | --- |
| ERROR | 播放过程中由于任何原因出现错误 |
| LOADING\_COMPLETE | 输入MediaDataSource已完全缓冲到结束 |
| RECOVERED\_EARLY\_EOF | 缓冲期间发生意外的网络EOF，但已自动恢复 |
| MEDIA\_INFO | 提供媒体的技术信息，如视频/音频编解码器、比特率等 |
| METADATA\_ARRIVED | 提供带有`onMetaData`标记的FLV文件（流）可以包含的元数据。 |
| SCRIPTDATA\_ARRIVED | 提供FLV文件（流）可以包含的脚本数据（OnCuePoint/OnTextData） |
| TIMED\_ID3\_METADATA\_ARRIVED | 提供包含私人数据（stream\_type=0x15）回调的定时ID3元数据包 |
| SMPTE2038\_METADATA\_ARRIVED | 提供包含私有数据回调的SMPTE2038元数据包 |
| SCTE35\_METADATA\_ARRIVED | 提供包含节（stream\_type=0x86）回调的SCTE35元数据数据包 |
| PES\_PRIVATE\_DATA\_ARRIVED | 提供包含专用数据（stream\_type=0x06）回调的ISO/IEC 13818-1 PES数据包 |
| STATISTICS\_INFO | 提供播放统计信息，如丢帧、当前速度等。 |

### flvjs.ErrotTypes

播放过程中可能出现的错误。它们需要前缀`flvjs.ErrorTypes`。比如`flvjs.ErrorTypes.NETWORK_ERROR`

| 错误类型 | 描述 |
| --- | --- |
| NETWORK\_ERROR | 与网络相关的错误 |
| MEDIA\_ERROR | 与网络相关的错误与媒体相关的错误（格式错误、解码问题等） |
| OTHER\_ERROR | 任何其他未指定的错误 |

### flvjs.ErrorDetails

任何其他未指定的错误为网络和媒体错误提供更详细的解释。它们需要前缀 `flvjs.ErrorDetails`。比如 `flvjs.ErrorDetails.NETWORK_EXCEPTION`

| 错误详情类型 | 描述 |
| --- | --- |
| NETWORK\_EXCEPTION | 与网络的任何其他问题有关；包含`message` |
| NETWORK\_STATUS\_CODE\_INVALID | 与无效的HTTP状态代码相关，如403、404等 |
| NETWORK\_TIMEOUT | R与超时请求问题相关 |
| NETWORK\_UNRECOVERABLE\_EARLY\_EOF | 与无法恢复的意外网络EOF有关 |
| MEDIA\_MSE\_ERROR | 与MediaSource的错误有关，如解码问题 |
| MEDIA\_FORMAT\_ERROR | 与媒体流中的任何无效参数相关 |
| MEDIA\_FORMAT\_UNSUPPORTED | 不支持输入MediaDataSource格式 |
| MEDIA\_CODEC\_UNSUPPORTED | 媒体流包含不支持的视频/音频编解码器 |