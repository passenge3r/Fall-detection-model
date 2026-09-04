# API-设备云组件-CS-T33-AW红外遥控器-基础功能-红外电器控制-查询电器类型

> 更新时间: 2026-06-30T11:55:40.000+08:00

> 文档ID: 1635 | 来源树: OPEN_API

---

## 查询电器类型

- 接口功能

   查询电器类型

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/ApplianceType`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | Content-Type | String | 固定值：application/json | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/IrRemote/1/IrDeviceCtrl/ApplianceType' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json'
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
        "type": 5
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
| data.type | Int | 类型，取值范围[1,13]：1-机顶盒，2-电视，3-盒子，4-DVD，5-空调，6-投影仪，7-功放，8-风扇，9-单反，10-灯泡，11-空气净化器，12-热水器，13-自定义 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |