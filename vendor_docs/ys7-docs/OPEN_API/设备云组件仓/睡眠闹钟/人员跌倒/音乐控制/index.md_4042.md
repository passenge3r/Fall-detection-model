# index.md

> 更新时间: 2026-06-17T18:04:28.000+08:00

> 文档ID: 4042 | 来源树: OPEN_API

---

## 设置简化音乐列表 （MusicListPure）

- 接口功能

   设置简化音乐列表 （MusicListPure）

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/MusicControl/MusicListPure`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| body | Content-Type | string |  | Y |
| header | accessToken | string | 用户访问令牌 | Y |
| body | data | string | MusicListPure, range:[1,] | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{{deviceSerial}}/global/["0"]/MusicControl/MusicListPure' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "Content-Type": "value",
    "data": "value"
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
  }
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

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 20007 | 设备不在线 |  |