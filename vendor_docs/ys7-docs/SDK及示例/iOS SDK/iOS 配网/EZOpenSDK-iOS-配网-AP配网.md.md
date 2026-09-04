# EZOpenSDK-iOS-配网-AP配网.md

> EZOpenSDK-iOS-配网-AP配网

> 更新时间: 2026-06-02T14:03:52.000+08:00

> 文档ID: 4098 | 来源树: SDK及示例

---

# AP配网

AP（Access Point，无线接入点）配网是一种常见的摄像机或智能设备连接到Wi-Fi网络的方式。它通过创建一个临时的Wi-Fi热点（即AP模式），使设备能够更方便地获取Wi-Fi设置信息并连接到目标网络。

## AP配网流程图

![AP配网流程图](https://resource.eziot.com/group2/M00/01/07/CtwQF2iIZe6AbGC8AAEQrS5GLmU285.png)

## AP配网集成开发流程

### 1. 第一步权限配置

需申请【本地网络权限 & 定位权限】，配置Signing & Capabilities。请参考[【iOS-权限设置】](https://open.ys7.com/help/4076)中的第4、5。

### 2. 第二步查询设备信息

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

**注意事项：**

萤石基线设备生成的热点前缀都是EZVIZ，定制设备生成的热点前缀可能是SoftAP或者其他，需要通过deviceInfo.deviceHotSpot属性来设置热点前缀。

代码示例：

EZBusinessTool.m

```
/** 获取设备热点前缀
  * @param deviceHotSpot 0-EZVIZ，1-SoftAP，2-CAMGO
  */
+ (NSString *)getWiFiConfigPrefix:(NSInteger)deviceHotSpot {
    NSString *WiFiConfigPrefix = @"EZVIZ";
    switch (deviceHotSpot) {
        case 1:
            WiFiConfigPrefix = @"SoftAP";
            break;
        case 2:
            WiFiConfigPrefix = @"CAMGO";
            break;
            
        default:
            break;
    }
    return WiFiConfigPrefix;
}
```

### 3. 第三步连接设备热点

待设备提示配网时，连接上设备热点

**示例代码**：

```
/** 连接设备热点 */
- (void)connect2DeviceHotspot {
    // 系统>=11，可以自动连接热备热点
    // do something

    self.devicWifiName = [NSString stringWithFormat:@"%@_%@",[GlobalKit shareKit].WiFiConfigPrefix,[GlobalKit shareKit].deviceSerialNo];
    self.devicWifiPsw = [NSString stringWithFormat:@"%@_%@",[GlobalKit shareKit].WiFiConfigPrefix,[GlobalKit shareKit].deviceVerifyCode];

    // 创建将要连接的WIFI配置实例
    NEHotspotConfiguration *hotspotConfig;
    hotspotConfig = [[NEHotspotConfiguration alloc] initWithSSID:self.devicWifiName passphrase:self.devicWifiPsw isWEP:NO];
    // 开始连接 (调用此方法后系统会自动弹窗确认)
    [[NEHotspotConfigurationManager sharedManager] applyConfiguration:hotspotConfig completionHandler:^(NSError * _Nullable error) {
        // 系统api-applyConfiguration有bug，就算连接失败，error也是nil。需要判断下当前WiFi是否是热备热点，是的话才算连接成功
        if ([[EZCommonTool getWiFiName] isEqualToString:self.devicWifiName]) {
            NSLog(@"connect to device hotspot success");
            // 开始配网，见第三步
            [self startConfigWifi];
        } else {
            NSLog(@"connect to device hotspot failed");
            // do something
        }
    }];
}
```

### 4. 第四步配置设备网络

待连接设备热点连接成功后，调用startAPConfigWifiWithSsid:password:deviceSerial:verifyCode:deviceStatus:发起AP配网

EZOpenSDK.h

```
/**
 * AP配网接口（推荐，v5.0新增）
 * 封装了设备状态轮询步骤，轮询20次，5秒一次，一共100秒等待时间；如果感觉等待时间过长，可以使用以下两个方案：
 * 1.使用上面的接口，callback回调ret=YES 即代表成功将WiFi信息发送给设备，api任务结束，由应用层自行调用probeDeviceInfo:deviceType:completion:方法进行查询设备是否配网成功并注册到平台
 * 2.使用此api的同时，创建一个定时器，设置自己期望的一个超时时间。超时后调用stopAPConfigWifi，视为配网失败
 *
 * @param ssid WiFi的ssid
 * @param password WiFi的密码
 * @param deviceSerial 设备序列号
 * @param verifyCode 设备验证码
 * @param statusBlock 结果回调，返回配网过程中的各种状态
 *
 * @return 成功或失败
 */
+ (BOOL)startAPConfigWifiWithSsid:(NSString *)ssid
                         password:(NSString *)password
                     deviceSerial:(NSString *)deviceSerial
                       verifyCode:(NSString *)verifyCode
                     deviceStatus:(void (^)(EZWifiConfigStatus status, NSString *deviceSerial))statusBlock;
```

EZWifiConfigStatus状态通过回调的block获取，只需要处理以下4个枚举值即可，详见demo。

```
DEVICE_WIFI_SENT_SUCCESS // 向设备发送WiFi信息成功
DEVICE_WIFI_SENT_FAILED // 向设备发送WiFi信息失败
DEVICE_PLATFORM_REGISTED // 设备注册平台成功
DEVICE_PLATFORM_REGIST_FAILED // 设备注册平台失败
```

**示例代码**：

```
[EZOpenSDK startAPConfigWifiWithSsid:self.ssid
                            password:self.password
                        deviceSerial:[GlobalKit shareKit].deviceSerialNo
                          verifyCode:[GlobalKit shareKit].deviceVerifyCode
                        deviceStatus:^(EZWifiConfigStatus status, NSString * _Nonnull deviceSerial) {
    switch (status) {
        case DEVICE_WIFI_SENT_SUCCESS:// 向设备发送WiFi信息成功
            // 等待设备配网，如果wifi密码错误，最后会回调DEVICE_PLATFORM_REGIST_FAILED
            break;
        case DEVICE_WIFI_SENT_FAILED:// 向设备发送WiFi信息失败
            // 配网失败，可以重试
            break;
        case DEVICE_PLATFORM_REGISTED:// 设备注册平台成功
            // TODO 将设备添加到自己账号下
            NSLog(@"设备注册平台成功");
            [EZToast show:@"设备注册平台成功"];
            break;
        case DEVICE_PLATFORM_REGIST_FAILED:// 设备注册平台失败
            // TODO 可以自行开启新一轮轮询
            NSLog(@"设备注册平台失败");
            break;
        default:
            break;
    }
}];
```

### 5. 第五步添加设备到当前账号下

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

**特别说明**： 账户下删除设备重新进行wifi配置并且添加时，请在重置设备等待2分钟以后再调用wifi配置的相关接口可以提高wifi配置的成功率，否则会降低成功率，因为重置设备以后我们平台将在2分钟内得到设备下线的状态，只有平台认为下线了，wifi配置成功率才会高。