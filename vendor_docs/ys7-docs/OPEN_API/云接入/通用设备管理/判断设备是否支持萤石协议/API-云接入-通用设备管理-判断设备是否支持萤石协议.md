# API-云接入-通用设备管理-判断设备是否支持萤石协议

> 更新时间: 2026-07-09T18:38:57.000+08:00

> 文档ID: 652 | 来源树: OPEN_API

---

## 判断设备是否支持萤石协议

- 接口功能

   根据设备型号以及设备版本号查询设备是否支持萤石协议。 子账户token请求所需最小权限："Permission":"Get" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/lapp/device/support/ezviz`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的 accessToken | Y |
| Body | appKey | String | 用户 appKey | Y |
| Body | model | String | 设备型号 | Y |
| Body | version | String | 设备版本号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/support/ezviz' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
--data-urlencode 'appKey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
--data-urlencode 'model=CS-C1-10F' \
--data-urlencode 'version=V4.1.0 build 130101'
```

- 返回数据

```
{
    "data": [
        {
            "model": "CS-C1-10F",
            "version": "V4.1.0 build 130101",
            "isSupport": 1
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| model | String | 设备型号 |
| version | String | 设备版本号。当 isSupport=0 时返回最近支持的版本；当 isSupport=1 时返回当前版本 |
| isSupport | Int | 是否支持萤石协议。0：不支持；1：支持 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或参数不存在 |
| 10002 | accessToken过期或异常 | accessToken 失效或已过期，请重新获取 |
| 10005 | appKey异常 | appKey 不存在或被冻结 |
| 49999 | 数据异常 | 接口调用异常 |