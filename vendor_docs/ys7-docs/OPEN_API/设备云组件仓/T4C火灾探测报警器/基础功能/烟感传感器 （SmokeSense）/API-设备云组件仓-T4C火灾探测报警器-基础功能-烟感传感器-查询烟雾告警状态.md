# API-设备云组件仓-T4C火灾探测报警器-基础功能-烟感传感器-查询烟雾告警状态

> API-设备云组件仓-T4C火灾探测报警器-基础功能-烟感传感器-查询烟雾告警状态

> 更新时间: 2026-06-30T17:55:04.000+08:00

> 文档ID: 1438 | 来源树: OPEN_API

---

## 查询烟雾告警状态

- 接口功能

   查询烟感传感器的烟雾告警状态。本文档仅适用于设备型号 CS-T4C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/SmokeSense/SmokeSensorStatus`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/L12345678/SmokeSensor/0/SmokeSense/SmokeSensorStatus' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json'
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
    "data": 1
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
| data | Integer | 烟雾告警状态，范围[0,1,2]：0-正常，1-烟雾告警，2-设备故障 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |