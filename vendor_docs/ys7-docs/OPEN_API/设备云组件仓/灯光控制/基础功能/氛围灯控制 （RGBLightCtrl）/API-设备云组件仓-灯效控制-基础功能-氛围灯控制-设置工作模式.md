# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-设置工作模式

> 更新时间: 2026-07-06T13:49:22.000+08:00

> 文档ID: 1171 | 来源树: OPEN_API

---

## 设置工作模式

- 接口功能

   设置工作模式。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/WorkMode`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | String | 工作模式：white-白光灯，colour-彩光灯，scene-场景，music-音乐，取值范围[white,colour,scene,music] | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/WorkMode' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '"white"'
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
| meta.code | Integer | 服务响应状态码，参见返回码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |