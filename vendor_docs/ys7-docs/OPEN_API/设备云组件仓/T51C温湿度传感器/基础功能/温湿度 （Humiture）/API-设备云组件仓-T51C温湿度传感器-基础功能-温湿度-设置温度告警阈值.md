# API-设备云组件仓-T51C温湿度传感器-基础功能-温湿度-设置温度告警阈值

> 更新时间: 2026-07-06T13:48:33.000+08:00

> 文档ID: 1143 | 来源树: OPEN_API

---

## 设置温度告警阈值

- 接口功能

   设置温度告警阈值。本文档仅适用于设备型号 CS-T51C-BG，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/Humiture/TemperatureAlarmThreshold`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | maxTemperature | Number | 最大温度，取值范围[-100.0,150.0] | N |
| body | unit | String | 温度单位：celsius-摄氏度，fahrenheit-华氏度，取值范围[celsius,fahrenheit] | N |
| body | minTemperature | Number | 最小温度，取值范围[-100.0,150.0] | N |
| body | enabled | Boolean | 告警使能 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/Humiture/TemperatureAlarmThreshold' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "maxTemperature": 0.0,
    "unit": "celsius",
    "minTemperature": 0.0,
    "enabled": true
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