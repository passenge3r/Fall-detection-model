# OPEN API-萤石用户连接-设备托管-集成开发回调-授权信息（设备）回调

> OPEN API-萤石用户连接-设备托管-集成开发回调-授权信息（设备）回调

> 更新时间: 2026-05-25T16:43:52.000+08:00

> 文档ID: 818 | 来源树: OPEN_API

---

## 授权信息（设备）回调

- 请求地址 Url:{callBackAddress}?opt\_type=opt&deviceSerials=deviceSerials&deviceTrustId=deviceTrustId
- 参数说明： Opt “device\_authorize” => 设备授权 “device\_cancel” => 取消授权 deviceSerials 用户操作的设备序列号 一般为 deviceSerial : channelNo, 多个设备直接 用 逗号(,)分隔 deviceTrustId 授权用户 id, 表示设备来源
- 请求方式 Get
- 返回信息 { "code": "200" }

注：返回上述信息,则开放平台认为开发者信息获取成功.返回其他任何信息,均认为失败.