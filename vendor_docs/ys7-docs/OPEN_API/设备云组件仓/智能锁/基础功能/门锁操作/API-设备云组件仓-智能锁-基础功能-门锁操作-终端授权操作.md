# API-设备云组件仓-智能锁-基础功能-门锁操作-终端授权操作

> 更新时间: 2026-07-09T13:44:19.000+08:00

> 文档ID: 762 | 来源树: OPEN_API

---

## 终端授权操作

- 接口功能

   终端授权操作,支持子账号，设备级鉴权，权限为Config。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/endpoint/auth`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | endpointId | String | 终端id | Y |
| Body | endpointName | String | 终端名 | Y |
| Body | password | String | 主用户密码,如果不填需在锁上验证主用户密码 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/endpoint/auth' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'endpointId=xxxxx' \
--data-urlencode 'endpointName=xxxxx' \
--data-urlencode 'password=xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 返回消息 |
| code | String | 返回码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 49999 | 数据异常 |  |
| 10002 | accessToken过期或异常 |  |
| 10001 | 无效参数 |  |
| 10031 | 子账号或开发者用户无权限 |  |
| 20623 | 远程解锁开关未开启 |  |