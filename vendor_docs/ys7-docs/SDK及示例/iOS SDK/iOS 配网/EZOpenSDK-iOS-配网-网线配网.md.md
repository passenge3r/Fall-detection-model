# EZOpenSDK-iOS-配网-网线配网.md

> EZOpenSDK-iOS-配网-网线配网

> 更新时间: 2026-06-02T14:03:53.000+08:00

> 文档ID: 4101 | 来源树: SDK及示例

---

# 网线配网

给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。

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