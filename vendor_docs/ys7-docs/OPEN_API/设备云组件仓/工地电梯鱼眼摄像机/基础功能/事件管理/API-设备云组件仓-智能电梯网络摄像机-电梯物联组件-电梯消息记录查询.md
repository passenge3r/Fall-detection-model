# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-电梯消息记录查询

> 更新时间: 2026-06-30T11:55:27.000+08:00

> 文档ID: 1627 | 来源树: OPEN_API

---

## 电梯事件记录查询

- 接口功能

   电梯事件记录查询，获取电梯检测事件记录，包括不限于：运行事件，告警事件等

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/statistic/running`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | startTime | String | 查询开始时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | endTime | String | 查询结束时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | elevatorSerial | String | 电梯唯一id | N |
| query | eventType | String | 事件类型：elevatorRunningStatus-运行事件，AIOP\_Video-告警事件 | N |
| query | statusType | String | 状态类型：notWearHelmet-未戴安全帽，wearHelmet-戴安全帽，cart-推车，wearReflectiveClothing-穿反光衣，notWearReflectiveClothing-未穿反光衣，elevatorDoorOpen-电梯门开，elevatorDoorClose-电梯门关，overload-超载 | N |
| query | pageStart | Int | 开始查询的起始条数 | N |
| query | pageSize | Int | 查询的条数 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/statistic/running?startTime=2024-01-01 00:00:00&endTime=2024-01-01 23:59:59' \
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
            "deviceSerial": "DS123456",
            "worksiteId": "ws001",
            "channelId": 1,
            "elevatorSerial": "EL123456",
            "eventType": "AIOP_Video",
            "eventState": "alarm",
            "eventDescription": "超载告警",
            "dataTime": "2024-01-01 12:00:00",
            "statusType": "overload",
            "personNums": 10,
            "image": "https://example.com/img.jpg",
            "ipAddress": "192.168.1.100",
            "ipv6Address": "",
            "portNo": 8000,
            "protocol": "TCP",
            "macAddress": "00:11:22:33:44:55"
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
| data[].deviceSerial | String | 设备序列号 |
| data[].worksiteId | String | 区域id |
| data[].channelId | Int | 触发报警的通道号 |
| data[].elevatorSerial | String | 电梯id |
| data[].eventType | String | 事件类型 |
| data[].eventState | String | 事件状态 |
| data[].eventDescription | String | 事件描述 |
| data[].dataTime | String | 消息时间 |
| data[].statusType | String | 状态类型 |
| data[].personNums | Int | 载人人数 |
| data[].image | String | 图片信息 |
| data[].ipAddress | String | 设备IPv4地址 |
| data[].ipv6Address | String | 设备ipv6地址 |
| data[].portNo | Int | 设备端口号 |
| data[].protocol | String | 传输通信协议 |
| data[].macAddress | String | mac地址 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |