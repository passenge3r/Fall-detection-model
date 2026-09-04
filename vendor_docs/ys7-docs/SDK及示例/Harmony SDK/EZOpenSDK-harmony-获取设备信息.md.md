# EZOpenSDK-harmony-获取设备信息.md

> EZOpenSDK-harmony-获取设备信息

> 更新时间: 2026-06-02T14:03:54.000+08:00

> 文档ID: 5193 | 来源树: SDK及示例

---

# 获取设备信息

SDK 提供了一组用于获取设备信息的 API 接口，开发者可以通过这些接口获取当前账号下的设备列表或单个设备的详细信息。返回的设备信息封装在 `EZDeviceInfo` 对象中，包含设备序列号、名称、在线状态、加密状态、能力集等丰富的设备属性。

## 获取设备列表

EZOpenSDK

```
/**
 * 获取用户所有的设备列表
 * @param pageIndex 分页当前页码（从0开始）
 * @param pageSize  分页每页数量（建议20以内）
 * @param callback  回调，正常时返回EZDeviceInfo的对象数组和设备总数，错误时返回错误码
 */
static getDeviceList(pageIndex: number, pageSize: number,
  callback: (deviceList: Array<EZDeviceInfo>, totalCount: number, error: EZError) => void)

/**
 * 获取用户所有的设备列表（包含子设备）
 * @param pageIndex 分页当前页码（从0开始）
 * @param pageSize  分页每页数量（建议20以内）
 * @param callback  回调，正常时返回EZDeviceInfo的对象数组和设备总数，错误时返回错误码
 */
static getDeviceListEx(pageIndex: number, pageSize: number,
  callback: (deviceList: Array<EZDeviceInfo>, totalCount: number, error: EZError) => void)
```

## 获取单个设备信息

```
/**
 * 根据序列号获取设备信息
 * @param deviceSerial 设备序列号
 * @param callback     回调，正常时返回EZDeviceInfo的对象，错误时返回错误码
 */
static getDeviceInfo(deviceSerial: string,
  callback: (deviceInfo: EZDeviceInfo, error: EZError) => void)

/**
 * 根据序列号获取设备信息（包含子设备）
 * @param deviceSerial 设备序列号
 * @param callback     回调，正常时返回EZDeviceInfo的对象，错误时返回错误码
 */
static getDeviceInfoEx(deviceSerial: string,
  callback: (deviceInfo: EZDeviceInfo, error: EZError) => void)
```

## EZDeviceInfo 类属性说明

### 基础属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| deviceSerial | string | 设备9位序列号，`EZDeviceInfo` 的唯一标识符 |
| deviceName | string | 设备名称。IPC设备时与对应 `EZCameraInfo` 的 CameraName 一致 |
| deviceType | string | 设备型号，可判断设备为 IPC、DVR、报警设备或存储设备等 |
| category | string | 设备大类 |
| status | number | 在线状态：1-在线，2-不在线 |
| isEncrypt | number | 是否加密：0-不加密，1-加密 |
| defence | number | 布撤防状态。防护设备：0-睡眠，8-在家，16-外出；普通IPC：0-撤防，1-布防 |
| deviceVersion | string | 设备固件版本号 |
| deviceCover | string | 设备封面图片 URL |
| cameraNum | number | 设备下的通道（camera）数量。IPC为1，4通道DVR为4，无camera设备为0 |
| detectorNum | number | 设备下探测器数量，0表示不支持或未绑定探测器 |
| devProtoEnum | number | 设备协议版本号类型：0-非国标，6-国标 |
| supportExtShort | string | 设备短能力集原始字符串 |
| abilities | Array<string> | 设备能力集数组（由 `supportExtShort` 解析而来） |

### 关联对象列表

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| cameraInfo | Array<EZCameraInfo> | 设备通道列表，`cameraNum > 0` 时有效 |
| detectorInfo | Array<EZDetectorInfo> | 设备探测器列表，`detectorNum > 0` 时有效 |
| subDeviceInfo | Array<EZSubDeviceInfo> | 子设备列表（仅 Ex 接口返回） |

### 能力集查询方法

鸿蒙 SDK 通过 `EzvizSupportKit` 工具类查询设备能力集，传入 `EZDeviceInfo.abilities` 数组进行判断：

```
import { EzvizSupportKit } from '@ohos/EZOpenSDK'

// 示例：判断设备是否支持云台控制
let supportPTZ = EzvizSupportKit.isSupportPTZ(deviceInfo.abilities)
```

| 方法 | 返回类型 | 说明 |
| --- | --- | --- |
| `EzvizSupportKit.isSupportTalk(abilities)` | number | 对讲能力： 0-不支持， 1-全双工， 3-半双工， 4-同时支持全双工和半双工 |
| `EzvizSupportKit.isSupportPTZ(abilities)` | boolean | 是否支持云台控制 |
| `EzvizSupportKit.isSupportZoom(abilities)` | boolean | 是否支持光学缩放（镜头拉近放远） |
| `EzvizSupportKit.isSupportPTZFocus(abilities)` | boolean | 是否支持云台焦距模式 |
| `EzvizSupportKit.isSupportAudioOnOff(abilities)` | boolean | 是否支持麦克风声音开关设置 |
| `EzvizSupportKit.isSupportMirrorCenter(abilities)` | boolean | 是否支持中心镜像翻转 |
| `EzvizSupportKit.isSupportSoundWave(abilities)` | boolean | 是否支持声波配网 |
| `EzvizSupportKit.isSupportPlaybackRate(abilities)` | boolean | 是否支持倍数回放 |
| `EzvizSupportKit.isSupportDirectInnerRelaySpeed(abilities)` | boolean | 内网直连下是否支持倍数回放 |
| `EzvizSupportKit.isSupportSDRecordDownload(abilities)` | boolean | 是否支持SD卡录像下载 |
| `EzvizSupportKit.isSupportSdCover(abilities)` | boolean | 是否支持SD卡视频封面 |
| `EzvizSupportKit.isSupportMultiChannel(abilities)` | boolean | 是否支持多通道（如C7、C60P等设备） |

### 通用能力集查询

如果 `EzvizSupportKit` 中未提供某些能力集的查询方法，请使用如下方式进行查询，index为能力集位数。
index对应能力集见 [能力集文档](https://open.ys7.com/help/77)

```
// 通过 EzvizSupportKit.getSupportInt 查询任意能力集位
let value = EzvizSupportKit.getSupportInt(index, deviceInfo.abilities)
```

| 方法 | 返回类型 | 说明 |
| --- | --- | --- |
| `EzvizSupportKit.getSupportInt(index, abilities)` | number | 根据能力集位数获取对应的 int 值 |

---