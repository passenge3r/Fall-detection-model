# API-设备云组件仓-T51C温湿度传感器-基础功能-温湿度传感器管理-获取所有温湿度信息

> 更新时间: 2026-07-06T13:48:48.000+08:00

> 文档ID: 1150 | 来源树: OPEN_API

---

## 获取所有温湿度信息

- 接口功能

   获取所有温湿度信息。本文档仅适用于设备型号 CS-T51C-BG，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/TempHumiSensorMgr/GetTempHumiInfoList`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Null | 请求体为 null | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/TempHumiSensorMgr/GetTempHumiInfoList' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw 'null'
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
        "currentTime": "",
        "temperature": 0.0,
        "humidity": 0.0,
        "ID": 0
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
| data | Array | 获取所有温湿度信息输出，取值范围[0,16] |
| data.currentTime | String | 当前时间，取值范围[1,] |
| data.temperature | Number | 设备环境温度，取值范围[-273.0,1000.0] |
| data.humidity | Number | 设备环境湿度，取值范围[0.0,100.0] |
| data.ID | Integer | 温湿度传感器采集编号，取值范围[0,2147483647] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |