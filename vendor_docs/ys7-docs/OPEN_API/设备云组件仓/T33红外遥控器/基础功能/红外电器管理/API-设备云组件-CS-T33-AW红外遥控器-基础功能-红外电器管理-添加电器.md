# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外电器管理-添加电器

> 更新时间: 2026-06-30T12:01:00.000+08:00

> 文档ID: 1650 | 来源树: OPEN_API

---

## 添加电器

- 接口功能

   添加电器

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/IrDeviceManage/AddDevice`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | total | Int | 总包数，取值范围[1,100] | Y |
| body | current | Int | 当前包编号，取值范围[1,100] | N |
| body | subType | Int | 子类型，取值范围[0,65535] | N |
| body | type | Int | 电器类型，取值范围[1,13]：1-机顶盒，2-电视机，3-盒子，4-DVD，5-空调，6-投影仪，7-功放，8-风扇，9-单反，10-空气净化器，11-空气净化器，12-热水器，13-自定义 | Y |
| body | UUID | String | 业务包标识，长度范围[12,64] | Y |
| body | brand | String | 电器品牌，长度范围[0,1000] | N |
| body | irInfo.id | String | 红码id，可以唯一标识红码，长度范围[0,256] | N |
| body | irInfo.tag | String | 参数tag，长度范围[0,255] | N |
| body | irInfo.type | Int | 类型，取值范围[0,65535] | N |
| body | irInfo.value | String | 参数tagValue，长度范围[0,65535] | N |
| body | irInfo.frequency | Int | 频率，取值范围[0,255555] | N |
| body | irInfo.functions[].mode | Int | 支持的功能（空调）模式，取值范围[0,10]：0-制冷，1-制热，2-自动，3-送风，4-除湿 | N |
| body | irInfo.functions[].temperature | String | 支持的温度值，逗号分隔，长度范围[0,65535] | N |
| body | irInfo.functions[].speed | String | 支持的速度，逗号分隔，风量：0-自动，1-低，2-中，3-高，长度范围[0,65535] | N |
| body | irInfo.keys[].keyTag | String | 按键参数tag，长度范围[0,255] | N |
| body | irInfo.keys[].keyValue | String | 按键参数value，长度范围[0,65535] | N |
| body | irInfo.keys[].name | String | 按键名称，长度范围[0,255] | N |
| body | irInfo.keys[].pulse | String | 按键波形，长度范围[0,255] | N |
| body | irInfo.keys[].id | String | 按键id，长度范围[0,256] | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{deviceSerial}/global/0/IrDeviceManage/AddDevice' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "irInfo": {
        "functions": [
            [
                {
                    "mode": 0,
                    "temperature": "",
                    "speed": ""
                }
            ]
        ],
        "keys": [
            [
                {
                    "keyTag": "",
                    "keyValue": "",
                    "name": "",
                    "pulse": "",
                    "id": ""
                }
            ]
        ],
        "id": "",
        "tag": "",
        "type": 0,
        "value": "",
        "frequency": 0
    },
    "total": 1,
    "current": 1,
    "subType": 0,
    "type": 1,
    "UUID": "",
    "brand": ""
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
    },
    "data": null
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
| data | Object | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |