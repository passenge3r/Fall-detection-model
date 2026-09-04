# 查询停车统计数据（GET）

> 查询停车统计数据（GET）

> 更新时间: 2026-05-25T16:39:03.000+08:00

> 文档ID: 1470 | 来源树: OPEN_API

---

# 查询停车统计数据（GET）

> 查询停车统计数据

---

## 接口URL

/api/service/devicekit/parking/statistic/flow

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| lotNumber | string | N | 停车场编号 |  |
| vehicleType | string | N | 车辆类型 |  |
| vehicleBrand | string | N | 车辆品牌 |  |
| date | string | N | 日期，例：2023-03-20 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |
| data | array<object> |  |  |
| -create\_date | string | 日期 |  |
| -per\_hour | string | 小时 |  |
| -lot\_number | string | 停车场编号 |  |
| -space\_id | int | 停车位id |  |
| -vehicle\_brand | string | 车辆品牌 |  |
| -vehicle\_type | string | 车辆类型 |  |
| -avg\_stay | string | 平均停车时长 |  |
| -cnt\_stay | string | 停车总数 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": [
        {
            "create_date": "2023-03-20",
            "per_hour": "2023-03-20 07",
            "lot_number": "1-1",
            "space_id": 1,
            "vehicle_brand": "长安",
            "vehicle_type": "SUV/MPV",
            "avg_stay": "29400",
            "cnt_stay": "1"
        },
        {
            "create_date": "2023-03-20",
            "per_hour": "2023-03-20 16",
            "lot_number": "1-1",
            "space_id": 1,
            "vehicle_brand": "长安",
            "vehicle_type": "SUV/MPV",
            "avg_stay": "15000",
            "cnt_stay": "1"
        }
    ]
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 10001 | 10001 | 参数错误 |  |
| 10002 | 10002 | accessToken过期或异常 |  |
| 50000 | 50000 | 服务器异常 |  |