# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-设置灯光助眠

> 更新时间: 2026-07-06T13:49:25.000+08:00

> 文档ID: 1173 | 来源树: OPEN_API

---

## 设置灯光助眠

- 接口功能

   设置灯光助眠。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/HelpSleep`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | data | Array | 助眠计划列表，取值范围[0,] | Y |
| body | data.fade | Integer | 淡出时间 | Y |
| body | data.custom | Boolean | 自定义 | Y |
| body | data.name | String | 助眠计划名称，取值范围[1,] | N |
| body | data.repeatPeriod | Array | 重复周期（为空，执行一次），取值范围[0,] | Y |
| body | data.action | Array | 计划操作内容，取值范围[0,] | Y |
| body | data.action.endValue | String | 执行动作的identifier的值（根据具体协议，通过string解析到具体的类型），取值范围[1,] | N |
| body | data.action.startValue | String | 执行动作的identifier的值（根据具体协议，通过string解析到具体的类型），取值范围[1,] | Y |
| body | data.action.uri | String | 执行动作URI，取值范围[1,] | Y |
| body | data.startTime | String | 触发时间，取值范围[1,] | Y |
| body | data.enabled | Boolean | 使能开关 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/HelpSleep' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '[
    [
        {
            "fade": 1177671413,
            "custom": false,
            "name": "",
            "repeatPeriod": [
                [
                    527105274
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
            "enabled": false
        }
    ]
]'
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