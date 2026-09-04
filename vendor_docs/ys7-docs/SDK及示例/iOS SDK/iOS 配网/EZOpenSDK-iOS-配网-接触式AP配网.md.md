# EZOpenSDK-iOS-配网-接触式AP配网.md

> EZOpenSDK-iOS-配网-接触式AP配网

> 更新时间: 2026-06-02T14:03:52.000+08:00

> 文档ID: 4100 | 来源树: SDK及示例

---

# 接触式AP配网

适用于防跌倒雷达设备、霍曼宠物喂食机等设备；该类设备无视频取流能力，设备标签上无二维码。

## 配网流程

### 1. 第一步获取配网token

EZOpenSDK.h

```
/**
 * 获取接触式AP配网token
 *
 * @param completion 回调
 *
 * @return operation
 */
+ (NSURLSessionDataTask *)getNewApConfigToken:(void(^)(EZConfigTokenInfo *tokenInfo, NSError * __nullable error))completion;
```

block回调的EZConfigTokenInfo对象如下

| 属性 | 含义 |
| --- | --- |
| userId | 用户id，暂未使用 |
| token | 接触式AP配网token，必要 |
| lbsDomain | 设备配网后注册平台，必要 |

### 2. 第二步连接设备热点（手动去设置里连接）

该类设备机身上无二维码，需要用户去设置-网络 页面连接上设备热点

### 3. 第三步获取设备信息

连接上设备热点后，回到应用，调用getAccessDeviceInfo:获取设备信息

EZOpenSDK.h

```
/**
 * 获取设备信息（需连接设备热点）
 *
 * @param handler 回调
 */
+ (void)getAccessDeviceInfo:(void(^)(EZAPDevInfo *devInfo, NSError * __nullable error))handler;
```

可以拿到设备的序列号EZAPDevInfo.devSubserial，后面查询设备配网结果用

### 4. 第四步配置设备网络

```
/**
 * 开始NewAP配网（需连接设备热点）
 * @param token 配网token
 * @param ssid WiFi ssid
 * @param password WiFi 密码
 * @param lbsDomain lbs 域名
 * @param handler 回调
 *
 * @return 成功或失败
 */
+ (BOOL)startNewApConfigWithToken:(NSString *)token
                             ssid:(NSString *)ssid
                         password:(NSString *)password
                        lbsDomain:(NSString *)lbsDomain
                completionHandler:(void(^)(EZNewAPConfigStatus status, NSError * __nullable error))handler;
```

入参token 和 lbsDomain 传入第一步中获取到的值。

**示例代码**：

EZOpenSDK.h

```
[EZOpenSDK startNewApConfigWithToken:configToken
                                ssid:self.tf_ssid.text password:self.tf_password.text
                           lbsDomain:self.tokenInfo.lbsDomain
                   completionHandler:^(EZNewAPConfigStatus status, NSError * _Nonnull error) {
    NSLog(@"EZNewAPConfigStatus result--->%ld", (long)status);
    switch (status) {
        case EZNewAPConfigStatusConnectSuccess:
        case EZNewAPConfigStatusUnknow:
            // 步骤5：设备联网成功或者未知错误(某些型号设备无返回值)的时候发起轮询设备的绑定情况
            self.mTimer = [NSTimer scheduledTimerWithTimeInterval:5 target:self selector:@selector(searchDeviceFromService) userInfo:nil repeats:YES];
            break;
        case EZNewAPConfigStatusPasswordError:
            
            break;
        case EZNewAPConfigStatusNoAPFound:
            
            break;
            
        default:
            break;
    }
}];
```

### 5. 第五步轮询设备绑定状态

EZOpenSDK.h

```
/**
 * 查询设备绑定状态
 * @param deviceSerial 设备序列号
 * @param completion 回调block，正常时返回isBindSuccess，错误码返回错误码
 *
 * @return 成功或失败
 */
+ (NSURLSessionDataTask *)queryPlatformBindStatus:(NSString *)deviceSerial
                                       completion:(void(^)(BOOL isBindSuccess, NSError * __nullable error))completion;
```

isBindSuccess == YES时，说明设备绑定到账号成功了。

**详见Demo代码中的EZTouchAPViewController.m类实现。**