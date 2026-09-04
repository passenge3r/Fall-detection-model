# API-设备云组件仓-T4C火灾探测报警器-基础功能-网关声音提醒设置-设置网关声音提醒状态

> API-设备云组件仓-T4C火灾探测报警器-基础功能-网关声音提醒设置-设置网关声音提醒状态

> 更新时间: 2026-06-30T17:55:13.000+08:00

> 文档ID: 1449 | 来源树: OPEN_API

---

## 设置网关声音提醒状态

- 接口功能

   设置T4C火灾探测报警器的网关声音提醒状态。本文档仅适用于设备型号 CS-T4C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/GatewayRemind/SoundRemindStatus`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Boolean | 网关声音提醒状态，true=开启，false=关闭 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/L12345678/SmokeSensor/0/GatewayRemind/SoundRemindStatus' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw 'true'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "成功",
        "moreInfo": {
            "deviceMeta": {
                "code": "0x00000000",
                "errorMsg": "Succeeded."
            }
        }
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，200表示成功 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码，0x00000000表示成功 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | -- | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |