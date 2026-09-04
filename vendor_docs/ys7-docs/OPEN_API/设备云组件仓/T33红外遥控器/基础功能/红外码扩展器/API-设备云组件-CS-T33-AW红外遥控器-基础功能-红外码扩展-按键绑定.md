# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外码扩展-按键绑定

> 更新时间: 2026-06-30T12:04:02.000+08:00

> 文档ID: 1654 | 来源树: OPEN_API

---

## 按键绑定

- 接口功能

   按键绑定

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/IrCodeExpend/BindKey`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | displayName | String | 按键展示名称，长度范围[1,] | N |
| body | icon | String | 按键图标，长度范围[1,] | N |
| body | localIndex | Int | 要绑定按键的遥控器资源的localIndex | N |
| body | key | String | 要绑定的key，长度范围[1,] | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/IrCodeExpend/BindKey' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "displayName": "",
    "icon": "",
    "localIndex": 1627398360,
    "key": ""
}'
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
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |