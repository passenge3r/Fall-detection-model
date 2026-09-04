# API-存储与媒体处理-查询已命中关键词的录像.md

> 开放存储AI语音云存相关

> 更新时间: 2026-06-16T17:21:08.000+08:00

> 文档ID: 5199 | 来源树: 云存储

---

## 查询命中关键词的录像列表

- 接口功能

   查询命中关键词的录像列表

- 请求地址

`https://open.ys7.com/api/service/cloud/storage/service/aivoice/record/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | Int | 设备通道号，默认1 | N |
| body | startTime | String | 查询开始时间，格式：YYYY-MM-dd HH:mm:ss | Y |
| body | stopTime | String | 查询结束时间，格式：YYYY-MM-dd HH:mm:ss | Y |
| body | withText | Boolean | 是否返回语音转文字内容，默认false | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloud/storage/service/aivoice/record/list' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: E71992159' \
--header 'localIndex: 1' \
--data-raw '{
    "startTime": "2026-04-22 13:00:00",
    "stopTime": "2026-04-22 23:00:00",
    "withText": true
}'
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
    "deviceSerial": "D12345678",
    "localIndex": 1,
    "videos": [
      {
        "segId": "seg_001",
        "startTime": "2026-04-10 08:30:00",
        "stopTime": "2026-04-10 08:35:00",
        "storageVersion": 2,
        "totalDay": 30,
        "expireTime": "2026-05-10 08:30:00",
        "audioText": "检测到异常声音报警"
      }
    ]
  }
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
| data.deviceSerial | String | 设备序列号 |
| data.localIndex | Int | 设备通道号 |
| data.videos | Array | 录像列表 |
| data.videos[].segId | String | 片段ID |
| data.videos[].startTime | String | 开始时间 |
| data.videos[].stopTime | String | 结束时间 |
| data.videos[].storageVersion | Int | 存储版本 |
| data.videos[].totalDay | Int | 总天数 |
| data.videos[].expireTime | String | 过期时间 |
| data.videos[].audioText | String | 语音转文字内容 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 50000 | 服务异常 | 服务异常 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 10001 | 请求参数错误 | 请求参数错误 |