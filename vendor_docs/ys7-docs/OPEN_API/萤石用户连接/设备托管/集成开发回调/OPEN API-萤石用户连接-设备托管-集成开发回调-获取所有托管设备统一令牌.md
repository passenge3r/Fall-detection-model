# OPEN API-萤石用户连接-设备托管-集成开发回调-获取所有托管设备统一令牌

> 更新时间: 2026-07-09T13:46:34.000+08:00

> 文档ID: 822 | 来源树: OPEN_API

---

## 获取所有托管设备统一令牌

- 接口功能

   该接口主要是开发者通过appKey和appSecret获取设备托管权限token，该token主要是获取账户下所有被托管的设备，来源是多个C用户。

- 请求地址

`https://open.ys7.com/api/lapp/trust/device/v2/token/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | appKey | String | 开发者应用的key | Y |
| Body | appSecret | String | 开发者应用的secret | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/trust/device/v2/token/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'appKey=xxxxx' \
--data-urlencode 'appSecret=xxxxx'
```

- 返回数据

```
{
    "data": {
        "accessToken": "da.3q98ktuz49rerl7ebfewu7br07ove6y9-4u8opzpclp-1rwgjkn-zyy52a5vn",
        "expireTime": 1553851609869
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| data.accessToken | String | 返回授权托管token |
| data.expireTime | Long | 该token的过期时间，单位为毫秒数 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |
| 10001 | 参数异常 |  |
| 10005 | appkey异常 |  |
| 10017 | appkey不存在 |  |
| 10030 | appkey和appsecret不匹配 |  |