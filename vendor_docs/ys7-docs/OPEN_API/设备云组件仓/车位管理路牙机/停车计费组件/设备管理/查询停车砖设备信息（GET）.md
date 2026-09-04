# 查询停车砖设备信息（GET）

> 查询停车砖设备信息（GET）

> 更新时间: 2026-05-25T16:39:02.000+08:00

> 文档ID: 1463 | 来源树: OPEN_API

---

# 查询停车砖设备信息（GET）

> 查询停车砖设备信息

---

## 接口URL

/api/service/devicekit/parking/device/info

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |
| deviceSerial | string | Y | 设备序列号 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |
| data | object |  |  |
| -deviceSerial | string | 设备序列号 |  |
| -deviceName | string | 设备名称 |  |
| -status | int | 设备在线状态 0-不在线，1-在线 |  |
| -addTime | string | 设备添加时间 |  |
| -offlineTime | string | 离线时间 |  |
| -batteryStatus | int | 电池电量,1到100(%)，-1:设备没有上报或者设备不支持该状态 |  |
| -nbCardId | string | 物联网卡号 |  |
| -remainingTrafficVolume | int | 剩余流量（MB） |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "deviceSerial": "K90132222",
        "deviceName": "停车砖设备",
        "status": 1,
        "addTime": "2023-03-10 21:07:10",
        "offlineTime": "2023-03-15 00:02:37",
        "batteryStatus": 100,
        "nbCardId": "8126342129908240000",
        "remainingTrafficVolume": 24576.0
    }
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