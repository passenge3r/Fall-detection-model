# API-设备云组件仓-T21智能人体存在传感器-基础功能-人形侦测-设置有人长时间滞留声音提醒计划

> 更新时间: 2026-07-06T13:47:07.000+08:00

> 文档ID: 1101 | 来源树: OPEN_API

---

## 设置有人长时间滞留声音提醒计划

- 接口功能

   该接口用于设置有人长时间滞留声音提醒计划。本文档仅适用于设备型号 CS-T21-DG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/HumanDetection/LongStaySoundRemindPlan`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | plan | Array | 计划列表，取值范围[0,8] | Y |
| Body | enabled | Boolean | 定时计划总开关 | N |
| Body | plan[].name | String | 计划名称，取值范围[0,32] | N |
| Body | plan[].repeatPeriod | Array | 重复周期，为空，执行一次；取值范围[1,16] | Y |
| Body | plan[].action | Array | 计划操作内容，取值范围[1,8] | Y |
| Body | plan[].startTime | String | 触发时间，取值范围[1,32] | Y |
| Body | plan[].sustain | Integer | 持续时间，取值范围[0,1440] | Y |
| Body | plan[].enabled | Boolean | 使能开关 | Y |
| Body | plan[].action[].actionType | String | 执行动作，取值范围[1,2556] | Y |
| Body | plan[].action[].endValue | Boolean | 执行动作的identifier的值(根据具体协议定制，类型) | N |
| Body | plan[].action[].startValue | Boolean | 执行动作的identifier的值(根据具体协议定制，类型) | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/HumanDetection/LongStaySoundRemindPlan' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
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
                            "endValue": true,
                            "startValue": true
                        }
                    ]
                ],
                "startTime": "undefined",
                "sustain": 0,
                "enabled": false
            }
        ]
    ],
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
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |