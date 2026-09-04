# API-存储与媒体处理-云录制-视频采集与存储-修改已创建一次性录像计划的设备列表

> 更新时间: 2026-06-25T14:31:13.000+08:00

> 文档ID: 2050 | 来源树: 云存储

---

## 修改已创建一次性录像计划的设备列表

- 接口功能

   修改已创建一次性录像计划的设备列表。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | oneOffPlanId | Long | 单次计划ID | Y |
| body | planName | String | 计划名称，允许为中文、英文、数字、下划线、中划线1-32位 | Y |
| body | spaceId | Long | 空间ID | Y |
| body | startTime | String | 开始时间，格式：yyyyMMddHHmmss | Y |
| body | endTime | String | 结束时间，格式：yyyyMMddHHmmss | Y |
| body | devIndexInfos | Array<Object> | 通道列表，限制1-1000，大于10个通道时，将异步创建计划 | Y |
| body | devIndexInfos.deviceSerial | String | 设备序列号 | Y |
| body | devIndexInfos.localIndex | String | 通道号 | Y |
| body | devIndexInfos.validateCode | String | 设备验证码，设备加密且配置了后处理模板时，必填 | N |
| body | streamType | Int | 1主码流 2子码流 不填默认主码流 | N |
| body | templateId | Long | 模板ID | N |
| body | specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间 | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "oneOffPlanId": 5904,
    "spaceId": 44028,
    "templateId": 6,
    "specifiedEndTime": true,
    "devIndexInfos": [
        {
            "deviceSerial": "BC305511",
            "localIndex": "1"
        }
    ],
    "planName": "录制计划_template_20250612_2000_01Up",
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
        "oneOffPlanId": 5904,
        "planName": "录制计划_template_20250612_2000_01Up",
        "spaceId": 44028,
        "startTime": "2025-06-13 20:30:30",
        "endTime": "2025-06-13 20:35:30",
        "planDetail": "{\"streamType\":1,\"hours\":0,\"autoDelete\":false,\"autoConvertHls\":false,\"specifiedEndTime\":true,\"templateConfig\":{\"templateId\":6,\"templateName\":\"templateName2025-06-11-001-up\",\"templateType\":\"custom\",\"format\":\"mp4\",\"segmentDuration\":1800,\"keepPsStream\":1,\"spaceId\":44130,\"spaceName\":\"云点播_001\",\"audioFormat\":\"default\",\"videoCodec\":null,\"extraParams\":\"{}\",\"createTime\":\"2025-06-11 20:42:18\",\"updateTime\":\"2025-06-11 20:43:03\"}}",
        "planStatus": 1,
        "errorCode": null,
        "errorMsg": null,
        "deviceNum": 0,
        "createTime": "2025-06-13 14:20:05",
        "updateTime": "2025-06-13 14:20:41",
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
| meta.code | Int | 返回码 |
| meta.message | String | 返回信息 |
| meta.moreInfo | String | 更多信息 |
| data | Object | 数据 |
| data.oneOffPlanId | Int | 一次性计划ID |
| data.planName | String | 计划名称 |
| data.spaceId | Int | 空间ID |
| data.startTime | String | 开始时间 |
| data.endTime | String | 结束时间 |
| data.planDetail | String | 计划详情 |
| data.planStatus | Int | 计划状态，1.创建中（设备任务创建）；2.创建失败（任务创建失败，错误信息）；3.未开始（计划正式创建，未到达计划开始时间）；4.进行中（计划已经执行）；5.已终止（计划停止）；6.终止中（计划正在终止）；7.终止失败（计划终止过程中发生异常，此场景一般不出现，除非服务异常）；8.删除中（计划删除中）；9.删除失败（计划删除过程中发生异常，此场景一般不出现，除非服务异常） |
| data.createTime | String | 创建时间 |
| data.updateTime | String | 更新时间 |
| data.validDevInfos | Array<Object> | 有效设备列表 |
| data.validDevInfos.deviceSerial | String | 设备序列号 |
| data.validDevInfos.localIndex | String | 通道号 |
| data.invalidDevInfos | Array<Object> | 无效设备列表 |
| data.invalidDevInfos.deviceSerial | String | 设备序列号 |
| data.invalidDevInfos.localIndex | String | 通道号 |
| data.templateConfig | Object | 模板配置信息 |
| data.templateConfig.templateId | Int | 模板id |
| data.templateConfig.templateName | String | 模板名称 |
| data.templateConfig.templateType | String | 模板类型(system:系统预置;custom:自定义) |
| data.templateConfig.format | String | 转封装格式(HLS;mp4) |
| data.templateConfig.segmentDuration | Int | 切片时长(秒)，0表示不切分 |
| data.templateConfig.keepPsStream | Int | 是否保存PS码流(0否1是)，默认1 |
| data.templateConfig.spaceId | Int | 云点播空间id |
| data.templateConfig.spaceName | String | 云点播空间名称 |
| data.templateConfig.audioFormat | String | 音频格式(AAC,default) |
| data.templateConfig.videoCodec | Object | 视频编码格式 |
| data.templateConfig.extraParams | String | 扩展参数 |
| data.templateConfig.createTime | String | 创建时间 |
| data.templateConfig.updateTime | String | 修改时间 |
| data.specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码：200 |
| 500 | 服务器异常 | HTTP状态码：500 |
| 400 | 参数错误 | HTTP状态码：400 |
| 412 | 前置条件不满足 | HTTP状态码：412 |
| 406 | 平台不支持的操作 | HTTP状态码：406 |