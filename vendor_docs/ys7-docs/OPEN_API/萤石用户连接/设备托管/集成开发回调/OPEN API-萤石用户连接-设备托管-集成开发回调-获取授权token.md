# OPEN API-萤石用户连接-设备托管-集成开发回调-获取授权token

> 更新时间: 2026-07-09T13:46:26.000+08:00

> 文档ID: 820 | 来源树: OPEN_API

---

## 获取授权token

- 接口功能

   该接口主要是开发者通过授权码获取授权信息，该token主要是用来获取单个用户下对应的托管设备。

- 请求地址

`https://open.ys7.com/api/lapp/trust/device/token/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | access\_token | String | 开发者accessToken | Y |
| Body | auth\_code | String | 授权码 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/trust/device/token/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'access_token=at.xxxxx' \
--data-urlencode 'auth_code=xxxxx'
```

- 返回数据

```
{
    "data": {
        "access_token": "du.2svbvjn82ycx5weh54slfbuebmn6im7o-3np7vpbklx-0zxzdhk-fkzgcpc84",
        "expires_in": 1541656437269,
        "refresh_token": "rt.99oz60qc8hn1jfwp9ml4nttid9u3w9h0-8s2wqprgxs-0zhci16-sssvtcmdk",
        "openId": "b4a3edff6af84a71b8a12912094359b5",
        "device_trust_id": "fdb5d9b9ad884edb84f62339ecc62d70"
    },
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| data.access\_token | String | 返回授权托管token |
| data.expires\_in | Long | 该token的过期时间，单位为毫秒数 |
| data.refresh\_token | String | 该token用来刷新授权托管token |
| data.openId | String | 授权码 |
| data.device\_trust\_id | String | 设备授权Id，用来标识授权用户 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |
| 1001 | 用户不存在 |  |
| 10002 | token过期或异常 |  |
| 10004 | 用户不存在 |  |
| 10015 | 用户未授权 |  |
| 70007 | 授权码不存在 |  |
| 80000 | 授权异常请重试 |  |
| 80002 | 授权码和token不匹配 |  |