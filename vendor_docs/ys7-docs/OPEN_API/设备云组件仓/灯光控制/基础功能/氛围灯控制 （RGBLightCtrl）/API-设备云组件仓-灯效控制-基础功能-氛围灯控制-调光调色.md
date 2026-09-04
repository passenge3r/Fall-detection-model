# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-调光调色

> 更新时间: 2026-07-06T13:49:34.000+08:00

> 文档ID: 1178 | 来源树: OPEN_API

---

## 调光调色

- 接口功能

   调光调色。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/Light/1/RGBLightCtrl/BrightnessAndColor`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | brightness | Integer | 亮度，取值范围[0,100] | Y |
| body | colorTemperature | Integer | 色温，取值范围[2700,6500] | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/Light/1/RGBLightCtrl/BrightnessAndColor' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "brightness": 75,
    "colorTemperature": 4931
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
| meta.code | Integer | 服务响应状态码，参见返回码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | -- | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |