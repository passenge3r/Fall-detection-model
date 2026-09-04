# EZOpenSDK-iOS-获取设备信息.md

> EZOpenSDK-iOS-获取设备信息

> 更新时间: 2026-06-02T14:03:46.000+08:00

> 文档ID: 5192 | 来源树: SDK及示例

---

# 获取设备信息

SDK 提供了一组用于获取设备信息的 API 接口，开发者可以通过这些接口获取当前账号下的设备列表或单个设备的详细信息。返回的设备信息封装在 `EZDeviceInfo` 对象中，包含设备序列号、名称、在线状态、加密状态、能力集等丰富的设备属性。

## 获取设备列表

EZOpenSDK

```
/**
 *  获取用户所有的设备列表
 *
 *  @param pageIndex  分页当前页码（从0开始）
 *  @param pageSize   分页每页数量（建议20以内）
 *  @param completion 回调block，正常时返回EZDeviceInfo的对象数组和设备总数，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getDeviceList:(NSInteger)pageIndex
                               pageSize:(NSInteger)pageSize
                             completion:(void (^)(NSArray *deviceList, NSInteger totalCount, NSError *error))completion;

/**
 *  获取用户所有的设备列表（包含子设备）
 *
 *  @param pageIndex  分页当前页码（从0开始）
 *  @param pageSize   分页每页数量（建议20以内）
 *  @param completion 回调block，正常时返回EZDeviceInfo的对象数组和设备总数，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getDeviceListEx:(NSInteger)pageIndex
                                 pageSize:(NSInteger)pageSize
                               completion:(void (^)(NSArray *deviceList, NSInteger totalCount, NSError *error))completion;
```

## 获取单个设备信息

```
/**
 *  根据序列号获取设备信息
 *
 *  @param deviceSerial 设备序列号
 *  @param completion   回调block，正常时返回EZDeviceInfo的对象，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getDeviceInfo:(NSString *)deviceSerial
                             completion:(void (^)(EZDeviceInfo *deviceInfo, NSError *error))completion;

/**
 *  根据序列号获取设备信息（包含子设备）
 *
 *  @param deviceSerial 设备序列号
 *  @param completion   回调block，正常时返回EZDeviceInfo的对象，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getDeviceInfoEx:(NSString *)deviceSerial
                               completion:(void (^)(EZDeviceInfo *deviceInfo, NSError *error))completion;
```

## EZDeviceInfo 类属性说明

### 基础属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| deviceSerial | NSString | 设备9位序列号，`EZDeviceInfo` 的唯一标识符 |
| deviceName | NSString | 设备名称。IPC设备时与对应 `EZCameraInfo` 的 CameraName 一致 |
| deviceType | NSString | 设备型号，可判断设备为 IPC、DVR、报警设备或存储设备等 |
| category | NSString | 设备大类 |
| status | NSInteger | 在线状态：1-在线，2-不在线 |
| isEncrypt | BOOL | 是否加密 |
| defence | NSInteger | 布撤防状态。防护设备：0-睡眠，8-在家，16-外出；普通IPC：0-撤防，1-布防 |
| deviceVersion | NSString | 设备固件版本号 |
| deviceCover | NSString | 设备封面图片 URL |
| addTime | NSDate | 设备被用户添加的时间 |
| cameraNum | NSInteger | 设备下的通道（camera）数量。IPC为1，4通道DVR为4，无camera设备为0 |
| detectorNum | NSInteger | 设备下探测器数量，0表示不支持或未绑定探测器 |
| devProtoEnum | NSInteger | 设备协议版本号类型：0-非国标，5-国标级联，6-国标 |

### 关联对象列表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| cameraInfo | NSArray | 设备通道列表，`cameraNum > 0` 时有效 |
| detectorInfo | NSArray | 设备探测器列表，`detectorNum > 0` 时有效 |
| subDeviceInfo | NSArray | 子设备列表（仅 Ex 接口返回） |

### 能力集属性

以下属性基于设备能力集进行判断，表示设备是否支持对应功能：

**注意**：以下属性均为计算型属性，须调用后才能查看具体的值。未调用时，查看EZDeviceInfo中的以下属性显示是NO

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| isSupportTalk | NSInteger | 对讲能力： 0-不支持， 1-全双工， 3-半双工， 4-同时支持全双工和半双工 |
| isSupportPTZ | BOOL | 是否支持云台控制 |
| isSupportZoom | BOOL | 是否支持光学缩放（镜头拉近放远） |
| isSupportPTZFocus | BOOL | 是否支持云台焦距模式 |
| isSupportAudioOnOff | BOOL | 是否支持麦克风声音开关设置 |
| isSupportMirrorCenter | BOOL | 是否支持中心镜像翻转 |
| isSupportSoundWave | BOOL | 是否支持声波配网 |
| isSupportPlaybackRate | BOOL | 是否支持倍数回放 |
| isSupportDirectInnerRelaySpeed | BOOL | 内网直连下是否支持倍数回放 |
| isSupportSDRecordDownload | BOOL | 是否支持SD卡录像下载 |
| isSupportSdCover | BOOL | 是否支持SD卡视频封面 |
| isSupportMultiChannel | BOOL | 是否支持多通道（如C7、C60P等设备） |
| isSupportDeviceAutoVideolevel | BOOL | 是否支持自动清晰度 |
| isSupportVideoMeeting | BOOL | 是否支持视频会议 |

### 通用能力集查询

如果EZDeviceInfo类中未提供某些能力集的查询属性，请使用如下方法进行查询，index为能力集位数。
index对应能力集见 [能力集文档](https://open.ys7.com/help/77)

| 方法 | 返回类型 | 说明 |
| --- | --- | --- |
| `- (int)getSupportInt:(int)index` | int | 根据能力集位数获取对应的 int 值 |
| `- (NSString *)getSupportValue:(int)index` | NSString | 根据能力集位数获取对应的原始字符串值 |

---