# API-云直播-播放地址-播放地址接口（新）-失效播放地址

> API-云直播-播放地址-播放地址接口（新）-失效播放地址

> 更新时间: 2026-06-30T17:54:51.000+08:00

> 文档ID: 1415 | 来源树: OPEN_API

---

## 失效播放地址

- 接口功能

   该接口用于失效获取的播放地址。子账户token请求所需最小权限：Permission:Get Resource:dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/v2/live/address/disable`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号例如427734222，均采用英文符号，限制50个 | Y |
| body | channelNo | Integer | 通道号，非必选，默认为1 | N |
| body | urlId | String | 直播地址Id，位于直播地址中 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/v2/live/address/disable' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=C78957921' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'urlId=424610320514547712'
```

- 返回数据

```
{
    "msg": "Operation succeeded",
    "code": "200"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功，失效指定的直播地址 |
| 401 | Unauthorized | 未授权 |
| 403 | Forbidden | 禁止访问 |
| 404 | Not Found | 未找到 |