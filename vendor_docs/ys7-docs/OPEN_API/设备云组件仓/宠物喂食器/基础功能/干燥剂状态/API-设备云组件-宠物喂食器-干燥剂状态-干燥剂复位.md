# API-设备云组件-宠物喂食器-干燥剂状态-干燥剂复位

> 更新时间: 2026-06-30T11:53:20.000+08:00

> 文档ID: 1587 | 来源树: OPEN_API

---

## 干燥剂复位

- 接口功能

   属于自定义领域（global），可下发干燥剂复位指令。干燥剂手动更改为新的干燥剂时间。

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/global/DesiccantReset`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Boolean | 干燥剂复位指令（请求体直接传布尔值true） | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/global/DesiccantReset' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw 'true'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": null,
        "moreInfo": {
            "deviceMeta": {
                "code": "0",
                "errorMsg": null
            }
        }
    },
    "data": true
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Boolean | true-操作成功，false-操作失败 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |