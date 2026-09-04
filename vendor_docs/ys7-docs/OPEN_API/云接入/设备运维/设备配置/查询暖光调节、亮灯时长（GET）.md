# 查询暖光调节、亮灯时长（GET）

> 查询暖光调节、亮灯时长（GET）

> 更新时间: 2026-05-25T16:38:38.000+08:00

> 文档ID: 5061 | 来源树: OPEN_API

---

# 查询暖光调节、亮灯时长（GET）

> 设备键值对查询-根据key获取value
> 是否支持托管：支持，权限为Config

---

## 接口URL

https://open.ys7.com/api/v3/keyValue/{deviceSerial}/{channelNo}/op

## 请求

### query

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 萤石开放API访问令牌 |  |
| key | string | Y | 设备键值对协议-key值：NightVision\_Model |  |

### 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/keyValue/BG9859941/1/op?accessToken=at.0v38go2cdf814p7k3ne8xwvy2codwt1m-1ovws9vkav-18gf1pk-bnadjuikn&key=NightVision_Model'
```

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 返回响应信息 |  |
| -code | int | 返回响应码 |  |
| -message | string | 返回响应信息 |  |
| -moreInfo | string | 更多详细信息 |  |
| data | object | 返回响应数据 |  |
| -valueInfo | string | 设备返回键值对value信息 |  |
| --luminance | int | 暖光调节 |  |
| --duration | int | 亮灯时长 |  |
| --graphicType | int | 0-黑白夜视模式，1-全彩夜视模式，2-智能夜视模式，3-人形检测全彩模式 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "valueInfo": {
            "luminance": 80,
            "duration": 90,
            "graphicType": 0
        }
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
| 200 | 50000 | 服务器异常 |  |
| 200 | 10002 | accessToken过期或异常 |  |
| 200 | 10001 | 无效参数 |  |
| 200 | 20018 | 该用户不拥有该设备 |  |
| 200 | 10031 | 子账号或开发者用户无权限 |  |