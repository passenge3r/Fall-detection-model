# API-存储与媒体处理-云录制-图片采集与存储-开通设备OTAP图片存储

> 更新时间: 2026-06-30T17:52:37.000+08:00

> 文档ID: 1386 | 来源树: 云存储

---

## 开通设备OTAP图片存储

- 接口功能

   开通用户云存储能力，并创建默认项目。

- 请求地址

`https://open.ys7.com/api/v3/open/cloud/permit/user`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 用户令牌 | Y |
| Body | openDesc | String | 项目名称，长度不能超过256个字符，仅允许输入大小写字母和数字，不允许特殊字符 | Y |
| Body | expireDays | Int | 过期时间，单位天，输入范围是7~36135，输入不在范围内视为无效请求；不填默认为7，0代表永久 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/open/cloud/permit/user' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'openDesc=myProject' \
--data-urlencode 'expireDays=7'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务器异常 | 请检查传递参数进行重试，如还是服务错误请联系客服 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |