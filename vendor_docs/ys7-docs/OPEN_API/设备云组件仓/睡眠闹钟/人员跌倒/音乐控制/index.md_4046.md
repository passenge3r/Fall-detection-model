# index.md

> 更新时间: 2026-06-17T18:04:33.000+08:00

> 文档ID: 4046 | 来源树: OPEN_API

---

## 蓝牙开启 （Bluetooth）

- 接口功能

   蓝牙开启 （Bluetooth）

- 请求地址

`https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/MusicControl/Bluetooth`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| body | Content-Type | string |  | Y |
| header | accessToken | string | 用户访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| body | data | integer | 开启蓝牙, range:[1]. 1-开启蓝牙 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/action/{{deviceSerial}}/global/["0"]/MusicControl/Bluetooth' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Content-Type": "value",
    "data": 0
}'
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
  "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| meta | object | 服务响应信息 |
| meta.code | integer | 服务响应状态码。参见响应码解释。 |
| meta.message | string | 服务响应状态描述 |
| meta.moreInfo | object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | string | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | string | 设备响应状态描述 |
| data | -- | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 20007 | 设备不在线 |  |