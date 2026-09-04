# 分页查询停车场（GET）

> 分页查询停车场（GET）

> 更新时间: 2026-05-25T16:39:00.000+08:00

> 文档ID: 1461 | 来源树: OPEN_API

---

# 分页查询停车场（GET）

> 分页查询停车场

---

## 接口URL

/api/service/devicekit/parking/parkingLot/page

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | accessToken |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| id | int | Y | 起始停车场id，查出数据不包含该id |  |
| pageSize | int | Y | 分页大小，小于50 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object |  |  |
| -code | int | 错误码 |  |
| -message | string | 错误码描述 |  |
| data | array<object> |  |  |
| -lotId | int | 停车场id |  |
| -lotNumber | string | 停车场编号 |  |
| -lotName | string | 停车场名称 |  |
| -province | string | 省 |  |
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
    "data": [
        {
            "lotId": 1,
            "lotNumber": "1-1",
            "lotName": "路边停车场1",
            "province": "浙江省",
            "city": "杭州市",
            "district": "西兴街道",
            "street": "西兴街道",
            "detailAddress": "xxxxxxxxx"
        },
        {
            "lotId": 3,
            "lotNumber": "1-2",
            "lotName": "路边停车场2",
            "province": "浙江省",
            "city": "杭州市",
            "district": "西兴街道",
            "street": "西兴街道",
            "detailAddress": "xxxxxxxxx"
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