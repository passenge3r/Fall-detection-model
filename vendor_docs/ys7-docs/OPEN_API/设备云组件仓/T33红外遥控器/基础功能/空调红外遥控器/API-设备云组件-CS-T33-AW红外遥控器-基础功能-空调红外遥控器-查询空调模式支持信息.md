# API-设备云组件-CS-T33-AW红外遥控器-基础功能-空调红外遥控器-查询空调模式支持信息

> 更新时间: 2026-06-30T12:00:11.000+08:00

> 文档ID: 1645 | 来源树: OPEN_API

---

## 查询空调模式支持信息

- 接口功能

   查询空调模式支持信息

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/ACIrRemote/Mode`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/ACIrRemote/Mode' \
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
        "keys": [
            [
                {
                    "custom": 0,
                    "name": "",
                    "id": 1,
                    "support": 1
                }
            ]
        ],
        "function": {
            "powerOn": "power_on",
            "functions": [
                [
                    {
                        "temp": {
                            "support": true,
                            "temps": [
                                [
                                    26
                                ]
                            ]
                        },
                        "id": 1,
                        "support": true,
                        "speed": {
                            "speeds": [
                                [
                                    1
                                ]
                            ],
                            "support": true
                        }
                    }
                ]
            ],
            "powerOff": "power_off"
        }
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
| data.keys | Array | 独立按键模式支持的按键，范围[0,] |
| data.keys[].custom | Int | 0-不是自定义按键，1-是自定义按键 |
| data.keys[].name | String | 按键名称，长度范围[1,] |
| data.keys[].id | Int | 按键id |
| data.keys[].support | Int | 是否支持此按键 |
| data.function | Object | 组合按键模式 |
| data.function.powerOn | String | 开机键的key，默认：power\_on，长度范围[1,] |
| data.function.powerOff | String | 关机键的key，默认：power\_off，长度范围[1,] |
| data.function.functions | Array | 组合按键模式支持的按键，范围[0,] |
| data.function.functions[].id | Int | 模式id |
| data.function.functions[].support | Boolean | 是否支持 |
| data.function.functions[].temp.support | Boolean | 是否支持 |
| data.function.functions[].temp.temps | Array | 支持的温度数值，范围[0,] |
| data.function.functions[].speed.support | Boolean | 是否支持 |
| data.function.functions[].speed.speeds | Array | 支持的风速档位，范围[0,] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |