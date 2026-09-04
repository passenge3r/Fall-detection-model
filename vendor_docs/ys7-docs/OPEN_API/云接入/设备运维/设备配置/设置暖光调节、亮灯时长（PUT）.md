# 设置暖光调节、亮灯时长（PUT）

> 设置暖光调节、亮灯时长（PUT）

> 更新时间: 2026-05-25T16:38:39.000+08:00

> 文档ID: 5062 | 来源树: OPEN_API

---

# 设置暖光调节、亮灯时长（PUT）

> 统一设置键值对
> 是否支持托管及子账号：支持，权限为Config

---

## 接口URL

https://open.ys7.com/api/v3/keyValue/{deviceSerial}/{channelNo}/op

## 请求

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |
| key | string | Y | 设备键值对协议，key值：NightVision\_Model |  |
| value | string | Y | 设备键值对协议，value值，可通过Get /api/v3/keyValue/{deviceSerial}/{channelNo}/op接口获取每类key的value格式；{"luminance":100,"duration":100,"graphicType":0}；luminance：暖光调节；duration：亮灯时长; graphicType：0-黑白夜视模式，1-全彩夜视模式，2-智能夜视模式，3-人形检测全彩模式 |  |

### 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/keyValue/BG9859941/1/op?accessToken=at.47g4c0k4aokhhyg02lwnsvcud7ci7o5m-2kses2xtgo-0fzuqbp-tdddnlrp5' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'key=NightVision_Model' \
--data-urlencode 'value={"luminance":80,"duration":90,"graphicType":0}'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 返回响应结果 |  |
| -code | int | 返回响应码 |  |
| -message | string | 返回响应信息 |  |
| -moreInfo | string | 更多详细信息 |  |
| data | object | 返回响应数据 |  |
| -result | string | 键值对设置结果 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "result": "OK"
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 200 | 20002 | 设备不存在 |  |
| 200 | 20007 | 设备不在线 |  |
| 200 | 20008 | 设备响应超时 |  |
| 200 | 10002 | accessToken过期或异常 |  |
| 200 | 10001 | 无效参数 |  |
| 200 | 20018 | 该用户不拥有该设备 |  |