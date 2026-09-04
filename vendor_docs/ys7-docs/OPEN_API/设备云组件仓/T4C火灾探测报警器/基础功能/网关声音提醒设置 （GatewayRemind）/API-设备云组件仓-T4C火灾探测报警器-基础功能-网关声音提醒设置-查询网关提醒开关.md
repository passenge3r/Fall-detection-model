# API-设备云组件仓-T4C火灾探测报警器-基础功能-网关声音提醒设置-查询网关提醒开关

>  

> 更新时间: 2026-06-30T17:55:36.000+08:00

> 文档ID: 1450 | 来源树: OPEN_API

---

## 查询网关提醒开关

- 接口功能

   查询网关提醒开关。本文档仅适用于设备型号 CS-T4C-BG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/GatewayRemind/GateWayRemindSwitch`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| header | Content-Type | String | application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/SmokeSensor/0/GatewayRemind/GateWayRemindSwitch' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--header 'deviceSerial: xxxxxxxxx'
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
    "data": true
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Boolean | 网关提醒开关 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 |  |