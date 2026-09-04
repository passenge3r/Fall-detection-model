# API-设备云组件仓-窗帘控制-窗帘控制领域-查询窗帘开合定时任务

> 更新时间: 2026-07-06T13:45:42.000+08:00

> 文档ID: 1056 | 来源树: OPEN_API

---

## 查询窗帘开合定时任务

- 接口功能

   该接口用于查询窗帘开合定时任务。本文档仅适用于设备型号 CS-HAW-MC3，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Curtain/0/CurtainCtrl/OpeningClosingTimePlan`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Curtain/0/CurtainCtrl/OpeningClosingTimePlan' \
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
    "data": {
        "plan": [
            [
                {
                    "name": "undefined",
                    "repeatPeriod": [
                        [
                            1
                        ]
                    ],
                    "action": [
                        [
                            {
                                "actionType": "undefined",
                                "endValue": false,
                                "startValue": 0
                            }
                        ]
                    ],
                    "startTime": "undefined",
                    "sustain": 0,
                    "enabled": false
                }
            ]
        ]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数，详细说明见下方字段 |
| data.plan | Array | 计划列表，取值范围[0,8] |
| data.plan[].name | String | 计划名称，取值范围[0,32] |
| data.plan[].repeatPeriod | Array | 重复周期，为空，执行一次；取值范围[1,16] |
| data.plan[].action | Array | 计划操作内容，取值范围[1,8] |
| data.plan[].startTime | String | 触发时间，取值范围[1,32] |
| data.plan[].sustain | Integer | 持续时间，取值范围[0,1440] |
| data.plan[].enabled | Boolean | 使能开关 |
| data.plan[].action[].actionType | String | 执行动作URI，取值范围[1,2556] |
| data.plan[].action[].endValue | Boolean | 执行动作的identifier的值(根据具体协议定制，类型) |
| data.plan[].action[].startValue | Integer | 0 - 表示关闭，取值范围[0,100] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |