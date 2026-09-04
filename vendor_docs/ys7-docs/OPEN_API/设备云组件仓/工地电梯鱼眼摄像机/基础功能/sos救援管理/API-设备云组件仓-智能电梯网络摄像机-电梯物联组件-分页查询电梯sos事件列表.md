# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-分页查询电梯sos事件列表

> 更新时间: 2026-06-30T11:55:34.000+08:00

> 文档ID: 1630 | 来源树: OPEN_API

---

## 查询电梯困人告警事件列表

- 接口功能

   获取电梯困人告警事件列表

- 请求地址

`https://open.ys7.com/api/devicekit/elevator/sos/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | elevatorSerial | String | 电梯id | Y |
| query | startTime | String | 开始时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | endTime | String | 结束时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | size | Int | 查询条数 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/devicekit/elevator/sos/list?elevatorSerial=EL123456&startTime=2024-01-01 00:00:00&endTime=2024-01-01 23:59:59&size=10' \
--header 'accessToken: at.xxxxx'
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
            "elevatorSerial": "EL123456",
            "eventType": "sos",
            "eventId": "evt001",
            "triggerTime": "2024-01-01 12:00:00",
            "resumeTime": "2024-01-01 12:10:00",
            "rescueStartTime": "2024-01-01 12:02:00",
            "rescueEndTime": "2024-01-01 12:09:00",
            "createTime": "2024-01-01 12:00:00",
            "modifyTime": "2024-01-01 12:10:00",
            "recordDetailVos": {
                "eventId": "evt001",
                "triggerTime": "2024-01-01 12:00:00",
                "floor": 3,
                "doorCloseTime": 2,
                "customFloorName": "3F",
                "personStat": 1,
                "personNum": 2,
                "stuckTime": 600,
                "imageUrl": "https://example.com/img.jpg"
            }
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Array | 响应体 |
| data[].elevatorSerial | String | 电梯id |
| data[].eventType | String | 事件类型 |
| data[].eventId | String | 事件id |
| data[].triggerTime | String | 事件触发时间，电梯故障开始时间 |
| data[].resumeTime | String | 事件恢复时间，故障结束电梯恢复正常时间 |
| data[].rescueStartTime | String | 救援开始时间 |
| data[].rescueEndTime | String | 救援结束时间 |
| data[].createTime | String | 记录创建时间 |
| data[].modifyTime | String | 修改时间 |
| data[].recordDetailVos | Object | 记录详细信息 |
| data[].recordDetailVos.eventId | String | 事件id |
| data[].recordDetailVos.triggerTime | String | 事件触发时间 |
| data[].recordDetailVos.floor | Int | 楼层 |
| data[].recordDetailVos.doorCloseTime | Int | 关门次数 |
| data[].recordDetailVos.customFloorName | String | 自定楼层名 |
| data[].recordDetailVos.personStat | Int | 人员统计 |
| data[].recordDetailVos.personNum | Int | 人数 |
| data[].recordDetailVos.stuckTime | Int | 困人时间 |
| data[].recordDetailVos.imageUrl | String | 图片url |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |