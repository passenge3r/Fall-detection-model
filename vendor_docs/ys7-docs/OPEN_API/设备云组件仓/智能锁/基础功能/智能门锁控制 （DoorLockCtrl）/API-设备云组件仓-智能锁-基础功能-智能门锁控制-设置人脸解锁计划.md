# API-设备云组件仓-智能锁-基础功能-智能门锁控制-设置人脸解锁计划

> 更新时间: 2026-07-09T13:45:22.000+08:00

> 文档ID: 778 | 来源树: OPEN_API

---

## 设置人脸解锁计划

- 接口功能

该接口用于通过传入计划列表（含 触发时间、持续时间、使用开关等参数）设置人脸锁人脸解锁计划。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/DoorLockCtrl/FaceUnlockPlan`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | plan | Array | 计划列表，取值范围[0,8]。计划列表中，相同重复周期其计划时间不能交叉或包含。如8点到22点计划设置了7天，8点到21点也设置了7天。两条重叠的计划，设备无法处理，会返回报错 | Y |
| Body | plan[].name | String | 计划名称，取值范围[0,32] | N |
| Body | plan[].repeatPeriod | Array | 重复周期，为空执行一次，取值范围[1,16]：0-周一、2-周二、...、6-周日 | Y |
| Body | plan[].action | Array | 计划操作内容，取值范围[1,8] | Y |
| Body | plan[].action[].actionType | String | 执行动作URI，取值范围[1,2556] | Y |
| Body | plan[].action[].endValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,256] | N |
| Body | plan[].action[].startValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,256] | Y |
| Body | plan[].startTime | String | 触发时间，取值范围[1,32]，格式：08:00 | Y |
| Body | plan[].sustain | Integer | 持续时间，取值范围[0,1440]，单位：分钟 | Y |
| Body | plan[].enabled | Boolean | 使能开关，true-使能，false-不使能 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/DoorLockCtrl/FaceUnlockPlan' \
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
                            "endValue": "",
                            "startValue": ""
                        }
                    ]
                ],
                "startTime": "undefined",
                "sustain": 0,
                "enabled": false
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
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |