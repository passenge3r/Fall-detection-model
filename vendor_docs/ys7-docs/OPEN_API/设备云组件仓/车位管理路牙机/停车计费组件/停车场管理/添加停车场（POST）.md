# 添加停车场（POST）

> 添加停车场（POST）

> 更新时间: 2026-05-25T16:38:59.000+08:00

> 文档ID: 1457 | 来源树: OPEN_API

---

# 添加停车场（POST）

> 添加停车场

---

## 接口URL

/api/service/devicekit/parking/parkingLot

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| lotNumber | string | Y | 停车场编号，小于64字符 |  |
| lotName | string | N | 停车场名称，小于64字符 |  |
| province | string | N | 省份，小于18字符 |  |
| city | string | N | 市，小于32字符 |  |
| district | string | N | 区，小于64字符 |  |
| street | string | N | 街道，小于64字符 |  |
| detailAddress | string | N | 详细地址，小于128字符 |  |

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
| 50000 | 50000 | 服务器异常 |  |