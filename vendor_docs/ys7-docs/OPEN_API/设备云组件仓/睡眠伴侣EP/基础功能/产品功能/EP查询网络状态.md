# EP查询网络状态

> 更新时间: 2026-06-25T14:31:20.000+08:00

> 文档ID: 2053 | 来源树: OPEN_API

---

## 查询网络状态

- 接口功能

   查询网络状态（NetStatus）。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| query | deviceSerial | String | 设备序列号 | Y |
| query | localIndex | String | 资源描述，描述资源类型下的序号，示例值：0 | Y |
| query | resourceCategory | String | 资源种类，描述资源的类型，示例值：global | Y |
| query | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，示例值：WifiStatus | Y |
| query | propIdentifier | String | 功能点标识，填写报备时的属性标识符，示例值：NetStatus | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop?deviceSerial=xxxxxxxxx&localIndex=0&resourceCategory=global&domainIdentifier=WifiStatus&propIdentifier=NetStatus' \
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

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 业务参数，详细说明见下方 |
| data.address | String | ip地址，范围：[0,64] |
| data.connectStatus | String | 连接状态，范围：[connected,disconnected,connecting]；connected-已连接；disconnected-未连接；connecting-连接中 |
| data.type | String | 网络类型，范围：[0,64] |
| data.signal | String | 信号大小，范围：[0,64] |
| data.ssid | String | wifissid，范围：[0,64] |
| data.gateway | String | 网关地址，范围：[0,64] |
| data.mac | String | mac地址，范围：[0,64] |
| data.mask | String | 子网掩码，范围：[0,64] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |