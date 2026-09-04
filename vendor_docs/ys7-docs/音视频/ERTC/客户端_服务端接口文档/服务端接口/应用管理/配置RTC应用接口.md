# 配置RTC应用接口

> 更新时间: 2026-06-25T16:19:25.000+08:00

> 文档ID: 1895 | 来源树: 音视频

---

## 配置RTC应用接口

- 接口功能

   该接口用于配置RTC项目。当参数appid为空时，将创建一个项目，并且返回appId。当参数不为空时，将修改该项目。

- 请求地址

`https://open.ys7.com/api/v3/rtc/project`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | bizTypes | String | 业务类型：1-实时音视频，2-远程控制，3-多屏互动，4-视频客服。可多值，用西文逗号分隔。示例：'1,2' | N |
| Body | appId | String | RTC应用ID，当参数appid为空时，将创建一个项目，并且返回appId。当参数不为空时，将修改该项目。 | N |
| Body | name | String | 项目名 | Y |
| Body | intro | String | 项目介绍 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/rtc/project' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'bizTypes=1,2' \
--data-urlencode 'name=myProject' \
--data-urlencode 'intro=myIntro'
```

- 返回数据

```
{
    "data": {
        "appId": "65b6c37b4adf43f3aa753e60910b9f27"
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
| data | Object | 响应结果，appId为空时返回 |
| -appId | String | RTC应用ID |
| meta | Object | 响应元信息 |
| -code | String | 响应码 |
| -message | String | 响应信息 |
| -moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 49999 | 数据异常 | 数据异常 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 400 | 参数错误 | 参数错误 |