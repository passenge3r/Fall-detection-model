# API-存储与媒体处理-云录制-视频采集与存储-查询加密录制项目列表

> 更新时间: 2026-06-24T15:52:25.000+08:00

> 文档ID: 2062 | 来源树: 云存储

---

## 查询加密录制项目列表

- 接口功能

   查询加密录制项目列表。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/space/listById`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | startTime | String | 查询开始时间，格式yyyyMMddHHmmss | Y |
| query | endTime | String | 查询结束时间，格式yyyyMMddHHmmss，开始结束时间需要同一天，startTime 和 endTime 查询的是 createTime 的时间 | Y |
| query | lastSpaceId | String | 上一页最后空间id，不传时默认为0 | N |
| query | pageSize | Int | 分页大小，默认10，范围1-50 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/space/listById?startTime=20231118000000&endTime=20231118235959&lastSpaceId=0&pageSize=10' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": ""
    },
    "data": {
        "spacesInfo": [
            {
                "spaceId": 11,
                "totalSize": 0,
                "totalTimePlan": 0,
                "totalEventPlan": 0,
                "spaceName": "t",
                "storageType": 1,
                "expireDays": 1,
                "primarySpace": false,
                "createTime": "2023-11-18 08:27:04",
                "updateTime": "2023-11-18 08:27:04"
            }
        ],
        "lastSpaceId": 11,
        "pageSize": 2,
        "hasNext": false
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回体 |
| meta.code | Int | 返回码 |
| meta.message | String | 返回信息 |
| meta.moreInfo | String | 更多信息 |
| data | Object | 数据 |
| data.spacesInfo | Array<Object> | 空间列表 |
| data.spacesInfo.spaceId | Int | 空间id |
| data.spacesInfo.totalSize | Int | 总大小 |
| data.spacesInfo.totalTimePlan | Int | 总时间计划数量 |
| data.spacesInfo.totalEventPlan | Int | 事件计划数量 |
| data.spacesInfo.spaceName | String | 空间名称 |
| data.spacesInfo.storageType | Int | 存储类型 |
| data.spacesInfo.expireDays | Int | 过期时间 |
| data.spacesInfo.primarySpace | Boolean | 是否为主空间 |
| data.spacesInfo.createTime | String | 创建时间 |
| data.spacesInfo.updateTime | String | 更新时间 |
| data.lastSpaceId | Int | 上一次空间id，下一次查询时使用 |
| data.pageSize | Int | 分页大小 |
| data.hasNext | Boolean | 有没有下一页 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码 200 |
| 400 | 参数错误 | HTTP状态码 400 |
| 406 | 平台不支持的操作 | HTTP状态码 406 |
| 412 | 前置条件不满足 | HTTP状态码 412 |
| 500 | 服务器异常 | HTTP状态码 500 |