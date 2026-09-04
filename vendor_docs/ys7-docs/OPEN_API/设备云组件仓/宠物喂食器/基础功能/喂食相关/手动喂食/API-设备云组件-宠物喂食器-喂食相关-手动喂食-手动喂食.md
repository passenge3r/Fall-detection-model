# API-设备云组件-宠物喂食器-喂食相关-手动喂食-手动喂食

> 更新时间: 2026-06-30T11:49:15.000+08:00

> 文档ID: 1570 | 来源树: OPEN_API

---

## 手动喂食

- 接口功能

   属于自定义领域（global），可即时下发一次手动喂食。

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/global/ManualFeed`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Int | 喂食量，份额，一份份额约8-10g，取值范围[0,20]（请求体直接传整数值） | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/global/ManualFeed' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '1'
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