# API-存储与媒体处理-云录制-视频采集与存储-创建一次性录制计划

> 更新时间: 2026-06-25T14:30:49.000+08:00

> 文档ID: 2045 | 来源树: 云存储

---

## API-存储与媒体处理-云录制-视频采集与存储-创建一次性录制计划

- 接口功能

   创建一次性录制计划。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/json | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | planName | String | 计划名称，允许为中文、英文、数字、下划线、中划线1-32位 | Y |
| body | spaceId | Long | 空间ID | Y |
| body | startTime | String | 开始时间，格式：yyyyMMddHHmmss | Y |
| body | endTime | String | 结束时间，格式：yyyyMMddHHmmss；当specifiedEndTime入参为false时，表示不指定时间，endTime入参可不传 | N |
| body | autoConvertHls | Boolean | 是否自动转换m3u8录像，默认false（该入参即将废弃，开发者建议尽快走后处理模板转m3u8） | N |
| body | autoDelete | Boolean | 是否1天后自动删除，默认false | N |
| body | devIndexInfos | Array<Object> | 通道列表，限制1-1000，大于10个通道时，将异步创建计划 | Y |
| body | -deviceSerial | String | 设备序列号 | Y |
| body | -localIndex | String | 通道号 | Y |
| body | -validateCode | String | 设备验证码，设备加密时且配置了后处理模版时必填 | N |
| body | streamType | Int | 1主码流 2子码流 不填默认主码流 | N |
| body | templateId | Long | 模板ID，可通过 https://open.ys7.com/help/4382 查询模板列表；模板相关介绍可查看 https://open.ys7.com/help/4383 | N |
| body | specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间；specifiedEndTime入参为false时，表示不指定结束时间 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "spaceId": 44028,
    "autoConvertHls": false,
    "templateId": 6,
    "autoDelete": false,
    "specifiedEndTime": true,
    "devIndexInfos": [
        {
            "deviceSerial": "BC30551",
            "localIndex": "1"
        }
    ],
    "planName": "录制计划_template_20250612_2000_01",
    "startTime": "20250613203030",
    "endTime": "20250613203530"
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
        "oneOffPlanId": 590,
        "planName": "录制计划_template_20250612_2000_01",
        "spaceId": 44028,
        "startTime": "2025-06-13 20:30:30",
        "endTime": "2025-06-13 20:35:30",
        "planDetail": "{\"streamType\":1,\"hours\":0,\"autoDelete\":false,\"autoConvertHls\":false,\"specifiedEndTime\":true,\"templateConfig\":{\"templateId\":6,\"templateName\":\"templateName2025-06-11-001-up\",\"templateType\":\"custom\",\"format\":\"mp4\",\"segmentDuration\":1800,\"keepPsStream\":1,\"spaceId\":44130,\"spaceName\":\"云点播_001\",\"audioFormat\":\"default\",\"videoCodec\":null,\"extraParams\":\"{}\",\"createTime\":\"2025-06-11 20:42:18\",\"updateTime\":\"2025-06-11 20:43:03\"}}",
        "planStatus": 3,
        "errorCode": null,
        "errorMsg": null,
        "deviceNum": 0,
        "createTime": "2025-06-13 12:56:42",
        "updateTime": "2025-06-13 12:56:42",
        "planType": 1,
        "hours": null,
        "validDevInfos": [
            {
                "deviceSerial": "BC3055114",
                "localIndex": "1"
            }
        ],
        "invalidDevInfos": [],
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
| -startTime | String | 开始时间 |
| -endTime | String | 结束时间 |
| -planDetail | String | 计划详情 |
| -planStatus | Int | 计划状态，1.创建中（设备任务创建） 2.创建失败（任务创建失败，错误信息） 3.未开始（计划正式创建，未到达计划开始时间） 4.进行中（计划已经执行） 5.已终止（计划停止） 6.终止中（计划正在终止） 7.终止失败（计划终止过程中发生异常） 8.删除中（计划删除中） 9.删除失败（计划删除过程中发生异常） 10.异常 11.已完成 |
| -createTime | String | 创建时间 |
| -updateTime | String | 更新时间 |
| -validDevInfos | Array<Object> | 有效设备列表 |
| --deviceSerial | String | 设备序列号 |
| --localIndex | String | 通道号 |
| -invalidDevInfos | Array<Object> | 无效设备列表 |
| --deviceSerial | String | 设备序列号 |
| --localIndex | String | 通道号 |
| -templateConfig | Object | 后处理模板配置信息 |
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
| --createTime | String | 创建时间 |
| --updateTime | String | 修改时间 |
| -specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间；specifiedEndTime入参为false时，表示不指定结束时间，endTime出参中的时间表示当前该计划会自动执行到什么时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 500 | 服务器异常 | 服务器内部异常 |
| 400 | 参数错误 | 请求参数错误 |
| 412 | 前置条件不满足 | 前置条件不满足 |
| 406 | 平台不支持的操作 | 平台不支持的操作 |