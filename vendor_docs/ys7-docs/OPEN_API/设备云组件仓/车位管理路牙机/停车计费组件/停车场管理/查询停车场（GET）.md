#  查询停车场（GET）

> 查询停车场（GET）

> 更新时间: 2026-05-25T16:39:00.000+08:00

> 文档ID: 1460 | 来源树: OPEN_API

---

# 查询停车场（GET）

> 查询停车场

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

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |
| data | object |  |  |
| -lotId | int | 停车场id |  |
| -lotNumber | string | 停车场编号 |  |
| -lotName | string | 停车场名称 |  |
| -province | string | 省份 |  |
| -city | string | 市 |  |
| -district | string | 区 |  |
| -street | string | 街道 |  |
| -detailAddress | string | 详细地址 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "lotId": 15,
        "lotNumber": "1-8",
        "lotName": "路边停车场1-8",
        "province": "浙江省",
        "city": "杭州市",
        "district": "西兴街道",
        "street": "西兴街道",
        "detailAddress": "xxxxxxxxx8"
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