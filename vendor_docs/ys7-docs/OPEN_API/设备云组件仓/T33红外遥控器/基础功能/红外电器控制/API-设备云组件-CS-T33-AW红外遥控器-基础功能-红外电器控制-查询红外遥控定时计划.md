# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外电器控制-查询红外遥控定时计划

> 更新时间: 2026-06-30T11:55:49.000+08:00

> 文档ID: 1641 | 来源树: OPEN_API

---

## 查询红外遥控定时计划

- 接口功能

   查询红外遥控定时计划

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/IrRemoteTimePlan`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/IrRemoteTimePlan' \
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
                    "name": "",
                    "repeatPeriod": [
                        [
                            1
                        ]
                    ],
                    "action": [
                        [
                            {
                                "actionType": "",
                                "endValue": "",
                                "startValue": ""
                            }
                        ]
                    ],
                    "startTime": "",
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
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数 |
| data.plan | Array | 计划列表，范围[0,8] |
| data.plan[].name | String | 计划名称，长度范围[0,32] |
| data.plan[].repeatPeriod | Array | 重复周期，为空执行一次，范围[0,16] |
| data.plan[].action | Array | 计划操作内容，范围[1,8] |
| data.plan[].action[].actionType | String | 执行动作URI，长度范围[1,2556] |
| data.plan[].action[].endValue | String | 结束值，长度范围[0,255] |
| data.plan[].action[].startValue | String | 开始值，长度范围[0,255] |
| data.plan[].startTime | String | 触发时间，长度范围[1,32] |
| data.plan[].sustain | Int | 持续时间，取值范围[0,1440] |
| data.plan[].enabled | Boolean | 使能开关 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |