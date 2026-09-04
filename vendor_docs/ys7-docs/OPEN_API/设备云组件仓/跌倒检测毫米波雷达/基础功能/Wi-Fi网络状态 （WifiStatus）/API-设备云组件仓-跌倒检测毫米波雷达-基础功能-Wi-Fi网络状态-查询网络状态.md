# API-设备云组件仓-跌倒检测毫米波雷达-基础功能-Wi-Fi网络状态-查询网络状态

> 更新时间: 2026-07-01T18:27:39.000+08:00

> 文档ID: 1287 | 来源树: OPEN_API

---

## 查询网络状态

- 接口功能

   该接口用于查询设备Wi-Fi网络状态。本文档仅适用于设备型号 CSEPMR511，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/WifiStatus/NetStatus`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/WifiStatus/NetStatus' \
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
    "data": {
        "address": "",
        "type": "",
        "signal": "",
        "ssid": "",
        "gateway": "",
        "mask": ""
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
| data.address | String | ip地址，范围[0,64] |
| data.type | String | 网络类型，范围[0,64] |
| data.signal | String | 信号大小，范围[0,64] |
| data.ssid | String | wifissid，范围[0,64] |
| data.gateway | String | 网关地址，范围[0,64] |
| data.mask | String | 子网掩码，范围[0,64] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |