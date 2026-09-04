# 录像计划下的任务列表查询（GET）

>  

> 更新时间: 2026-06-11T14:50:15.000+08:00

> 文档ID: 4860 | 来源树: 云存储

---

## 录像计划下的任务列表查询

- 接口功能

   录像计划下的任务列表查询

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/task/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | pageStart | Int | 页码，默认0 | N |
| query | pageSize | Int | 分页大小，默认10，pageSize为1~50 | N |
| query | planId | Long | 一次性录制计划id | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/task/list?pageStart=0&pageSize=10&planId=1128140' \
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
    "data": {
        "result": [
            {
                "id": 1501958,
                "planId": 1119110,
                "planType": 1,
                "startTime": "2025-07-30 12:29:34",
                "endTime": "2025-07-30 12:35:10",
                "taskType": 1,
                "taskDetail": "{\"streamType\":1,\"recordList\":[{\"beginTime\":1753849773796,\"endTime\":1753850110000,\"errorCode\":\"6519\",\"cloudTaskId\":5525260621}]}",
                "spaceId": 44028,
                "deviceSerial": "BA5551167",
                "localIndex": "1",
                "cloudTaskId": 5525260621,
                "taskStatus": 4,
                "errorCode": "6519",
                "errorMsg": "设备取流异常",
                "totalSize": 2519980,
                "totalDuration": 186,
                "haveVideos": true,
                "createTime": "2025-07-30 12:29:34",
                "updateTime": "2025-07-30 12:33:04"
            }
        ],
        "pageStart": 0,
        "pageSize": 10,
        "total": 1
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta信息 |
| -code | Int | 状态码 |
| -message | String | 状态信息 |
| -moreInfo | Object | 更多信息 |
| data | Object | 返回数据 |
| -result | Array | 任务列表 |
| --id | Long | 任务主键id |
| --planId | Long | 一次性计划ID |
| --planType | Int | 计划类型，1. 一次性录像计划; 2.批量录像计划; 3.即时录像计划 |
| --startTime | String | 开始时间，yyyy-MM-DD HH:mm:ss |
| --endTime | String | 结束时间，yyyy-MM-DD HH:mm:ss |
| --taskType | Int | 任务类型，1. 预览; 2.回放 |
| --taskDetail | String | 任务详情 |
| --spaceId | Long | 云录制2.0空间id |
| --deviceSerial | String | 设备序列号 |
| --localIndex | String | 通道号 |
| --cloudTaskId | Long | 云录制拉流任务id |
| --taskStatus | Int | 任务状态，0-未开始;1-等待中;2-进行中;3-暂停中;4-异常结束;5-已完成;6-已取消 |
| --errorCode | String | 错误码，具体含义可查看[云录制2.0常见错误码](https://open.ys7.com/help/4488) |
| --errorMsg | String | 该错误信息为默认值，具体错误码对应的错误信息可查看[云录制2.0常见错误码](https://open.ys7.com/help/4488) |
| --totalSize | Long | 存储大小，单位B |
| --totalDuration | Long | 时长，单位秒 |
| --haveVideos | Boolean | 是否存在录像片段 |
| --createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| --updateTime | String | 修改时间，yyyy-MM-DD HH:mm:ss |
| -pageStart | Int | 当前页码 |
| -pageSize | Int | 每页数量 |
| -total | Int | 总数 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 500 | 服务器异常 | 服务器内部错误 |
| 400 | 参数错误 | 请求参数有误 |