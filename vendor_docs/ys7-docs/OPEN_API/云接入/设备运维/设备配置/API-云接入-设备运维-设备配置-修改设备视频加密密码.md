# API-云接入-设备运维-设备配置-修改设备视频加密密码

> API-云接入-设备运维-设备配置-修改设备视频加密密码

> 更新时间: 2026-05-25T16:40:18.000+08:00

> 文档ID: 699 | 来源树: OPEN_API

---

## 修改设备视频加密密码

- 接口功能

  该接口用于修改设备视频加密密码（**设备重置后修改的密码失效**）
- 请求地址

  `https://open.ys7.com/api/lapp/device/password/update`
- 请求方式

  `POST`
- 子账户token请求所需最小权限

  `"Permission":"Config"` `"Resource":"Cam:序列号:通道号"`
- 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| accessToken | String | 授权过程获取的access\_token | Y |
| deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| oldPassword | String | 设备旧的加密密码 | Y |
| newPassword | String | 设备新的加密密码，长度大超过12字节 | Y |

- HTTP请求报文

```
POST /api/lapp/device/password/update HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

accessToken=at.0v1ksxnqdu5lxc2fak3ctbiq0r3269y9&deviceSerial=596510666&oldPassword=AAAAAA&newPassword=BBBBBB
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20010 | 设备验证码错误 | 确认输入的旧密码是否正确 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 未知错误 | 设备返回其他错误码 |
| 60020 | 不支持该命令 | 确认设备是否支持修改视频预览密码 |