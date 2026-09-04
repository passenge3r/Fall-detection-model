# API-存储与媒体处理-云录制-视频采集与存储-查询一次性录制计划列表

> 更新时间: 2026-06-25T14:31:16.000+08:00

> 文档ID: 2051 | 来源树: 云存储

---

## 查询一次性录制计划列表

- 接口功能

   查询一次性录制计划列表。是否支持托管：否；是否支持子帐号：否。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/listById`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| query | lastOneOffPlanId | Long | 上一页计划ID | Y |
| query | pageSize | Int | 分页大小，范围：1-50，默认10 | Y |
| query | startTime | String | 开始时间，格式yyyyMMddHHmmss | Y |
| query | endTime | String | 结束时间，格式yyyyMMddHHmmss，开始时间和结束时间必须在同一天 | Y |
| query | spaceId | Long | 空间ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/cloudrecord/video/plan/oneOff/listById?lastOneOffPlanId=0&pageSize=10&startTime=20250613000000&endTime=20250613235959&spaceId=44028' \
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
        "plansInfo": [
            {
                "oneOffPlanId": 589872,
                "planName": "线上验证_001",
                "spaceId": 44028,
                "startTime": "2025-06-13 09:30:01",
                "endTime": "2025-06-14 09:30:03",
                "planDetail": "{\"streamType\":1,\"hours\":0,\"autoDelete\":false,\"autoConvertHls\":false,\"specifiedEndTime\":true,\"templateConfig\":null}",
                "planStatus": 10,
                "errorCode": "5405",
                "errorMsg": "设备取流异常",
                "deviceNum": 2,
                "createTime": "2025-06-13 09:30:27",
                "updateTime": "2025-06-13 10:38:12",
                "planType": 1,
                "hours": null,
                "templateConfig": null,
                "specifiedEndTime": true
            },
            {
                "oneOffPlanId": 589878,
                "planName": "线上验证_003",
                "spaceId": 44028,
                "startTime": "2025-06-13 09:35:08",
                "endTime": "2025-06-14 09:35:08",
                "planDetail": "{\"streamType\":1,\"hours\":0,\"autoDelete\":false,\"autoConvertHls\":false,\"specifiedEndTime\":false,\"templateConfig\":{\"templateId\":24,\"templateName\":\"线上验证\",\"templateType\":\"custom\",\"format\":\"HLS\",\"segmentDuration\":0,\"keepPsStream\":1,\"spaceId\":44130,\"spaceName\":\"云点播_001\",\"audioFormat\":\"AAC\",\"videoCodec\":null,\"extraParams\":\"{}\",\"createTime\":\"2025-06-13 09:11:46\",\"updateTime\":\"2025-06-13 09:11:46\"}}",
                "planStatus": 4,
                "errorCode": "6520",
                "errorMsg": "设备取流异常",
                "deviceNum": 2,
                "createTime": "2025-06-13 09:31:48",
                "updateTime": "2025-06-13 10:43:42",
                "planType": 1,
                "hours": null,
                "templateConfig": {
                    "templateId": 24,
                    "templateName": "线上验证",
                    "templateType": "custom",
                    "format": "HLS",
                    "segmentDuration": 0,
                    "keepPsStream": 1,
                    "spaceId": 44130,
                    "spaceName": "云点播_001",
                    "audioFormat": "AAC",
                    "videoCodec": null,
                    "extraParams": "{}",
                    "createTime": "2025-06-13 09:11:46",
                    "updateTime": "2025-06-13 09:11:46"
                },
                "specifiedEndTime": false
            }
        ],
        "lastOneOffPlanId": 589878,
        "pageSize": 10,
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
| data.plansInfo | Array<Object> | 计划列表 |
| data.plansInfo.oneOffPlanId | Int | 一次性计划ID |
| data.plansInfo.planName | String | 计划名称 |
| data.plansInfo.spaceId | Int | 空间ID |
| data.plansInfo.startTime | String | 开始时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.endTime | String | 结束时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.planDetail | String | 计划详情 |
| data.plansInfo.planStatus | Int | 计划状态：1.创建中（设备任务创建）；2.创建失败（任务创建失败，错误信息）；3.未开始（计划正式创建，未到达计划开始时间）；4.进行中（计划已经执行）；5.已终止（计划停止）；6.终止中（计划正在终止）；7.终止失败（计划终止过程中发生异常）；8.删除中（计划删除中）；9.删除失败（计划删除过程中发生异常）；10.异常；11.已完成 |
| data.plansInfo.errorCode | String | 错误码 |
| data.plansInfo.errorMsg | String | 错误信息描述 |
| data.plansInfo.deviceNum | Int | 该计划的设备数量 |
| data.plansInfo.createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.updateTime | String | 更新时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.planType | Int | 计划类型，1.一次性录像计划；2.批量录像计划；3.即时录像计划 |
| data.plansInfo.hours | Int | planType为3，即时录制时，该字段有值，表示几个小时 |
| data.plansInfo.templateConfig | Object | 模板配置信息 |
| data.plansInfo.templateConfig.templateId | Int | 模板id |
| data.plansInfo.templateConfig.templateName | String | 模板名称 |
| data.plansInfo.templateConfig.templateType | String | 模板类型(system:系统预置;custom:自定义) |
| data.plansInfo.templateConfig.format | String | 转封装格式(HLS;mp4) |
| data.plansInfo.templateConfig.segmentDuration | Int | 切片时长(秒)，0表示不切分 |
| data.plansInfo.templateConfig.keepPsStream | Int | 是否保存PS码流(0否1是)，默认1 |
| data.plansInfo.templateConfig.spaceId | Int | 云点播空间id |
| data.plansInfo.templateConfig.spaceName | String | 云点播空间名称 |
| data.plansInfo.templateConfig.audioFormat | String | 音频格式(AAC,default) |
| data.plansInfo.templateConfig.videoCodec | Object | 视频编码格式 |
| data.plansInfo.templateConfig.extraParams | String | 扩展参数 |
| data.plansInfo.templateConfig.createTime | String | 创建时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.templateConfig.updateTime | String | 修改时间，yyyy-MM-DD HH:mm:ss |
| data.plansInfo.specifiedEndTime | Boolean | 是否指定结束时间，默认true表示指定结束时间。**specifiedEndTime入参为false时，表示不指定结束时间，endTime出参中的时间表示当前该计划的会自动执行到什么时间** |
| data.lastOneOffPlanId | Int | 上一页最后计划ID |
| data.pageSize | Int | 分页大小 |
| data.hasNext | Boolean | 是否有下一页 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | HTTP状态码：200 |
| 404 | 资源不存在 | HTTP状态码：404 |
| 500 | 服务器异常 | HTTP状态码：500 |