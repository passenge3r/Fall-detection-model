# API-存储与媒体处理-云存储-开启或关闭设备云存储

> API-存储与媒体处理-云存储-开启或关闭设备云存储

> 更新时间: 2026-06-30T17:54:24.000+08:00

> 文档ID: 1403 | 来源树: 云存储

---

## 开启和暂停设备云存储

- 接口功能

   该接口用于开启和暂停设备云存储（非取消云存储套餐，只是暂停设备上传录像）。子账户token请求所需最小权限：Permission:Config Resource:Cam:序列号:通道号。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/enable`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 开通云存储用户的设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | enable | Int | 开启或暂停云存储：0-暂停，1-开启 | Y |
| body | phone | String | 开通云存储用户的手机号，非必选参数，为空表示为当前用户开通云存储 | N |
| body | channelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/enable' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510666' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'phone=18888888888' \
--data-urlencode 'enable=1'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 |  |
| 20007 | 设备不在线 |  |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | phone对应用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 未知错误 | 设备返回其他错误码或操作异常 |