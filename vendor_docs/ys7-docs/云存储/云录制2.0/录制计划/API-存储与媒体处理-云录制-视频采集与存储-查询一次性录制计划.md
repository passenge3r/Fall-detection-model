# API-存储与媒体处理-云录制-视频采集与存储-查询一次性录制计划

> 更新时间: 2026-06-25T14:30:57.000+08:00

> 文档ID: 2047 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-查询一次性录制计划

- 接口功能

   查询一次性录制计划。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | oneOffPlanId | String | 一次性计划ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff?oneOffPlanId=590404' \
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
        "oneOffPlanId": 5904,
        "planName": "录制计划_template_20250612_2000_01Up",
        "spaceId": 44028,
        "startTime": "2025-06-13 20:30:30",
        "endTime": "2025-06-13 20:35:30",
        "planDetail": "{\"streamType\":1,\"hours\":0,\"autoDelete\":false,\"autoConvertHls\":false,\"specifiedEndTime\":true,\"templateConfig\":{\"templateId\":6,\"templateName\":\"templateName2025-06-11-001-up\",\"templateType\":\"custom\",\"format\":\"mp4\",\"segmentDuration\":1800,\"keepPsStream\":1,\"spaceId\":44130,\"spaceName\":\"云点播_001\",\"audioFormat\":\"default\",\"videoCodec\":null,\"extraParams\":\"{}\",\"createTime\":\"2025-06-11 20:42:18\",\"updateTime\":\"2025-06-11 20:43:03\"}}",
        "planStatus": 3,
        "errorCode": null,
        "errorMsg": "ok",
        "deviceNum": 1,
        "createTime": "2025-06-13 14:20:05",
        "updateTime": "2025-06-13 14:20:42",
        "planType": 1,
        "hours": null,
        "templateConfig": {
            "templateId": 6,
            "templateName": "templateName2025-06-11-001-up",
            "templateType": "custom",
            "format": "mp4",
            "segmentDuration": 1800,
            "keepPsStream": 1,
            "spaceId": 44130,
            "spaceName": "云点播_001",
            "audioFormat": "default",
            "videoCodec": null,
            "extraParams": "{}",
            "createTime": "2025-06-11 20:42:18",
            "updateTime": "2025-06-11 20:43:03"
        },
        "specifiedEndTime": true
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回体 |
| -code | Int | 返回码 |
| -message | String | 返回信息 |
| -moreInfo | String | 更多信息 |
| data | Object | 数据 |
| -oneOffPlanId | Int | 一次性计划ID |
| -planName | String | 计划名称 |
| -spaceId | Int | 空间ID |
| -startTime | String | 开始时间，yyyy-MM-DD HH:mm:ss |
| -endTime | String | 结束时间，yyyy-MM-DD HH:mm:ss |
| -planDetail | String | 计划详情 |
| -planStatus | Int | 计划状态，1.创建中（设备任务创建） 2.创建失败（任务创建失败，错误信息） 3.未开始（计划正式创建，未到达计划开始时间） 4.进行中（计划已经执行） 5.已终止（计划停止） 6.终止中（计划正在终止） 7.终止失败（计划终止过程中发生异常） 8.删除中（计划删除中） 9.删除失败（计划删除过程中发生异常） 10.异常 11.已完成 |
| -createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| -updateTime | String | 更新时间，yyyy-MM-DD HH:mm:ss |
| -deviceNum | Int | 该计划的设备数量 |
| -planType | Int | 计划类型，1.一次性录像计划；2.批量录像计划；3.即时录像计划 |
| -hours | Object | planType为3，即时录制时，该字段有值，表示几个小时 |
| -templateConfig | Object | 模板配置信息 |
| --templateId | Int | 模板id |
| --templateName | String | 模板名称 |
| --templateType | String | 模板类型(system:系统预置;custom:自定义) |
| --format | String | 转封装格式(HLS;mp4) |
| --segmentDuration | Int | 切片时长(秒)，0表示不切分 |
| --keepPsStream | Int | 是否保存PS码流(0否1是),默认1 |
| --spaceId | Int | 云点播空间id |
| --spaceName | String | 云点播空间名称 |
| --audioFormat | String | 音频格式(AAC,default) |
| --videoCodec | Object | 视频编码格式 |
| --extraParams | String | 扩展参数 |
| --createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| --updateTime | String | 修改时间，yyyy-MM-DD HH:mm:ss |
| -specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间；specifiedEndTime入参为false时，表示不指定结束时间，endTime出参中的时间表示当前该计划会自动执行到什么时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 500 | 服务器异常 | 服务器内部异常 |
| 400 | 参数错误 | 请求参数错误 |