# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-查询灯光唤醒

> 更新时间: 2026-07-06T13:49:12.000+08:00

> 文档ID: 1166 | 来源树: OPEN_API

---

## 查询灯光唤醒

- 接口功能

   查询灯光唤醒。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/WakeUp`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/WakeUp' \
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
        "fade": 1116957405,
        "custom": false,
        "name": "",
        "repeatPeriod": [
          [
            210669479
          ]
        ],
        "action": [
          [
            {
              "endValue": "",
              "startValue": "",
              "uri": ""
            }
          ]
        ],
        "startTime": "",
        "sustain": 54032684,
        "enabled": false
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
| data | Array | 唤醒计划列表，取值范围[0,] |
| data.fade | Integer | 淡入时间 |
| data.custom | Boolean | 自定义 |
| data.name | String | 唤醒计划名称，取值范围[1,] |
| data.repeatPeriod | Array | 重复周期（为空，执行一次），取值范围[0,] |
| data.action | Array | 计划操作内容，取值范围[0,] |
| data.action.endValue | String | 执行动作的identifier的值（根据具体协议，通过string解析到具体的类型），取值范围[1,] |
| data.action.startValue | String | 执行动作的identifier的值（根据具体协议，通过string解析到具体的类型），取值范围[1,] |
| data.action.uri | String | 执行动作URI，取值范围[1,] |
| data.startTime | String | 触发时间，取值范围[1,] |
| data.sustain | Integer | 持续时间 |
| data.enabled | Boolean | 使能开关 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |