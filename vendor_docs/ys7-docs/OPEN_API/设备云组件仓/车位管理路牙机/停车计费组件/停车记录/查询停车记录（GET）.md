# 查询停车记录（GET）

>  

> 更新时间: 2026-06-30T17:55:50.000+08:00

> 文档ID: 1469 | 来源树: OPEN_API

---

## 查询停车记录

- 接口功能

   查询停车记录。

- 请求地址

`https://open.ys7.com/api/service/devicekit/parking/parkingRecord`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | accessToken | Y |
| query | spaceId | Int | 停车位id | Y |
| query | id | Int | 记录id，不包含当前id | Y |
| query | pageSize | Int | 分页大小，小于50 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/parking/parkingRecord?spaceId=1&id=0&pageSize=10' \
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
            "id": 1,
            "spaceId": 1,
            "lotNumber": "A001",
            "deviceSerial": "K90123422",
            "plateNumber": "浙A12345",
            "vehicleColor": "白色",
            "vehicleType": "小型车",
            "vehicleBrand": "大众",
            "enterPic": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "departPic": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "enterTime": "2023-04-27 08:00:00",
            "departTime": "2023-04-27 12:00:00",
            "parkDuration": 240,
            "parkResult": 1,
            "errorInfo": ""
        },
        {
            "id": 2,
            "spaceId": 1,
            "lotNumber": "A001",
            "deviceSerial": "K90123422",
            "plateNumber": "浙B67890",
            "vehicleColor": "黑色",
            "vehicleType": "小型车",
            "vehicleBrand": "宝马",
            "enterPic": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "departPic": "https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxx&fileKey=xxx",
            "enterTime": "2023-04-27 13:00:00",
            "departTime": "2023-04-27 17:30:00",
            "parkDuration": 270,
            "parkResult": 1,
            "errorInfo": ""
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
| data | Array<Object> | 停车记录列表 |
| data.id | Int | 记录id |
| data.spaceId | Int | 停车位id |
| data.lotNumber | String | 车位编号 |
| data.deviceSerial | String | 设备序列号 |
| data.plateNumber | String | 车牌号 |
| data.vehicleColor | String | 车辆颜色 |
| data.vehicleType | String | 车辆类型 |
| data.vehicleBrand | String | 车辆品牌 |
| data.enterPic | String | 入场图片地址 |
| data.departPic | String | 出场图片地址 |
| data.enterTime | String | 入场时间 |
| data.departTime | String | 出场时间 |
| data.parkDuration | Int | 停车时长（分钟） |
| data.parkResult | Int | 停车结果 |
| data.errorInfo | String | 错误信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 50000 | 服务器异常 | 服务器异常 |