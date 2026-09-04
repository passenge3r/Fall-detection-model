# 分页查询车位信息（GET）

> 分页查询车位信息（GET）

> 更新时间: 2026-05-25T16:39:02.000+08:00

> 文档ID: 1468 | 来源树: OPEN_API

---

# 分页查询车位信息（GET）

> 分页查询车位信息

---

## 接口URL

/api/service/devicekit/parking/parkingSpace/page

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |
| deviceSerial | string | Y | 设备序列号 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| lotNumber | string | N | 停车场编号，不传或传空则查询账号下所有停车位 |  |
| id | int | Y | 起始车位id，不包含当前id |  |
| pageSize | int | Y | 分页大小，小于50 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |
| data | array<object> |  |  |
| -spaceId | int | 停车位id |  |
| -lotNumber | string | 停车场编号 |  |
| -spaceNumber | string | 泊位号 |  |
| -deviceSerial | string | 设备序列号 |  |
| -spaceStatus | int | 停车状态 0 无车 1 有车 |  |
| -plateNumber | string | 车牌号 |  |
| -vehicleColor | string | 车辆颜色 |  |
| -vehicleType | string | 车辆类型 |  |
| -vehicleBrand | string | 车辆品牌 |  |
| -enterTime | string | 入车时间 |  |
| -departTime | string | 出车时间 |  |
| -parkDuration | int | 停车时长 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": [
        {
            "spaceId": 1,
            "lotNumber": "1-1",
            "spaceNumber": "1",
            "deviceSerial": "K90134622",
            "spaceStatus": 0,
            "plateNumber": "沪E88888",
            "vehicleColor": "",
            "vehicleType": "",
            "vehicleBrand": "",
            "enterTime": "2023-01-02 00:00:15",
            "departTime": "2023-05-16 20:49:26",
            "parkDuration": 194209
        },
        {
            "spaceId": 3,
            "lotNumber": "1-1",
            "spaceNumber": "2",
            "deviceSerial": "K61429927",
            "spaceStatus": 0,
            "plateNumber": "",
            "vehicleColor": "",
            "vehicleType": "",
            "vehicleBrand": "",
            "enterTime": null,
            "departTime": null,
            "parkDuration": 0
        },
        {
            "spaceId": 45,
            "lotNumber": "1-1",
            "spaceNumber": "500",
            "deviceSerial": "",
            "spaceStatus": 0,
            "plateNumber": "",
            "vehicleColor": "",
            "vehicleType": "",
            "vehicleBrand": "",
            "enterTime": null,
            "departTime": null,
            "parkDuration": 0
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
| 20018 | 20018 | 该用户不拥有该设备 |  |
| 50000 | 50000 | 服务器异常 |  |