# API-存储与媒体处理-云录制-任务操作-分页查询任务列表接口

> 更新时间: 2026-06-30T17:51:46.000+08:00

> 文档ID: 1371 | 来源树: 云存储

---

## 分页查询任务列表接口

- 接口功能

   分页查询任务列表接口。

- 请求地址

`https://open.ys7.com/api/v3/open/cloud/tasks`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 授权过程获取的accessToken | Y |
| Query | pageNumber | Int | 分页页码，以0开始，默认为0 | N |
| Query | pageSize | Int | 分页大小 | N |
| Query | startTime | String | 查询起始时间，若不传时间则默认当天，格式: yyyyMMddHHmmss | N |
| Query | endTime | String | 查询结束时间，若不传时间则默认当天，格式: yyyyMMddHHmmss，结束时间与开始时间不允许跨天，查询时间以任务创建时间为准，目前不支持排序 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/open/cloud/tasks?accessToken=at.xxxxx&startTime=20221216143333&endTime=20221216211011&pageNumber=0&pageSize=2'
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
            "taskId": "014f0e3fb6d6482a93fbe8416be4a9d6",
            "projectId": "test_syq_0427_1",
            "deviceSerial": "D88600067",
            "channelNo": 1,
            "taskType": 3,
            "taskSubType": 30,
            "taskStatus": 0,
            "taskDetail": {
                "validateCode": "",
                "recType": "local",
                "devProto": "",
                "frameInterval": 0,
                "frameModel": 0,
                "streamType": null,
                "voiceSwitch": 1,
                "aiBox": 1,
                "format": "mp4",
                "retryNum": 0,
                "sliceDuration": 30,
                "recordSpeed": "1"
            },
            "fileNum": 1,
            "totalSize": 10197644,
            "startTime": "2022-08-18T10:22:45",
            "endTime": "2022-08-18T10:25:00",
            "timingPoints": null,
            "errorCode": "0",
            "errorMsg": null,
            "createTime": "2022-08-18T22:29:20"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Array | 任务列表 |
| data[].taskId | String | 任务id |
| data[].projectId | String | 项目id |
| data[].deviceSerial | String | 设备序列号 |
| data[].channelNo | Int | 通道号 |
| data[].taskType | Int | 任务类型 1-视频抽帧 2-预览录制 3-回放录制 4-即时录制 5-全景图片采集 6-抓拍 |
| data[].taskSubType | Int | 任务子类型 10-按时间间隔抽帧 11-按时间点列表抽帧 60-按时间间隔抓拍 61-按时间点列表抓拍 |
| data[].taskStatus | Int | 任务状态 0-已完成 1-等待中 2-处理中 3-已结束 4-异常结束 |
| data[].taskDetail | Object | 任务详情 |
| data[].taskDetail.recType | String | 录像类型 local-本地录像 cloud-云存储录像 live-实时 |
| data[].taskDetail.devProto | String | 设备协议 |
| data[].taskDetail.frameInterval | Int | 抽帧间隔，普通模式单位秒；抽I帧模式传GOP间隔倍数 |
| data[].taskDetail.frameModel | Int | 抽帧模式 0-普通模式 1-错峰抽帧模式 2-抽I帧模式；默认0 |
| data[].taskDetail.streamType | String | 码流类型 1-高清（主码流） 2-标清（子码流）；默认1 |
| data[].taskDetail.voiceSwitch | Int | 录制视频声音开关 0-关 1-开 2-自动 默认2，如果音频不是AAC，则自动关闭视频声音 |
| data[].taskDetail.aiBox | Int | 是否需要录制Ai框，0关 1开，默认关闭 |
| data[].taskDetail.format | String | 视频封装类型，默认mp4，ps为直接录制ps流 |
| data[].fileNum | Int | 文件个数 |
| data[].totalSize | Long | 任务文件总大小 |
| data[].startTime | String | 任务开始时间 |
| data[].endTime | String | 任务结束时间 |
| data[].timingPoints | String | 时间点列表 |
| data[].createTime | String | 任务创建时间 |
| data[].errorCode | String | 错误码 |
| data[].errorMsg | String | 错误信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |