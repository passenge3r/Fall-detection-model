# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-电梯异常事件统计

> 更新时间: 2026-06-30T11:55:29.000+08:00

> 文档ID: 1628 | 来源树: OPEN_API

---

## 电梯异常事件统计

- 接口功能

   电梯异常告警事件统计查询，支持时间范围，电梯id，区域id等多维条件过滤查询

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/statistic/event`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | startTime | String | 查询开始时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | endTime | String | 查询结束时间，格式yyyy-MM-dd HH:mm:ss | Y |
| query | elevatorSerial | String | 电梯id | N |
| query | worksiteId | String | 区域id | N |
| query | statusType | String | 状态类型：notWearHelmet-未戴安全帽，wearHelmet-戴安全帽，cart-推车，wearReflectiveClothing-穿反光衣，notWearReflectiveClothing-未穿反光衣，elevatorDoorOpen-电梯门开，elevatorDoorClose-电梯门关，overload-超载 | Y |
| query | pageStart | Int | 开始查询的起始条数 | N |
| query | pageSize | Int | 查询条数 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/statistic/event?startTime=2024-01-01 00:00:00&endTime=2024-01-01 23:59:59&statusType=overload' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "overload": 5
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Object | 响应体 |
| data.statusType | Int | 返回查询的状态类型对应的数量 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |