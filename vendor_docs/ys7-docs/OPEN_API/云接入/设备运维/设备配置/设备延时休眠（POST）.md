# 设备延时休眠（POST）

> 设备延时休眠（POST）

> 更新时间: 2026-05-25T16:38:40.000+08:00

> 文档ID: 5202 | 来源树: OPEN_API

---

# 设备延时休眠（POST）

> 设备延时休眠
> 设备级config权限，支持托管和子账号

---

## 接口URL

https://open.ys7.com/api/v3/device/sleep/delay

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| deviceSerial | string | Y | 设备序列号 |  |
| channelNo | int | N | 设备通道号，默认为0 |  |
| type | string | Y | 业务操作类型,1:预览 |  |

### 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/sleep/delay' \
--header 'accessToken: at.3dhvhznwc4rrdo5rc56da8n1beme4a95-67y1zmrxp0-1baj0gc-0tq5i4ux1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=BG9859941' \
--data-urlencode 'channelNo=0' \
--data-urlencode 'type=1'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": {}
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 400 | 10001 | 参数错误 |  |
| 403 | 10031 | 账号无权限访问此设备 |  |
| 412 | 20007 | 设备不在线 |  |
| 404 | 20002 | 设备不存在 |  |
| 422 | 20011 | 设备不支持或者设备异常 |  |
| 408 | 20008 | 设备响应超时 |  |
| 408 | 20006 | 网络异常 |  |