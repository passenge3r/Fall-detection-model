# API-设备云组件仓-执法记录仪-远程巡检组件-巡检复盘-查询巡检记录列表

> 更新时间: 2026-07-09T13:42:05.000+08:00

> 文档ID: 744 | 来源树: OPEN_API

---

## 查询巡检记录列表

- 接口功能

   查询巡检记录，以列表形式呈现，返回每条巡检记录的基本信息，包括设备序列号、巡检区域、巡检名称、巡检区域ID、巡检区域标识、巡检开始/结束时间、巡检状态、是否远程巡检、巡检人员/远程巡检人员及此条记录的创建、更新时间。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | N |
| Query | startTime | String | 查询开始时间，格式：yyyy-MM-dd HH:mm:ss | N |
| Query | endTime | String | 查询结束时间，格式：yyyy-MM-dd HH:mm:ss | N |
| Query | inspectRecordId | Int | 查询起始巡检记录ID，查询结果为ID大于所输入inspectRecordId的巡检记录 | N |
| Query | size | Int | 查询最大返回数量 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect/list?startTime=xxxxx&endTime=xxxxx&inspectRecordId=xxxxx&size=xxxxx' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": [
        {
            "inspectRecordId": 25,
            "deviceSerial": "E72039480",
            "inspectName": "",
            "inspectDistrict": "测试区域222",
            "inspectDistrictId": "",
            "inspectDistrictCode": "",
            "beginTime": "2023-02-27 20:15:06",
            "endTime": null,
            "inspectStatus": 1,
            "remoteInspectStatus": 0,
            "inspectPerson": null,
            "remoteInspectPerson": "chenchao2",
            "createTime": "2023-02-27 20:14:56",
            "updateTime": "2023-02-27 20:32:26"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| data | Array<object> | 巡检记录列表 |
| inspectRecordId | Int | 巡检记录ID |
| deviceSerial | String | 设备序列号 |
| inspectDistrict | String | 巡检区域 |
| inspectName | String | 巡检名称 |
| inspectDistrictId | String | 巡检区域id |
| inspectDistrictCode | String | 巡检区域标识，worksite-工地，worksite即为工地场景的标识 |
| beginTime | String | 巡检开始时间 |
| endTime | String | 巡检结束时间 |
| inspectStatus | Int | 巡检状态，0-巡检中，1-巡检结束 |
| remoteInspectStatus | Int | 远程巡检状态，0-未远程巡检，1-存在远程巡检 |
| inspectPerson | String | 巡检人员 |
| remoteInspectPerson | String | 远程巡检人员 |
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