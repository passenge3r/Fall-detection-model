# 查询是否支持将音频格式转码为AAC

> 更新时间: 2026-06-23T10:18:36.000+08:00

> 文档ID: 3736 | 来源树: OPEN_API

---

## 查询是否支持将音频格式转码为AAC

- 接口功能

   查询是否支持将音频格式转码为AAC

- 请求地址

`https://open.ys7.com/api/service/media/aac/transfer`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 授权过程获取的access\_token，支持at token，da du token，ra ar token，localIndex不填或者为0，则是设备级CONFIG权限，否则为通道级别CONFIG权限 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | Int | 通道号，不填或者为0表示为设备级别的配置 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/media/aac/transfer' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: L12345678' \
--header 'localIndex: 1'
```

- 返回数据

```
{
    "data": {
        "enable": true
    },
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 响应体 |
| data.enable | Boolean | true-支持将音频格式转码为AAC，false-不支持将音频格式转码为AAC |
| meta | Object | 响应元信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应信息 |
| meta.moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | deviceSerial不能为空 |  |
| 10001 | localIndex错误 |  |
| 10002 | accessToken过期或异常 |  |
| 10031 | 账号无权限访问此设备 |  |
| 20002 | 设备不存在 |  |
| 20001 | 通道不存在 |  |
| 50000 | 系统异常 |  |