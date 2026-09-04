# API-存储与媒体处理-删除关键词.md

> 开放存储AI语音云存相关

> 更新时间: 2026-06-16T17:21:02.000+08:00

> 文档ID: 5196 | 来源树: 云存储

---

## 删除关键词

- 接口功能

   删除语音质检的关键词

- 请求地址

`https://open.ys7.com/api/service/cloud/storage/service/aivoice/keyword/delete`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | id | Long | 关键词ID | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloud/storage/service/aivoice/keyword/delete?id=55' \
--header 'Content-Type: application/x-www-form-urlencoded' \
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
  "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta信息 |
| meta.code | Int | 状态码 |
| meta.message | String | 状态信息 |
| meta.moreInfo | String | 更多信息 |
| data | Object | 返回数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 50000 | 服务异常 | 服务异常 |
| 10001 | 请求参数错误 | 请求参数错误 |