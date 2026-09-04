# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外电器控制-查询按键列表

> 更新时间: 2026-06-30T11:55:54.000+08:00

> 文档ID: 1639 | 来源树: OPEN_API

---

## 查询按键列表

- 接口功能

   查询按键列表

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/KeyList`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/KeyList' \
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
                    "keyTag": "",
                    "keyValue": "",
                    "displayName": "",
                    "custom": 0,
                    "name": "",
                    "icon": "",
                    "pulse": "",
                    "id": 0,
                    "position": "",
                    "support": false
                }
            ]
        ],
        "applianceType": "",
        "tag": 0,
        "type": 1,
        "value": 0,
        "frequency": 0
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
| data.keys | Array | 按键列表，范围[0,256] |
| data.keys[].keyTag | String | 按键参数tag，长度范围[0,255] |
| data.keys[].keyValue | String | 按键参数value，长度范围[0,65535] |
| data.keys[].displayName | String | 按键显示名称，长度范围[0,64] |
| data.keys[].custom | Int | 取值范围[0,1]：0-不是自定义按键，1-是自定义按键 |
| data.keys[].name | String | 按键名称，长度范围[0,128] |
| data.keys[].icon | String | 按键图标，长度范围[0,64] |
| data.keys[].pulse | String | 红码的波形，长度范围[0,65535] |
| data.keys[].id | Int | 按键id，取值范围[0,65535] |
| data.keys[].position | String | 位置，长度范围[0,255] |
| data.keys[].support | Boolean | 是否支持此按键 |
| data.applianceType | String | 电器类型，取值范围[AC,TV]：AC-空调，TV-电视 |
| data.tag | Int | 遥控器参数tag，取值范围[0,255] |
| data.type | Int | 取值范围[1,2]：1-无状态红外码可直接发送，2-有状态要SDK解码 |
| data.value | Int | 遥控器参数value，取值范围[0,65535] |
| data.frequency | Int | 频率，每套码都有自己的频率，取值范围[1,65535] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |