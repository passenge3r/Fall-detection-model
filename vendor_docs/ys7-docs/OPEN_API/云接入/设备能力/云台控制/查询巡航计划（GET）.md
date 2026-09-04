# 查询巡航计划（GET）

> 查询巡航计划（GET）

> 更新时间: 2026-05-25T16:38:12.000+08:00

> 文档ID: 5065 | 来源树: OPEN_API

---

# 查询巡航计划（GET）

> 查询巡航计划

---

## 接口URL

https://open.ys7.com/api/v3/device/ptz/cruise/timePlan

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 用户令牌 |  |
| deviceSerial | string | Y | 设备序列号 |  |

### 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/ptz/cruise/timePlan' \
--header 'accessToken: at.0v38go2cdf814p7k3ne8xwvy2codwt1m-1ovws9vkav-18gf1pk-bnadjuikn' \
--header 'deviceSerial: BF7513110'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 返回信息 |  |
| -code | int | 错误码 |  |
| -message | string | 错误信息 |  |
| data | object | 返回数据 |  |
| -enable | int | 0关1开 |  |
| -timingPlanBasicInfos | string | 时间计划 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "enable": 0,
        "timingPlanBasicInfos": [
            {
                "startTime": "08:00",
                "endTime": "10:00",
                "week": "0,1"
            },
            {
                "startTime": "13:00",
                "endTime": "14:00",
                "week": "1,2"
            }
        ]
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |