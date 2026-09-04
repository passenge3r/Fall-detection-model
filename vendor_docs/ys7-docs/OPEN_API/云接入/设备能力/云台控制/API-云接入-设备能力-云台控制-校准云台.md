# API-云接入-设备能力-云台控制-校准云台

> 更新时间: 2026-07-09T13:39:01.000+08:00

> 文档ID: 686 | 来源树: OPEN_API

---

## 校准云台

- 接口功能

校准云台。设备能力集support\_ptz\_position\_correction 子账户和托管：支持PTZ权限

- 请求地址

`https://open.ys7.com/api/v3/device/ptz/manual/adjust`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 用户令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | localIndex | String | 通道号，ipc默认为1 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/ptz/manual/adjust' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'localIndex=1'
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
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |