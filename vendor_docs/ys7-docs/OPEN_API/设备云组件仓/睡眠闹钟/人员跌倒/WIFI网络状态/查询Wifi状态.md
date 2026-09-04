# 查询Wifi状态

> 更新时间: 2026-06-23T16:42:59.000+08:00

> 文档ID: 3977 | 来源树: OPEN_API

---

## 查询Wifi状态

### 接口功能

- 查询设备Wifi网络状态

### 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/["0"]/WifiStatus/NetStatus`

### 请求方式

`GET`

### 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 萤石开放API访问令牌 | Y |
| Header | Content-Type | String | application/json | Y |
| Path | deviceSerial | String | 设备序列号 | Y |

### 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/["0"]/WifiStatus/NetStatus' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
```

### 返回数据

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
    "connectStatus": "",
    "type": "",
    "signal": "",
    "ssid": "",
    "gateway": "",
    "mac": "",
    "mask": ""
  }
}
```

### 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数 |
| data.address | String | ip地址 |
| data.connectStatus | String | wifi连接状态，connected-已连接，disconnected-未连接，connecting-连接中 |
| data.type | String | 网络类型 |
| data.signal | String | 信号大小，db值例如 -71 |
| data.ssid | String | wifi ssid |
| data.gateway | String | 网关地址 |
| data.mac | String | mac地址 |
| data.mask | String | 子网掩码 |

### 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 操作成功 |