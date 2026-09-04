# 睡眠半路EP-获取设备在离床消息

> 更新时间: 2026-06-24T15:59:02.000+08:00

> 文档ID: 2098 | 来源树: OPEN_API

---

## 睡眠半路EP-获取设备在离床消息

- 接口功能

   获取设备在离床消息。

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/whst/statistics/data/bodyDetect`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | deviceSerial | String | 设备序列号 | Y |
| query | offset | Int | 偏移量 | Y |
| query | limit | Int | 限制条数 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/whst/statistics/data/bodyDetect?deviceSerial=BG9859941&offset=0&limit=10' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "page": {
        "offset": 0,
        "limit": 10,
        "totalResults": 348,
        "hasNext": true
    },
    "data": [
        {
            "messageTime": "2023-12-02 15:59:28",
            "messageType": 1
        },
        {
            "messageTime": "2023-12-02 15:58:44",
            "messageType": 2
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| page | Object | 分页数据 |
| -offset | Int | 偏移量 |
| -limit | Int | 限制条数 |
| -totalResults | Int | 总条数 |
| -hasNext | Boolean | 是否有下一页 |
| data | Array<Object> | 具体数据 |
| -messageTime | String | 消息时间 |
| -messageType | Int | 1=在床消息；2=离床消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码:200 |
| 500 | 服务器异常 | HTTP状态码:500 |
| 400 | 参数错误 | HTTP状态码:400 |