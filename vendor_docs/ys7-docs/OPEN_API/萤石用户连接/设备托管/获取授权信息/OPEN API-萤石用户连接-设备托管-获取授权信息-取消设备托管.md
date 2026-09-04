# OPEN API-萤石用户连接-设备托管-获取授权信息-取消设备托管

> 更新时间: 2026-07-09T13:46:47.000+08:00

> 文档ID: 826 | 来源树: OPEN_API

---

## 取消设备托管

- 接口功能

   开发者对托管的设备进行取消托管操作。

- 请求地址

`https://open.ys7.com/api/lapp/trust/cancel`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 开发者托管access\_token(da前缀)或者设备托管授权的access\_token(du前缀) | Y |
| Body | deviceSerials | String | 格式：“设备序列号:通道号”，多个设备以逗号分隔，最大5个 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/trust/cancel' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=du.xxxxx' \
--data-urlencode 'deviceSerials=D1:C1,D2:C2'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
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
| 200 | 成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 10004 | 用户不存在 |  |
| 10031 | 子账户或萤石用户没有权限 |  |
| 49999 | 数据异常 |  |