# EZOpenSDK-android-获取设备信息.md

> EZOpenSDK-android-获取设备信息

> 更新时间: 2026-06-02T14:03:36.000+08:00

> 文档ID: 5190 | 来源树: SDK及示例

---

# 获取设备信息

SDK 提供了一组用于获取设备信息的 API 接口，开发者可以通过这些接口获取当前账号下的设备列表或单个设备的详细信息。返回的设备信息封装在 `EZDeviceInfo` 对象中，包含设备序列号、名称、在线状态、加密状态、能力集等丰富的设备属性。

## 获取设备列表

EZOpenSDK

```
/**
 * 获取用户的设备列表，返回EZDeviceInfo的对象数组，只提供设备基础数据
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param pageIndex 查询页index，从0开始
 * @param pageSize  每页数量（建议20以内）
 * @return 返回的EZDeviceInfo
 * @throws BaseException
 */
public List<EZDeviceInfo> getDeviceList(int pageIndex, int pageSize) throws BaseException;

/**
 * 获取用户的设备列表，返回EZDeviceInfo的对象数组，只提供设备基础数据（包含子设备）
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param pageIndex 查询页index，从0开始
 * @param pageSize  每页数量（建议20以内）
 * @return 返回的EZDeviceInfo
 * @throws BaseException
 */
public List<EZDeviceInfo> getDeviceListEx(int pageIndex, int pageSize) throws BaseException;
```

## 获取单个设备信息

```
/**
 * 获取单个设备信息
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @return 设备信息对象EZDeviceInfo，与getDeviceList中对象一致
 * @throws BaseException
 */
public EZDeviceInfo getDeviceInfo(String deviceSerial) throws BaseException;

/**
 * 获取单个设备信息（包含子设备）
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @return 设备信息对象EZDeviceInfo，与getDeviceList中对象一致
 * @throws BaseException
 */
public EZDeviceInfo getDeviceInfoEx(String deviceSerial) throws BaseException;
```

## EZDeviceInfo 类属性说明

### 基础属性

| 属性 | 类型 | 获取方法 | 说明 |
| --- | --- | --- | --- |
| deviceSerial | String | `getDeviceSerial()` | 设备9位序列号，`EZDeviceInfo` 的唯一标识符 |
| deviceName | String | `getDeviceName()` | 设备名称。IPC设备时与对应 `EZCameraInfo` 的 CameraName 一致 |
| deviceType | String | `getDeviceType()` | 设备型号，可判断设备为 IPC、DVR、报警设备或存储设备等 |
| category | String | `getCategory()` | 设备大类 |
| status | int | `getStatus()` | 在线状态：1-在线，2-不在线 |
| isEncrypt | int | `getIsEncrypt()` | 是否加密：0-不加密，1-加密 |
| defence | int | `getDefence()` | 布撤防状态。防护设备：0-睡眠，8-在家，16-外出；普通IPC：0-撤防，1-布防 |
| deviceVersion | String | `getDeviceVersion()` | 设备固件版本号 |
| deviceCover | String | `getDeviceCover()` | 设备封面图片 URL |
| addTime | long | `getAddTime()` | 设备被用户添加的时间，精确到毫秒 |
| cameraNum | int | `getCameraNum()` | 设备下的通道（camera）数量。IPC为1，4通道DVR为4，无camera设备为0 |
| detectorNum | int | `getDetectorNum()` | 设备下探测器数量，0表示不支持或未绑定探测器 |
| supportChannelNums | int | `getSupportChannelNums()` | 支持的通道数 |
| offlineNotify | int | `getOfflineNotify()` | 设备下线是否通知：0-不通知，1-通知 |

### 关联对象列表

| 属性 | 类型 | 获取方法 | 说明 |
| --- | --- | --- | --- |
| cameraInfoList | `List<EZCameraInfo>` | `getCameraInfoList()` | 设备通道列表，`cameraNum > 0` 时有效 |
| detectorInfoList | `List<EZDetectorInfo>` | `getDetectorInfoList()` | 设备探测器列表，`detectorNum > 0` 时有效 |
| subDeviceInfoList | `List<EZSubDeviceInfo>` | `getSubDeviceInfoList()` | 子设备列表（仅 Ex 接口返回） |

### 能力集查询方法

以下方法基于设备能力集（`supportExtShort`）进行判断，返回设备是否支持对应功能：

| 方法 | 返回类型 | 说明 |
| --- | --- | --- |
| `isSupportTalk()` | `EZTalkbackCapability` | 对讲能力： `EZTalkbackNoSupport`（不支持）、 `EZTalkbackFullDuplex`（全双工）、 `EZTalkbackHalfDuplex`（半双工） |
| `isSupportDefence()` | boolean | 是否支持布撤防 |
| `isSupportDefencePlan()` | boolean | 是否支持布防计划 |
| `isSupportPTZ()` | boolean | 是否支持云台控制 |
| `isSupportZoom()` | boolean | 是否支持光学缩放（镜头拉近放远） |
| `isSupportUpgrade()` | boolean | 是否支持固件升级 |
| `isSupportMirrorCenter()` | boolean | 是否支持中心镜像 |
| `isSupportAudioOnOff()` | boolean | 是否支持麦克风声音开关设置 |
| `isSupportSoundWave()` | boolean | 是否支持声波配网 |
| `isSupportPTZFocus()` | boolean | 是否支持云台焦距模式 |
| `isSupportPlaybackRate()` | boolean | 是否支持倍数回放 |
| `isSupportDirectInnerRelaySpeed()` | boolean | 内网直连下是否支持倍数回放 |
| `isSupportSDRecordDownload()` | boolean | 是否支持SD卡录像下载 |
| `isSupportSdCover()` | boolean | 是否支持SD卡视频封面 |
| `isSupportMultiChannel()` | boolean | 是否支持多通道（如C7、C60P等设备） |
| `isSupportDeviceAutoVideolevel()` | boolean | 是否支持自动清晰度 |
| `isSupportVideoMeeting()` | boolean | 是否支持视频会议 |

### 通用能力集查询

如果EZDeviceInfo类中未提供某些能力集的查询方法，请使用如下方式进行查询，index为能力集位数。
index对应能力集见 [能力集文档](https://open.ys7.com/help/77)

| 方法 | 返回类型 | 说明 |
| --- | --- | --- |
| `getSupportInt(int index)` | int | 根据能力集位数获取对应的 int 值 |
| `getSupportValue(int index)` | String | 根据能力集位数获取对应的原始字符串值 |

---