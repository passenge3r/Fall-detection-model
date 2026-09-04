# EZOpenSDK-harmony-配网-网线配网.md

> EZOpenSDK-harmony-配网-网线配网

> 更新时间: 2026-06-02T14:04:00.000+08:00

> 文档ID: 4216 | 来源树: SDK及示例

---

# 网线配网

给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。

EZOpenSDK

```
/**
 * 根据设备序列号和设备验证码添加设备接口
 * @param deviceSerial  设备序列号
 * @param verifyCode    设备验证码
 * @param callback      回调，error为空时表示添加成功
 */
static addDevice(deviceSerial: string, verifyCode: string, callback: (error: EZError) => void);
```