# 根据设备序列号和通道号查询计执行中的任务列表（GET）

>  

> 更新时间: 2026-06-11T14:50:12.000+08:00

> 文档ID: 4861 | 来源树: 云存储

---

## 根据设备序列号和通道号查询该执行中的任务列表

- 接口功能

   根据设备序列号和通道号查询该执行中的任务列表

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/task/listRunningByDevId`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | deviceSerial | String | 设备序列号，字符长度100以内 | Y |
| query | localIndex | String | 设备通道号，4位，默认1 | N |
| query | startTime | String | 查询开始时间，格式yyyyMMddHHmmss | Y |
| query | endTime | String | 查询结束时间，格式yyyyMMddHHmmss，开始结束时间不能超过30天 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/task/listRunningByDevId?startTime=20250801000200&endTime=20250830000200&localIndex=1&deviceSerial=833055114' \
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
            "id": 1689,
            "planId": 1805,
            "planType": 1,
            "startTime": "2025-08-07 19:48:47",
            "endTime": "2025-08-07 19:52:15",
            "taskType": 1,
            "taskDetail": "{\"streamType\":1,\"recordList\":[{\"beginTime\":1754567327169,\"endTime\":1754567535000,\"errorCode\":null,\"cloudTaskId\":3291131}]}",
            "spaceId": 773,
            "deviceSerial": "889296437",
            "localIndex": "8",
            "cloudTaskId": 3291131,
            "taskStatus": 2,
            "errorCode": "",
            "errorMsg": "",
            "totalSize": 0,
            "totalDuration": 0,
            "createTime": "2025-08-07 19:48:47",
            "updateTime": "2025-08-07 19:48:47"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta信息 |
| -code | Int | 状态码 |
| -message | String | 状态信息 |
| -moreInfo | Object | 更多信息 |
| data | Array | 任务列表 |
| -id | Long | 任务主键id |
| -planId | Long | 一次性计划ID |
| -planType | Int | 计划类型，1. 一次性录像计划; 2.批量录像计划; 3.即时录像计划 |
| -startTime | String | 开始时间，yyyy-MM-DD HH:mm:ss |
| -endTime | String | 结束时间，yyyy-MM-DD HH:mm:ss |
| -taskType | Int | 任务类型，1. 预览; 2.回放 |
| -taskDetail | String | 任务详情 |
| -spaceId | Long | 云录制2.0空间id |
| -deviceSerial | String | 设备序列号 |
| -localIndex | String | 通道号 |
| -cloudTaskId | Long | 云录制拉流任务id |
| -taskStatus | Int | 任务状态，0-未开始;1-等待中;2-进行中;3-暂停中;4-异常结束;5-已完成;6-已取消 |
| -errorCode | String | 错误码，具体含义可查看[云录制2.0常见错误码](https://open.ys7.com/help/4488) |
| -errorMsg | String | 该错误信息为默认值，具体错误码对应的错误信息可查看[云录制2.0常见错误码](https://open.ys7.com/help/4488) |
| -totalSize | Long | 存储大小，单位B |
| -totalDuration | Long | 时长，单位秒 |
| -createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| -updateTime | String | 修改时间，yyyy-MM-DD HH:mm:ss |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 500 | 服务器异常 | 服务器内部错误 |
| 400 | 参数错误 | 请求参数有误 |