# EP查询心率异常消息提醒计划

> 更新时间: 2026-06-24T15:56:47.000+08:00

> 文档ID: 2085 | 来源树: OPEN_API

---

## 查询心率异常消息提醒计划

- 接口功能

   查询心率异常消息提醒计划（HeartAbnormityMsgRemindPlan）

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 用户访问令牌（[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html)） | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 资源描述，描述资源类型下的序号，示例值：0 | Y |
| header | resourceCategory | String | 资源种类，描述资源的类型，示例值：global | Y |
| header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，示例值：SleepDetector | Y |
| header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，示例值：HeartAbnormityMsgRemindPlan | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxxxxxxx' \
--header 'localIndex: 0' \
--header 'resourceCategory: global' \
--header 'domainIdentifier: SleepDetector' \
--header 'propIdentifier: HeartAbnormityMsgRemindPlan'
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
        "plan":[
            [
                {
                    "name":"undefined",
                    "repeatPeriod":[[1]],
                    "action":[
                        [
                            {
                                "actionType":"undefined",
                                "endValue":true,
                                "startValue":true
                            }
                        ]
                    ],
                    "startTime":"undefined",
                    "sustain":0,
                    "enabled":false
                }
            ]
        ],
        "enabled":true
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数，详细说明见下表 |
| data.plan | Array | 计划列表（范围：[0,8]） |
| data.enabled | Boolean | 定时计划总开关 |
| data.plan[].name | String | 计划名称（范围：[0,32]） |
| data.plan[].repeatPeriod | Array | 重复周期，为空，执行一次（范围：[1,16]） |
| data.plan[].action | Array | 计划操作内容（范围：[1,8]） |
| data.plan[].startTime | String | 触发时间（范围：[1,]） |
| data.plan[].sustain | Integer | 持续时间（范围：[0,1440]） |
| data.plan[].enabled | Boolean | 使能开关 |
| data.plan[].action[].actionType | String | 执行动作（范围：[1,2556]） |
| data.plan[].action[].endValue | Boolean | 执行动作的identifier的值(根据具体协议定制，类型) |
| data.plan[].action[].startValue | Boolean | 执行动作的identifier的值(根据具体协议定制，类型) |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |