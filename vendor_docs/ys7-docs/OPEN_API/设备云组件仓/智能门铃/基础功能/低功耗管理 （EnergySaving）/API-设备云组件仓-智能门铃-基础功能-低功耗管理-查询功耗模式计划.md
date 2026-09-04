# API-设备云组件仓-智能门铃-基础功能-低功耗管理-查询功耗模式计划

> 更新时间: 2026-07-06T17:45:25.000+08:00

> 文档ID: 871 | 来源树: OPEN_API

---

## 查询功耗模式计划

- 接口功能

   该接口用于查询功耗模式计划。本文档仅适用于设备型号 CS-CMT-CHIME-B，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Default/0/EnergySaving/EnergyModePlan`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Default/0/EnergySaving/EnergyModePlan' \
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
                    "repeatPeriod": [[2]],
                    "action": [
                        [
                            {
                                "actionType": "model/attribute/set/EnergySaving/EnergyModeCfg",
                                "startValue": "perf"
                            }
                        ]
                    ],
                    "startTime": "00:00:00",
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
| data.plan | Array | 计划列表，取值范围[0,8] |
| data.plan[].name | String | 计划名称，取值范围[0,32] |
| data.plan[].repeatPeriod | Array | 重复周期，为空执行一次，取值范围[1,16] |
| data.plan[].action | Array | 计划操作内容，取值范围[1,8] |
| data.plan[].startTime | String | 触发时间，取值范围[1,32] |
| data.plan[].sustain | Integer | 持续时间，取值范围[0,1440] |
| data.plan[].enabled | Boolean | 使能开关 |
| data.plan[].action[].actionType | String | 执行动作URI，取值范围[1,2556] |
| data.plan[].action[].startValue | String | 功耗类型，取值范围[perf,saving,super-saving,non-sleep,normal,user]：perf-性能模式，saving-省电模式，super-saving-超级省电模式，non-sleep-不休眠模式，normal-常规模式，user-用户模式 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |