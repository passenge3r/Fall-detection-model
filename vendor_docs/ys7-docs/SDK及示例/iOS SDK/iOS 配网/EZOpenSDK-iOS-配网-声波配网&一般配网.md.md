# EZOpenSDK-iOS-配网-声波配网&一般配网.md

> EZOpenSDK-iOS-配网-声波配网&一般配网

> 更新时间: 2026-06-02T14:03:52.000+08:00

> 文档ID: 4099 | 来源树: SDK及示例

---

# 声波配网 & 一般配网（Smart）

声波配网：设备通过发出特定频率的声波，用户使用手机等设备接收并解析声波，从而实现配网。

一般配网（Smart）：让设备能够快速、轻松地连接到网络，SDK会根据设备自动选择配网模式，自动配网。

声波配网 和 一般配网（Smart）的流程是一样的，只是入参区别。

## 配网流程

### 1. 第一步查询设备信息

查询设备信息probeDeviceInfo:deviceType:completion:接口所获得对象是EZProbeDeviceInfo，正常查询到设备信息对象说明查询成功。

EZOpenSDK.h

```
/**
 *  查询设备信息（用于添加设备之前, 简单查询设备信息，如是否在线，是否添加等）
 *
 *  @param deviceSerial 设备序列号
 *  @param deviceType     设备型号，无法获取到设备型号则可传nil
 *  @param completion     回调block，正常时返回EZProbeDeviceInfo对象，错误码返回错误码
 *  @see 全新的设备是没有注册到平台的，所以会出现设备不存在的情况，设备wifi配置成功以后会上报数据到萤石云平台，以后每次查询就不会出现设备不存在的情况了。
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)probeDeviceInfo:(NSString *)deviceSerial
                               deviceType:(NSString *)deviceType
                               completion:(void (^)(EZProbeDeviceInfo *deviceInfo, NSError * __nullable error))completion;
```

  

**示例代码**：

```
[EZOpenSDK probeDeviceInfo:[GlobalKit shareKit].deviceSerialNo
                deviceType:[GlobalKit shareKit].deviceModel
                completion:^(EZProbeDeviceInfo *deviceInfo, NSError *error) {
    ...
    if (error) {
        if (error.code == EZ_HTTPS_DEVICE_ADDED_MYSELF ||
            error.code == EZ_HTTPS_DEVICE_ONLINE_ADDED ||
            error.code == EZ_HTTPS_DEVICE_OFFLINE_IS_ADDED_MYSELF) {
            // 您已添加过此设备
        } else if (error.code == EZ_HTTPS_DEVICE_ONLINE_IS_ADDED || error.code == EZ_HTTPS_DEVICE_OFFLINE_IS_ADDED) {
            // 此设备已被别人添加
        } else if (error.code == EZ_HTTPS_DEVICE_NOT_EXISTS) {
            // 此设备不存在
        } else if (error.code == EZ_HTTPS_DEVICE_OFFLINE_NOT_ADDED) {
            // 设备不在线,需连接网络
            if (deviceInfo) {
                deviceInfo.supportAP == 2;// 支持AP配网
                deviceInfo.supportWifi == 3;// 支持Smart配网
                deviceInfo.supportSoundWave == 1;// 支持声波配网
                deviceInfo.supportAPLink == 1;// 支持Link配网
                deviceInfo.supportAPType == 1;// 支持新协议AP配网，海外爱加设备专用
                // 记录该设备热点前缀
                [GlobalKit shareKit].WiFiConfigPrefix = [EZBusinessTool getWiFiConfigPrefix:deviceInfo.deviceHotSpot];
            } else {
                // 查不到能力级则根据设备灯来判断配网模式
            }
        } else {
            // 查询失败，网络不给力,可进行重试
        }
        return;
    }
    // 设备已在线，可进行添加
}];
```

### 2. 第二步配置设备网络

待设备提示配网时，调用startConfigWifi:password:deviceSerial:verifyCode:mode:deviceStatus:发起配网

EZOpenSDK.h

```
/**
 *  WiFi配置开始接口
 *
 *  @param ssid         连接WiFi SSID
 *  @param password     连接WiFi 密码
 *  @param deviceSerial 连接WiFi的设备的设备序列号,批量配置时填nil
 *  @param mode         配网的方式，EZWiFiConfigMode中列举的模式进行任意组合,例如:EZWiFiConfigSmart|EZWiFiConfigWave
 *  @param statusBlock  返回设备序列号以及当前连接状态
 *
 *  @return YES/NO
 */
+ (BOOL)startConfigWifi:(NSString *)ssid
               password:(NSString *)password
           deviceSerial:(NSString *)deviceSerial
                   mode:(NSInteger)mode
           deviceStatus:(void (^)(EZWifiConfigStatus status, NSString *deviceSerial))statusBlock;
```

**示例代码**：

```
NSInteger mode = 0;
mode |= self.supportSmartMode?EZWiFiConfigSmart:0;
mode |= self.supportSoundMode?EZWiFiConfigWave:0;
[EZOpenSDK startConfigWifi:weakSelf.ssid
                  password:weakSelf.password
              deviceSerial:[GlobalKit shareKit].deviceSerialNo
                      mode:mode
              deviceStatus:^(EZWifiConfigStatus status, NSString *deviceSerial) {
                  if (status == DEVICE_WIFI_CONNECTING) {
                      weakSelf.enState = STATE_NONE;
                      [weakSelf createTimerWithTimeOut:60];// 开始计时
                  } else if (status == DEVICE_PLATFORM_REGISTED) {
                      weakSelf.enState = STATE_PLAT;
                      [weakSelf createTimerWithTimeOut:30];
                      if ([GlobalKit shareKit].deviceVerifyCode != nil) {
                          // 开始绑定操作
                      } else {
                          // 密码错误，弹框让用户重新输入验证码
                      }
                  }
              }];
```

### 3. 第三步添加设备到当前账号下

调用addDevice:deviceSerial:verifyCode:completion:接口进行设备添加。当状态为DEVICE\_PLATFORM\_REGISTED时方可添加成功。

EZOpenSDK.h

```
/**
 *  根据设备序列号和设备验证码添加设备接口
 *
 *  @param deviceSerial 设备序列号
 *  @param verifyCode   设备验证码
 *  @param completion   回调block，error为空时表示添加成功
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)addDevice:(NSString *)deviceSerial
                         verifyCode:(NSString *)verifyCode
                         completion:(void (^)(NSError * __nullable error))completion;
```