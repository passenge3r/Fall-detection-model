# API-设备云组件仓-智能锁-基础功能-徘徊侦测-设置徘徊侦测规则参数

> 更新时间: 2026-07-09T13:45:44.000+08:00

> 文档ID: 791 | 来源树: OPEN_API

---

## 设置徘徊侦测规则参数

- 接口功能

   该接口用于设置徘徊侦测规则参数。本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁，其余型号不保证可用。如下接口调用需要联系萤石配置白名单，否则接口可能调用报错。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/Loitering/LoiteringRuleParams`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | targetFilter.filterSize.minTargetSize | Array | 最小目标尺寸，取值范围[4,4] | N |
| Body | targetFilter.filterSize.minTargetSize[].positionY | Number | 点的纵坐标，取值范围[0.0,1.0] | N |
| Body | targetFilter.filterSize.minTargetSize[].positionX | Number | 点的横坐标，取值范围[0.0,1.0] | N |
| Body | targetFilter.filterSize.maxTargetSize | Array | 最大目标尺寸，取值范围[0,16] | N |
| Body | targetFilter.filterSize.maxTargetSize[].positionY | Number | 点的纵坐标，取值范围[0.0,1.0] | N |
| Body | targetFilter.filterSize.maxTargetSize[].positionX | Number | 点的横坐标，取值范围[0.0,1.0] | N |
| Body | targetFilter.enable | Boolean | 尺寸过滤使能 | Y |
| Body | targetFilter.targetFilterMode | String | 目标过滤模式，取值范围[pixels,actualSize]：pixels-目标像素过滤，actualSize-实际坐标尺寸过滤（坐标归一化至1.000） | N |
| Body | ruleInfo | Array | 规则信息列表，取值范围[1,16] | Y |
| Body | ruleInfo[].timeThreshold | Integer | 触发时间阈值，取值范围[1,120] | Y |
| Body | ruleInfo[].ruleName | String | 规则名称，取值范围[0,32] | N |
| Body | ruleInfo[].sensitivityLevel | Integer | 灵敏度，取值范围[0,100] | Y |
| Body | ruleInfo[].ruleID | Integer | 规则序号，取值范围[1,16] | Y |
| Body | ruleInfo[].region | Array | 区域坐标列表，取值范围[0,16] | N |
| Body | ruleInfo[].region[].positionY | Number | 坐标Y，取值范围[0.0,1.0] | Y |
| Body | ruleInfo[].region[].positionX | Number | 坐标X，取值范围[0.0,1.0] | Y |
| Body | ruleInfo[].enabled | Boolean | 使能 | Y |
| Body | sceneID | Integer | 场景id，取值范围[1,16] | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/Loitering/LoiteringRuleParams' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "targetFilter": {
        "filterSize": {
            "minTargetSize": [
                [
                    {
                        "positionY": 0.5,
                        "positionX": 0.5
                    }
                ]
            ],
            "maxTargetSize": [
                [
                    {
                        "positionY": 0.5,
                        "positionX": 0.5
                    }
                ]
            ]
        },
        "enable": true,
        "targetFilterMode": "pixels"
    },
    "ruleInfo": [
        [
            {
                "timeThreshold": 100,
                "ruleName": "undefined",
                "sensitivityLevel": 0,
                "ruleID": 1,
                "region": [
                    [
                        {
                            "positionY": 1.0,
                            "positionX": 0.001
                        }
                    ]
                ],
                "enabled": true
            }
        ]
    ],
    "sceneID": 1
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