# API-设备云组件仓-T8C天然气传感器-基础功能-电源管理-设置剩余电量

> 更新时间: 2026-07-06T13:43:42.000+08:00

> 文档ID: 997 | 来源树: OPEN_API

---

## 设置剩余电量

- 接口功能

   该接口用于设置剩余电量。本文档仅适用于设备型号 CS-T8C-DG，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/GasSensor/0/PowerMgr/SurplusPower`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |
| Body | data | Integer | 剩余电量，取值范围[0,100] | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/GasSensor/0/PowerMgr/SurplusPower' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '4'
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