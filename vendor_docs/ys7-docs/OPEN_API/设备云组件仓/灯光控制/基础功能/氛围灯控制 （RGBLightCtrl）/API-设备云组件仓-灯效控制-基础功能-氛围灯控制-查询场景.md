# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-查询场景

> 更新时间: 2026-07-06T13:49:27.000+08:00

> 文档ID: 1174 | 来源树: OPEN_API

---

## 查询场景

- 接口功能

   查询场景。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/Scene`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/Scene' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
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
  "data": [
    [
      {
        "transformSpeed": 68,
        "sceneID": "",
        "name": "",
        "colorBlock": [
          [
            {
              "brightness": 70,
              "color": "",
              "colorTemperature": 3441
            }
          ]
        ],
        "transformType": "",
        "enabled": true
      }
    ]
  ]
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
| data | Array | 自定义场景列表，取值范围[0,] |
| data.transformSpeed | Integer | 转换速度，取值范围[0,100] |
| data.sceneID | String | 场景ID，取值范围[1,] |
| data.name | String | 自定义场景名称，取值范围[1,] |
| data.colorBlock | Array | 循环色块列表，取值范围[0,] |
| data.colorBlock.brightness | Integer | 亮度，取值范围[1,100] |
| data.colorBlock.color | String | 颜色RGB代码，取值范围[1,] |
| data.colorBlock.colorTemperature | Integer | 色温，取值范围[2700,6500] |
| data.transformType | String | 转换方式：static-静态，jump-跳变，breathing-呼吸，取值范围[static,jump,breathing] |
| data.enabled | Boolean | 是否启用 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |