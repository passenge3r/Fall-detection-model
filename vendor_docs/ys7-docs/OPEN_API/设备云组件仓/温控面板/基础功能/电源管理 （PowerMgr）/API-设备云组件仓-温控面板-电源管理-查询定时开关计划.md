# API-设备云组件仓-温控面板-电源管理-查询定时开关计划

> 更新时间: 2026-07-06T13:44:31.000+08:00

> 文档ID: 1022 | 来源树: OPEN_API

---

## 查询开关定时计划

- 接口功能

   该接口用于查询开关定时计划。本文档仅适用于设备型号 CS-HAE-PV3-NWG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/PowerMgr/PowerSwitchTimePlan`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/PowerMgr/PowerSwitchTimePlan' \
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
                "name": "",
                "repeatPeriod": [
                    [
                        1
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
                "startTime": "2021-01-28T02:00:00+08:00",
                "sustain": 0,
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
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Array | 开关定时计划，取值范围[0,16] |
| data[].name | String | 计划名称，取值范围[0,64] |
| data[].repeatPeriod | Array | 重复周期，取值范围[0,16] |
| data[].action | Array | 计划操作内容，取值范围[0,16] |
| data[].startTime | String | 触发时间，取值范围[0,64] |
| data[].sustain | Integer | 持续时间，取值范围[0,2147483647] |
| data[].enabled | Boolean | 使能开关 |
| data[].action[].endValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,64] |
| data[].action[].startValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,64] |
| data[].action[].uri | String | 执行动作URI，取值范围[0,1024] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |