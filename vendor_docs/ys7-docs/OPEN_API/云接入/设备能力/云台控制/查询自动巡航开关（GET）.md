# 查询自动巡航开关（GET）

> 查询自动巡航开关（GET）

> 更新时间: 2026-05-25T16:38:12.000+08:00

> 文档ID: 5063 | 来源树: OPEN_API

---

# 查询自动巡航开关（GET）

> 查询自动巡航开关

---

## 接口URL

https://open.ys7.com/api/v3/device/ptz/cruise/auto/switch

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 用户令牌 |  |
| deviceSerial | string | Y | 设备序列号 |  |
| localIndex | string | Y | 资源号 |  |

### 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/ptz/cruise/auto/switch' \
--header 'accessToken: at.0v38go2cdf814p7k3ne8xwvy2codwt1m-1ovws9vkav-18gf1pk-bnadjuikn' \
--header 'deviceSerial: BF7513110' \
--header 'localIndex: 1'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 返回信息 |  |
| -code | string | 错误码 |  |
| -message | string | 错误信息 |  |
| -moreInfo | object | moreInfo |  |
| data | object | 返回体 |  |
| -enable | boolean | false关，true开 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "enable": false
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |