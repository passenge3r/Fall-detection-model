# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外码扩展-设置学习状态

> 更新时间: 2026-06-30T12:03:57.000+08:00

> 文档ID: 1652 | 来源树: OPEN_API

---

## 设置学习状态

- 接口功能

   设置学习状态

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/IrCodeExpend/Learning`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Int | 学习状态，取值范围[0,1,2]：0-未在学习，1-正在学习，2-停止学习 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/IrCodeExpend/Learning' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '1'
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
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |