# API-存储与媒体处理-云存储-获取设备云存储是否开通中

> API-存储与媒体处理-云存储-获取设备云存储是否开通中

> 更新时间: 2026-06-30T17:54:48.000+08:00

> 文档ID: 1410 | 来源树: 云存储

---

## 获取设备云存储是否开通中

- 接口功能

   该接口用于获取设备云存储是否正在开通中。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/service/open/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/service/open/info' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=LL0000001' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "data": {
        "isOpening": 0
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| isOpening | Int | 是否有开通中的云存储，0-否，1-是 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 10013 | 非开发者账户无权限调用 |  |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 |  |
| 20007 | 设备不在线 |  |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |