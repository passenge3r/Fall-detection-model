# MC4设置定时计划

> 更新时间: 2026-06-25T14:28:56.000+08:00

> 文档ID: 2032 | 来源树: OPEN_API

---

## MC4设置定时计划

- 接口功能

   设置MC4设备定时计划，通过otap透传通道下发计划列表。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 用户访问令牌，参考 accessToken获取方法 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 资源描述，描述资源类型下的序号，示例：0 | Y |
| header | resourceCategory | String | 资源种类，描述资源的类型，示例：Curtain | Y |
| header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，示例：CustomPassThrogh | Y |
| header | propIdentifier | String | 功能点标识，填写报备时的属性标识符，示例：TimePlan | Y |
| body | plan | Array | 计划列表，名称：计划列表，范围：[0,8] | Y |
| body | -name | String | 计划名称，范围：[0,32] | N |
| body | -repeatPeriod | Array | 重复周期，为空，执行一次，范围：[0,16] | Y |
| body | -action | Array | 计划操作内容，范围：[1,8] | Y |
| body | --actionType | String | 执行动作URI，名称：执行动作URI，范围：[1,2556] | Y |
| body | -startTime | String | 触发时间，范围：[1,32] | Y |
| body | -sustain | Integer | 持续时间，范围：[0,1440] | Y |
| body | -enabled | Boolean | 使能开关 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/prop' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G00000001' \
--header 'localIndex: 0' \
--header 'resourceCategory: Curtain' \
--header 'domainIdentifier: CustomPassThrogh' \
--header 'propIdentifier: TimePlan' \
--data-raw '{
    "plan":[
        [
            {
                "name":"undefined",
                "repeatPeriod":[
                    [1]
                ],
                "action":[
                    [
                        {
                            "actionType":"undefined",
                            "endValue":{},
                            "startValue":{}
                        }
                    ]
                ],
                "startTime":"undefined",
                "sustain":0,
                "enabled":false
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
| meta.code | Integer | 服务响应状态码。参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |