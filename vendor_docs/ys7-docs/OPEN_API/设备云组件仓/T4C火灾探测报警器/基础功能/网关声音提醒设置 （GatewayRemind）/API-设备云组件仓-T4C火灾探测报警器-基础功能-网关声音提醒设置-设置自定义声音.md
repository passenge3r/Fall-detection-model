# API-设备云组件仓-T4C火灾探测报警器-基础功能-网关声音提醒设置-设置自定义声音

>  

> 更新时间: 2026-06-30T17:55:47.000+08:00

> 文档ID: 1455 | 来源树: OPEN_API

---

## 设置自定义声音

- 接口功能

   设置自定义声音。本文档仅适用于设备型号 CS-T4C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/GatewayRemind/CustomSound`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| header | Content-Type | String | application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | String | 音效，可选值[1,2,3,4,5]：1-叮咚，2-有人闯入，3-欢迎光临，4-请随时关门，5-请注意安全 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/GatewayRemind/CustomSound' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"data":"1"}'
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
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 更多响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |