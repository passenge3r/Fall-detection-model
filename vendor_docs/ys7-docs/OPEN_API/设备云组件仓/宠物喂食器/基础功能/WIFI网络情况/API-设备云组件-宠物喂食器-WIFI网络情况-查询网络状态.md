# API-设备云组件-宠物喂食器-WIFI网络情况-查询网络状态

>  

> 更新时间: 2026-06-30T11:48:58.000+08:00

> 文档ID: 1561 | 来源树: OPEN_API

---

## 查询网络状态

- 接口功能

   属于WIFI网络配置(WifiStatus)，查询设备网络状态

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/WifiStatus/NetStatus`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/WifiStatus/NetStatus' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "address": "192.168.43.46",
        "type": "wireless",
        "signal": "-54",
        "ssid": "abcd",
        "gateway": "192.168.43.1",
        "mask": "255.255.255.0"
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
| data.address | String | ip地址，长度范围[0,64] |
| data.type | String | 网络类型，长度范围[0,64] |
| data.signal | String | 信号大小，长度范围[0,64] |
| data.ssid | String | wifi ssid，长度范围[0,64] |
| data.gateway | String | 网关地址，长度范围[0,64] |
| data.mask | String | 子网掩码，长度范围[0,64] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |