# 分页查询云点播任务详情（GET）

>  

> 更新时间: 2026-06-11T14:50:16.000+08:00

> 文档ID: 4941 | 来源树: 云存储

---

## 分页查询云点播任务详情

- 接口功能

   分页查询云点播任务详情，支持按时间范围和任务类型筛选

- 请求地址

`https://open.ys7.com/api/service/open/vod/tasks`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | pageStart | Int | 起始页码，默认0 | N |
| query | pageSize | Int | 每页条数，默认10 | N |
| query | startTime | String | 查询开始时间 | N |
| query | endTime | String | 查询结束时间 | N |
| query | taskType | Int | 任务类型，7:视频剪辑，8:转封装 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/open/vod/tasks?pageStart=0&pageSize=10&taskType=8' \
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
                "taskId": "d3b34f5e9c9943c2846c984e01a81649",
                "spaceId": "2026559",
                "deviceSerial": "K19978742",
                "channelNo": 1,
                "taskType": 8,
                "taskTypeDesc": "转封装",
                "taskStatus": 0,
                "totalSize": 3928824,
                "startTime": "2025-08-25 10:50:33",
                "endTime": "2025-08-25 10:51:27",
                "progressRate": 0,
                "createTime": "2025-09-10 20:19:23"
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
| meta.code | Int | 业务码，200表示成功 |
| meta.message | String | 响应信息 |
| data.result[].taskId | String | 任务ID |
| data.result[].spaceId | String | 空间ID |
| data.result[].deviceSerial | String | 设备序列号 |
| data.result[].channelNo | Int | 通道号 |
| data.result[].taskType | Int | 任务类型，7:视频剪辑，8:转封装 |
| data.result[].taskTypeDesc | String | 任务类型描述 |
| data.result[].taskStatus | Int | 任务状态，0-已完成，1-排队中，2-进行中，3-已结束，4-异常结束，5-暂停中，6-已取消，7-未开始 |
| data.result[].totalSize | Long | 文件大小，单位字节 |
| data.result[].startTime | String | 录像开始时间 |
| data.result[].endTime | String | 录像结束时间 |
| data.result[].progressRate | Int | 任务进度百分比 |
| data.result[].createTime | String | 任务创建时间 |
| data.pageStart | Int | 当前页码 |
| data.pageSize | Int | 每页条数 |
| data.total | Int | 总记录数 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 参数错误 | 请检查请求参数是否正确 |
| 500 | 服务器异常 | 服务端异常，请稍后重试 |