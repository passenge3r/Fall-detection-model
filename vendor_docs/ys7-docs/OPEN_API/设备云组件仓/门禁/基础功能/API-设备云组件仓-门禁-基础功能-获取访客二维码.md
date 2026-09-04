# API-设备云组件仓-门禁-基础功能-获取访客二维码

> 更新时间: 2026-07-06T13:48:05.000+08:00

> 文档ID: 1124 | 来源树: OPEN_API

---

## 获取访客二维码

- 接口功能

   该接口用于获取有时效、有次数限制的访客二维码，支持子账号的Config权限。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/acs/person/qrcode/get`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Query | deviceSerial | String | 设备序列号 | Y |
| Query | empNo | String | 人员工号 | Y |
| Query | validPeriod | Integer | 二维码有效期,默认5分钟,最长不超过30分钟 | N |
| Query | maxSwipeTime | String | 开锁次数,最大4次,默认1次 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/acs/person/qrcode/get?deviceSerial=&empNo=&validPeriod=&maxSwipeTime=' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": ""
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| data | String | 二维码字符串,采用base64编码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |