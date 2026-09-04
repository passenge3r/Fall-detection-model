# API-设备云组件-CS-T33-AW红外遥控器-基础功能-空调红外遥控器-查询最后设置状态

> 更新时间: 2026-06-30T12:00:13.000+08:00

> 文档ID: 1646 | 来源树: OPEN_API

---

## 查询最后设置状态

- 接口功能

   查询最后设置状态

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/ACIrRemote/LastStatus`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/ACIrRemote/LastStatus' \
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
        "mode": 1,
        "temp": 5,
        "speed": 2,
        "switch": false
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
| data.mode | Int | 模式，取值范围[0,1,2,3,4]：0-制冷，1-制热，2-自动，3-送风，4-除湿 |
| data.temp | Int | 温度，取值范围[0,32] |
| data.speed | Int | 风速，取值范围[0,1,2,3]：0-自动，1-低速，2-中速，3-高速 |
| data.switch | Boolean | 开关 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |