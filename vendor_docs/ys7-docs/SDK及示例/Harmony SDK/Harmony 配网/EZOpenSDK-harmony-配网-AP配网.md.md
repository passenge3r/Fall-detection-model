# EZOpenSDK-harmony-配网-AP配网.md

> EZOpenSDK-harmony-配网-AP配网

> 更新时间: 2026-06-02T14:04:00.000+08:00

> 文档ID: 4213 | 来源树: SDK及示例

---

# AP配网

AP（Access Point，无线接入点）配网是一种常见的摄像机或智能设备连接到Wi-Fi网络的方式。它通过创建一个临时的Wi-Fi热点（即AP模式），使设备能够更方便地获取Wi-Fi设置信息并连接到目标网络。

## AP配网流程图

![AP配网流程图](https://resource.eziot.com/group2/M00/01/07/CtwQF2iIZe6AbGC8AAEQrS5GLmU285.png)

## AP配网集成开发流程

### 1. 第一步权限配置

需申请【本地网络权限】，请参考[【Harmony-权限设置】](https://open.ys7.com/help/4190)中的第5条。

### 2. 第二步查询设备信息

查询设备信息probeDeviceInfo接口所获得对象是EZProbeDeviceInfo，正常查询到设备信息对象说明查询成功。

EZOpenSDK.ets

```
/**
  * 查询设备信息（用于添加设备之前, 简单查询设备信息，如是否在线，是否添加等）
  * @param deviceSerial  设备序列号
  * @param deviceType    设备型号，无法获取到设备型号则可传nil
  * @param callback      回调，正常时返回EZProbeDeviceInfo对象，错误码返回错误码
  * @see 全新的设备是没有注册到平台的，所以会出现设备不存在的情况，设备wifi配置成功以后会上报数据到萤石云平台，以后每次查询就不会出现设备不存在的情况了。
  */
static probeDeviceInfo(deviceSerial: string, deviceType: string,
  callback: (deviceInfo: EZProbeDeviceInfo, error: EZError) => void);
```

  

**示例代码**：

```
EZOpenSDK.probeDeviceInfo(GlobalKit.getInstance().deviceSerialNo, GlobalKit.getInstance()
  .deviceModel, (deviceInfo, error) => {
  this.showLoadingProgress = false
  this.showResultImage = true
  this.resultText = GlobalKit.getInstance().deviceSerialNo
  if (error) {
    if (error.code == EZErrorCode.EZ_HTTPS_DEVICE_ADDED_MYSELF ||
      // 您已添加过此设备
    } else if (error.code == EZErrorCode.EZ_HTTPS_DEVICE_ONLINE_IS_ADDED ||
      error.code == EZErrorCode.EZ_HTTPS_DEVICE_OFFLINE_IS_ADDED) {
      // 此设备已被别人添加
    } else if (error.code == EZErrorCode.EZ_HTTPS_DEVICE_NOT_EXISTS) {
      // 此设备不存在
    } else if (error.code == EZErrorCode.EZ_HTTPS_DEVICE_OFFLINE_NOT_ADDED) {
      // 设备不在线,需连接网络
      if (deviceInfo) {
        // 支持AP配网
        let supportAP: number = EZProbeDeviceInfo.supportAP(deviceInfo.supportExtJSON)
        this.supportApMode = supportAP == 2 || supportAP == 1
        // 记录该设备热点前缀
        GlobalKit.getInstance().WiFiConfigPrefix =
          EZBusinessTool.getWiFiConfigPrefix(EZProbeDeviceInfo.getDeviceHotSpot(deviceInfo.supportExtJSON))
      } else {
        // 查不到能力级则根据设备灯来判断配网模式
      }
      // do something
    } else {
      // 查询失败，网络不给力,可进行重试
    }
    return
  }
  // 设备已在线，可进行添加
})
```

**注意事项：**

萤石基线设备生成的热点前缀都是EZVIZ，定制设备生成的热点前缀可能是SoftAP或者其他，需要通过deviceInfo.deviceHotSpot属性来设置热点前缀。

代码示例：

EZBusinessTool.ets

```
/**
  * 获取设备热点前缀
  * @param deviceHotSpot 0-EZVIZ，1-SoftAP，2-CAMGO
  */
static getWiFiConfigPrefix(deviceHotSpot: number) {
  let WiFiConfigPrefix = 'EZVIZ'
  switch (deviceHotSpot) {
    case 1:
      WiFiConfigPrefix = 'SoftAP'
      break;
    case 2:
      WiFiConfigPrefix = 'CAMGO'
      break;
    default:
      break;
  }
  return WiFiConfigPrefix
}
```

### 3. 第三步配置设备网络

待设备提示配网时，调用startAPConfigWifi发起AP配网

EZOpenSDK.ets

```
/**
  * AP配网接口（封装了设备状态轮询步骤）
  * @param ssid          WiFi的ssid
  * @param password      WiFi的密码
  * @param deviceSerial  设备序列号
  * @param verifyCode    设备验证码
  * @param callback      结果回调，返回配网过程中的各种状态
  */
static startAPConfigWifi(ssid: string, password: string, deviceSerial: string, verifyCode: string,
  callback: (status: EZWifiConfigStatus, deviceSerial: string) => void);
```

**示例代码**：(详见EZAPWiFiConfigPage.ets类实现)

```
EZOpenSDK.startAPConfigWifi(this.routerParams.ssid, this.routerParams.password, GlobalKit.getInstance()
  .deviceSerialNo, GlobalKit.getInstance().deviceVerifyCode, (status, deviceSerial) => {
  switch (status) {
    case EZWifiConfigStatus.DEVICE_WIFI_SENT_SUCCESS: // 向设备发送WiFi信息成功
      // 等待设备配网
      EZLog.info(this.TAG, '向设备发送WiFi信息成功')
      EZToastUtil.showToast('向设备发送WiFi信息成功')
      break
    case EZWifiConfigStatus.DEVICE_WIFI_SENT_FAILED: // 向设备发送WiFi信息失败
      // 配网失败，可以重试
      EZLog.info(this.TAG, '配网失败，请稍后重试')
      EZToastUtil.showToast('配网失败，请稍后重试')
      this.showLoadingProgress = false
      break
    case EZWifiConfigStatus.DEVICE_PLATFORM_REGISTED: // 设备注册平台成功
      // TODO 将设备添加到自己账号下
      EZLog.info(this.TAG, '设备注册平台成功')
      EZToastUtil.showToast('设备注册平台成功')
      this.showLoadingProgress = false
      this.showAddBtn = true
      break
    case EZWifiConfigStatus.DEVICE_PLATFORM_REGIST_FAILED: // 设备注册平台失败
      // TODO 可以自行开启新一轮轮询
      EZLog.info(this.TAG, '设备注册平台失败')
      EZToastUtil.showToast('设备注册平台失败')
      this.showLoadingProgress = false
      break
  }
})
```

### 4. 第四步添加设备到当前账号下

调用addDevice接口进行设备添加。当状态为EZWifiConfigStatus.DEVICE\_PLATFORM\_REGISTED时方可添加成功。

EZOpenSDK.ets

```
/**
  * 根据设备序列号和设备验证码添加设备接口
  * @param deviceSerial  设备序列号
  * @param verifyCode    设备验证码
  * @param callback      回调，error为空时表示添加成功
  */
static addDevice(deviceSerial: string, verifyCode: string, callback: (error: EZError) => void);
```

**特别说明**： 账户下删除设备重新进行wifi配置并且添加时，请在重置设备等待2分钟以后再调用wifi配置的相关接口可以提高wifi配置的成功率，否则会降低成功率，因为重置设备以后我们平台将在2分钟内得到设备下线的状态，只有平台认为下线了，wifi配置成功率才会高。