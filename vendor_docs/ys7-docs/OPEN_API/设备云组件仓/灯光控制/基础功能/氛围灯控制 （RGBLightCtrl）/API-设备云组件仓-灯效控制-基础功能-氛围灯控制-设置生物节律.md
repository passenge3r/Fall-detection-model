# API-设备云组件仓-灯效控制-基础功能-氛围灯控制-设置生物节律

> 更新时间: 2026-07-06T13:49:11.000+08:00

> 文档ID: 1165 | 来源树: OPEN_API

---

## 设置生物节律

- 接口功能

   设置生物节律。本文档仅适用于设备型号 CS-HAL-WD2-2C12G，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/Biorhythm`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | enable | Boolean | 使能开关 | Y |
| body | repeatPeriod | Array | 周期设置，取值范围[0,] | Y |
| body | gradientWay | String | 渐变方式：entireGradient-全程渐变，directGradient-直接渐变，取值范围[entireGradient,directGradient] | Y |
| body | rhythmPlan | Array | 节律计划列表，取值范围[0,] | Y |
| body | rhythmPlan.rhythmIcon | String | 节律图片，取值范围[1,] | Y |
| body | rhythmPlan.enable | Boolean | 是否执行 | Y |
| body | rhythmPlan.name | String | 名称，取值范围[1,] | Y |
| body | rhythmPlan.action | Array | 执行动作列表，取值范围[0,] | Y |
| body | rhythmPlan.action.endValue | Integer | 结束动作（固定值：100） | N |
| body | rhythmPlan.action.startValue | Integer | 开始动作（固定值：0） | Y |
| body | rhythmPlan.action.uri | String | 执行动作URI，取值范围[1,] | Y |
| body | rhythmPlan.startTime | String | 触发时间，取值范围[1,] | Y |
| body | rhythmPlan.sustain | Integer | 持续时间（秒） | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Light/1/RGBLightCtrl/Biorhythm' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "enable": true,
    "repeatPeriod": [
        [
            810144018
        ]
    ],
    "gradientWay": "",
    "rhythmPlan": [
        [
            {
                "rhythmIcon": "",
                "enable": true,
                "name": "",
                "action": [
                    [
                        {
                            "endValue": 106029979,
                            "startValue": 1108672136,
                            "uri": ""
                        }
                    ]
                ],
                "startTime": "",
                "sustain": 937511602
            }
        ]
    ]
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