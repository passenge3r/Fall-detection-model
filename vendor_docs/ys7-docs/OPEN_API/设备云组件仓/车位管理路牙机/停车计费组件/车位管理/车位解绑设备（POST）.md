#  车位解绑设备（POST）

> 车位解绑设备（POST）

> 更新时间: 2026-05-25T16:39:01.000+08:00

> 文档ID: 1466 | 来源树: OPEN_API

---

# 车位解绑设备（POST）

> 车位解绑设备

---

## 接口URL

/api/service/devicekit/parking/parkingSpace/unbind

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |
| deviceSerial | string | Y | 设备序列号 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| spaceId | int | Y | 车位Id |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
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