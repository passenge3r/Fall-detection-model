# API-设备云组件仓-执法记录仪-远程巡检组件-查询设备巡检轨迹

>  

> 更新时间: 2026-06-30T11:48:21.000+08:00

> 文档ID: 1539 | 来源树: OPEN_API

---

## 查询设备巡检轨迹

- 接口功能

   查询设备巡检轨迹，设备巡检期间行动轨迹在地图上显示。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/device/trace`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| query | inspectRecordId | Int | 巡检记录id | Y |
| query | pageStart | Int | 分页起始，从0开始 | N |
| query | pageSize | Int | 分页大小，默认10，最大50 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/device/trace?inspectRecordId=1&pageStart=0&pageSize=10' \
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
            "deviceSerial": "F08189125",
            "longitude": 120.219194,
            "latitude": 30.214132,
            "reportTime": "2023-06-20 20:02:47"
        },
        {
            "deviceSerial": "F08189125",
            "longitude": 120.219327,
            "latitude": 30.216095,
            "reportTime": "2023-06-20 20:03:17"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |
| data | Array<Object> | 数据 |
| data.deviceSerial | String | 设备序列号 |
| data.longitude | Float | 经度，用于标识位置经度，支持小数点后六位，不传默认为0，示例：116.263379 |
| data.latitude | Float | 纬度，用于标识位置纬度，支持小数点后六位，不传默认为0，示例：40.2273 |
| data.reportTime | String | 上报时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |