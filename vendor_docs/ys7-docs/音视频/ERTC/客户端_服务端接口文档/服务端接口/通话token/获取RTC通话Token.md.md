# 获取RTC通话Token.md

>  

> 更新时间: 2026-06-11T14:50:27.000+08:00

> 文档ID: 4938 | 来源树: 音视频

---

## 获取RTC通话Token

- 接口功能

   获取RTC通话Token，用于建立实时音视频通话

- 请求地址

`https://open.ys7.com/api/service/media/token/rtc`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | expireTime | String | Token过期时间，单位秒 | Y |
| body | appId | String | ERTC应用Id | Y |
| body | params | Object | 扩展参数对象，包含strRoomId和customId | Y |
| body | params.strRoomId | String | ERTC房间号 | Y |
| body | params.customId | String | 自定义用户ID | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/media/token/rtc' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'expireTime=3600' \
--data-urlencode 'appId=xxxxx' \
--data-urlencode 'params={"strRoomId":"12345","customId":"user001"}'
```

- 返回数据

```
{
    "data": {
        "token": "tk.xxxxx"
    },
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta.code | Int | 业务码，200表示成功 |
| meta.message | String | 响应信息 |
| meta.moreInfo | Object | 更多信息 |
| data.token | String | RTC通话Token |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数是否正确 |
| 10002 | accessToken过期或异常 | 请重新获取accessToken |
| 400 | 参数错误 | 请检查请求参数格式 |