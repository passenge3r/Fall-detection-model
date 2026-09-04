# API-存储与媒体处理-云存储-设备升级AI云存储查询

> API-存储与媒体处理-云存储-设备升级AI云存储查询

> 更新时间: 2026-05-25T16:36:55.000+08:00

> 文档ID: 5144 | 来源树: 云存储

---

# 设备升级AI云存储价格查询（POST）

> 设备升级AI云存储价格查询

---

## 接口URL

https://open.ys7.com/api/service/cloud/storage/service/intelligent/upgradeInfo

### **请求方式**

POST

## 请求

请求示例

```
curl --location 'https://open.ys7.com/api/service/cloud/storage/service/intelligent/upgradeInfo' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'localIndex: 1' \
--header 'accessToken: at.b9z3v3dgbg6x2q3k0ezfaoce6eoo8v7u' \
--header 'deviceSerial: 889102086' \
--data-urlencode 'intelligentId=cloud_common_template_001'
```

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |
| deviceSerial | string | Y | 设备序列号 |  |
| localIndex | string | N | 设备通道号，默认1 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| payment | string | N | 付费方式 默认1，1-余额 |  |
| intelligentId | string | Y | 智能体id,由 [AI云存储模型列表](https://open.ys7.com/help/5145)接口获取 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |
| data | object | data |  |
| -deviceSerial | string | deviceSerial |  |
| -localIndex | string | localIndex |  |
| -intelligentName | string | intelligentName |  |
| -intelligencePrice | int | intelligencePrice |  |
| -userIntelligencePrice | int | userIntelligencePrice |  |
| -upgradeIntelligent | int | upgradeIntelligent |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "deviceSerial": "889102086",
        "localIndex": "1",
        "intelligentName": "通用云存储模板1",
"intelligencePrice": 118000, //AI智能云存储服务价格 单位 分
 "userIntelligencePrice": 118000,//用户维度AI智能云存储价格,单位分,
 "upgradeIntelligent": 0,// 支持AI升级,0:不支持，1:支持
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 200 | 10005 | appKey异常 |  |
| 200 | 10013 | 应用没有权限调用此接口 |  |
| 200 | 20002 | 设备不存在 |  |
| 200 | 20007 | 设备不在线 |  |
| 200 | 50000 | 服务器异常 |  |
| 404 | 404 | 资源不存在 |  |
| 200 | 10002 | accessToken过期或异常 |  |
| 200 | 10001 | 无效参数 |  |
| 429 | 429 | 请求过于频繁 |  |