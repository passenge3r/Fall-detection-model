# API-存储与媒体处理-查询关键词列表.md

> 开放存储AI语音云存相关

> 更新时间: 2026-06-16T17:21:04.000+08:00

> 文档ID: 5197 | 来源树: 云存储

---

## 查询关键词列表

- 接口功能

   查询已设置的语音质检关键词信息

- 请求地址

`https://open.ys7.com/api/service/cloud/storage/service/aivoice/keyword/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloud/storage/service/aivoice/keyword/list' \
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
  "data": [
    {
      "id": 123,
      "userId": "user001",
      "keywords": ["报警", "异常声音"],
      "matchDimension": 1,
      "matchType": 1,
      "keywordsStatus": 1,
      "createTime": "2026-04-10 10:00:00",
      "updateTime": "2026-04-15 14:30:00"
    }
  ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta信息 |
| meta.code | Int | 状态码 |
| meta.message | String | 状态信息 |
| meta.moreInfo | String | 更多信息 |
| data | Array | 关键词列表 |
| data[].id | Int | 关键词ID |
| data[].userId | String | 用户ID |
| data[].keywords | Array | 关键词集合 |
| data[].matchDimension | Int | 匹配维度 |
| data[].matchType | Int | 匹配类型 |
| data[].keywordsStatus | Int | 关键词状态 |
| data[].createTime | String | 创建时间 |
| data[].updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 50000 | 服务异常 | 服务异常 |
| 10001 | 请求参数错误 | 请求参数错误 |