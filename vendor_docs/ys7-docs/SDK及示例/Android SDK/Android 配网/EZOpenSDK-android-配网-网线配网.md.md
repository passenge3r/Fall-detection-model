# EZOpenSDK-android-配网-网线配网.md

> EZOpenSDK-android-配网-网线配网

> 更新时间: 2026-06-02T14:03:43.000+08:00

> 文档ID: 4176 | 来源树: SDK及示例

---

# 网线配网

给设备插上网线，待设备提示注册平台成功后，直接调用EZOpenSDK.addDevice发起绑定操作即可。

EZOpenSDK

```
/**
 * 添加设备
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @param verifyCode   设备验证码，验证码位于设备机身上，6位大写字母
 * @return true 表示成功， false 表示失败
 * @throws BaseException
 */
public boolean addDevice(String deviceSerial, String verifyCode) throws BaseException;
```