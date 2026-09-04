# API-设备云组件仓-调节控制器-基础功能-空调控制-查询外机工作模式

> 更新时间: 2026-07-06T13:51:23.000+08:00

> 文档ID: 1236 | 来源树: OPEN_API

---

## 查询外机工作模式

- 接口功能

   该接口用于查询空调外机工作模式。本文档仅适用于设备型号 CS-HAE-V2W，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/AirCondition/ /AirConditionCtrl/OutsideMachineWorkMode`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/AirCondition/ /AirConditionCtrl/OutsideMachineWorkMode' \
--header 'Content-Type: application/json' \
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
    "data": "auto"
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
| data | String | 工作模式，取值范围[heat,cool,auto,dry,fan,smart,powerSaving,strong,exhaust,breathe,none]：heat-制热，cool-制冷，auto-自动，dry-除湿，fan-送风，smart-智能，powerSaving-省电，strong-强劲，exhaust-排风，breathe-换气，none-关机 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |