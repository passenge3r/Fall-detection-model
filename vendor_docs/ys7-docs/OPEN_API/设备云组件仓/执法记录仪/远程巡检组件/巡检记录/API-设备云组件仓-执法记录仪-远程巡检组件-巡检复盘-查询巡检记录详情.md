# API-设备云组件仓-执法记录仪-远程巡检组件-巡检复盘-查询巡检记录详情

> 更新时间: 2026-07-09T13:42:08.000+08:00

> 文档ID: 745 | 来源树: OPEN_API

---

## 查询巡检记录详情

- 接口功能

   查询每条巡检记录的详细信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Body | inspectRecordId | Int | 巡检记录ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'inspectRecordId=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "inspectRecordId": 29,
        "deviceSerial": "L16120197",
        "inspectName": "研发测试b2--郭旺",
        "inspectDistrict": "213113",
        "inspectDistrictId": "`22`",
        "inspectDistrictCode": "2`2`2",
        "beginTime": "2023-02-28 00:10:12",
        "endTime": "2023-07-05 16:29:14",
        "inspectStatus": 1,
        "remoteInspectStatus": 0,
        "inspectPerson": "31313",
        "remoteInspectPerson": "314sdas",
        "createTime": "2023-02-28 00:10:03",
        "updateTime": "2023-07-05 16:29:16",
        "eventList": [{
            "inspectEventId": 51,
            "inspectRecordId": 29,
            "eventTime": null,
            "eventBeginTime": null,
            "eventEndTime": null,
            "depositaryOfficer": "",
            "eventRemark": "",
            "eventType": "预录事件类型33",
            "evidenceFileSource": "cloud_record",
            "evidenceFileId": "d14901c46b6e4b1eb23eea4183b0e5a2",
            "evidenceFileType": -1,
            "createTime": "2023-02-28 15:50:27",
            "updateTime": "2023-03-03 11:22:03",
            "fileUrl": null
        }]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| data | Object | data |
| inspectRecordId | Int | 巡检记录ID |
| deviceSerial | String | 设备序列号 |
| inspectName | String | 巡检名称 |
| inspectDistrictId | String | 巡检区域id |
| inspectDistrictCode | String | 巡检区域标识, worksite-工地 ，worksite即为工地场景的标识 |
| inspectDistrict | String | 巡检区域 |
| beginTime | String | 巡检开始时间 |
| endTime | String | 巡检结束时间 |
| inspectStatus | Int | 0-巡检中 1-巡检完成 |
| remoteInspectStatus | Int | 0-无远程巡检 1-有远程巡检 |
| inspectPerson | String | 巡检人员 |
| remoteInspectPerson | String | 远程巡检人员 |
| createTime | String | 创建时间 |
| updateTime | String | 更新时间 |
| eventList | Object | 巡检事件列表 |
| inspectEventId | Int | 巡检事件ID |
| inspectRecordId | Int | 巡检记录ID |
| eventTime | String | 事件时间（图片类型事件时间） yyyy-MM-dd HH:mm:ss |
| eventBeginTime | String | 事件起始时间（视频录制类型事件时间） yyyy-MM-dd HH:mm:ss |
| eventEndTime | String | 事件结束时间（视频录制类型事件时间） yyyy-MM-dd HH:mm:ss |
| depositaryOfficer | String | 存证人员 |
| eventRemark | String | 事件备注 |
| evidenceFileType | Int | 事件存证文件类型 0-图片 1-视频 |
| eventType | String | 事件标签 |
| evidenceFileSource | String | local-本地 cloud\_record-云录制 |
| evidenceFileId | String | 存证文件ID |
| createTime | String | 创建时间 |
| updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |