# API-云接入-设备运维-设备配置-配置人形追踪开关状态

> 更新时间: 2026-07-09T13:40:49.000+08:00

> 文档ID: 729 | 来源树: OPEN_API

---

## 配置人形追踪开关状态

- 接口功能

   功能描述：配置人形追踪开关接口

- 请求地址

`https://open.ys7.com/api/v3/device/switch/human/track`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 访问token | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | enable | Int | 是否启用：1-启用，0-不启用 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/switch/human/track' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'enable=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| moreInfo | String | 附加信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | SUCCESS |
| 10002 | token过期或异常 | ACCESS\_TOCKEN\_ERROR |
| 10031 | 子账号没有设备权限 | OPEN\_ACCOUNT\_HAS\_NOT\_PERMISSION |
| 20018 | 用户没有设备权限 | USER\_DEVICE\_NOT\_EXIST |
| 20002 | 设备不存在 | DEVICE\_NOT\_EXIST |
| 60020 | 设备不支持 | DEV\_IS\_COMMAND\_UNKNOWN |
| 20007 | 设备离线 | DEVICE\_OFF\_LINE |
| 20006 | 设备网络异常 | NET\_ERROR |
| 20008 | 设备响应超时 | DEVICE\_SO\_TIMEOUT |
| 49999 | 数据异常 | DATA\_ERROR |