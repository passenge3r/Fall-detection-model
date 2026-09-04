# API-存储与媒体处理-云存储-AI云存储模型列表

> API-存储与媒体处理-云存储-AI云存储模型列表

> 更新时间: 2026-05-25T16:36:56.000+08:00

> 文档ID: 5145 | 来源树: 云存储

---

# 模型列表（POST）

> 模型列表

---

## 接口URL

https://open.ys7.com/api/service/cloud/storage/service/intelligent/list

### **请求方式**

POST

## 请求

请求示例

```
curl --location 'https://open.ys7.com/api/service/cloud/storage/service/intelligent/list' \
--header 'accessToken: at.b9z3v3dgbg6x2q3k0ezfaoce6eoo8v7u' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'cloudType=100422'
```

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| cloudType | string | Y | 云存储类型,由 [获取设备支持的云存储类型](https://open.ys7.com/help/1405)接口获取，需要选择AI套餐；当升级AI时，固定传upgradeInfo |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |
| data | array<object> | data |  |
| -price | int | price |  |
| -userProductPrice | int | userProductPrice |  |
| -intelligentId | string | intelligentId |  |
| -intelligentName | string | intelligentName |  |
| -intelligentType | string | intelligentType |  |
| -intelligentRemark | string | intelligentRemark |  |
| -intelligentDesc | string | intelligentDesc |  |
| -industryType | string | industryType |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "price": 960,//智能体价格 单位 分
            "userProductPrice": 960,//智能体折扣价,单位:分
            "intelligentId": "cloud_common_template_001",
            "intelligentName": "萤石通用云存储模板1",
            "intelligentType": "common",
            "intelligentRemark": "通用云存储模板",
            "intelligentDesc": "https://resource.eziot.com/group1/M00/01/89/CtwQE2frpZSAD2K6AAAH1jc5oSU096.png",
            "industryType": "common"
        }
    ]
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |