# MT2查询窗帘开合定时任务

> 更新时间: 2026-06-24T15:58:18.000+08:00

> 文档ID: 2809 | 来源树: OPEN_API

---

## MT2查询窗帘开合定时任务

- 接口功能

查询窗帘开合定时任务。权限说明：支持托管及子账号，设备级，校验权限为Get。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 用户访问令牌，accessToken获取方法见 https://open.ys7.com/help/81 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 资源描述，描述资源类型下的序号，示例值：0 | Y |
| header | resourceCategory | String | 资源种类，描述资源的类型，示例值：Curtain | Y |
| header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，示例值：CurtainCtrl | Y |
| header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，示例值：OpeningClosingTimePlan | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'localIndex: 0' \
--header 'resourceCategory: Curtain' \
--header 'domainIdentifier: CurtainCtrl' \
--header 'propIdentifier: OpeningClosingTimePlan' \
--header 'Content-Type: application/json'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "plan": [
            {
                "name": "testPlan",
                "repeatPeriod": [1, 5],
                "action": [
                    {
                        "actionType": "model/attribute/set/CurtainCtrl/OpeningClosingPercentage",
                        "startValue": 45
                    }
                ],
                "startTime": "11:00:00",
                "sustain": 0,
                "enabled": true
            }
        ],
        "enabled": false
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
| data | Object | 业务参数，详细说明见下表 |
| data.plan | Array | 计划列表，最大支持创建8个计划 |
| data.enabled | Boolean | 计划使能总开关，计划执行的开关，若关闭，所有计划不会生效执行。取值：true |
| data.plan[].name | String | 计划名称，长度最大限制32 |
| data.plan[].repeatPeriod | Array | 重复周期，为空则执行一次；1,2,3,4,5,6,7 分别表示周一、周二、周三、周四、周五、周六、周日。 |
| data.plan[].action | Array | 计划操作内容，包含actionType、startValue信息 |
| data.plan[].startTime | String | 触发时间，长度限制最小1，最大32，格式HH:mm:ss，如11:00:00 |
| data.plan[].sustain | Int | 持续时间，单位分钟，最小值0，最大值1440 |
| data.plan[].enabled | Boolean | 使能开关，计划执行的开关，若关闭，计划不会生效执行。取值：true |
| data.plan[].action[].actionType | String | 执行动作URI，固定传值：model/attribute/set/CurtainCtrl/OpeningClosingPercentage，表示设置窗帘开合百分比 |
| data.plan[].action[].startValue | Int | 0表示关闭，大于0表示窗帘开合的百分比 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码：200 |
| 10001 | 参数错误 | HTTP状态码：200 |
| 10002 | token过期或异常 | HTTP状态码：200 |
| 10031 | 子账户或萤石用户没有权限 | HTTP状态码：200 |
| 20018 | 该用户不拥有该设备 | HTTP状态码：200 |
| 70018 | 资源不存在 | HTTP状态码：200 |
| 50000 | 服务异常 | HTTP状态码：200 |