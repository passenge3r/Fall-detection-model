# API-云接入-设备能力-抓拍-设备抓拍图片

> 更新时间: 2026-07-09T13:39:10.000+08:00

> 文档ID: 687 | 来源树: OPEN_API

---

## 设备抓拍图片

- 接口功能

   接口功能 抓拍设备当前画面，该接口仅适用于IPC或者关联IPC的DVR设备，该接口并非预览时的截图功能。海康型号设备可能不支持萤石协议抓拍功能，使用该接口可能返回不支持或者超时。 注意：该接口需要设备支持能力集：support\_capture=1 设备抓图能力有限，请勿频繁调用，建议每个摄像头调用的间隔4s以上。 子账户token请求所需最小权限："Permission":"Capture" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/device/capture`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 通道号，IPC设备填写1 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/capture' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "data": {
        "picUrl": "https://ezviz-fastdfs-gateway.oss-cn-hangzhou.aliyuncs.com/1/capture/003eyM73IFbVHUM6Ktz7K6JXXLeUbFU.jpg?Expires=1654756106&OSSAccessKeyId=LTAIzI38nEHqg64n&Signature=SEGCPK0ExrKYZBEK3hc6ZZ%252FcPSY%3D"
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 业务数据 |
| picUrl | String | 抓拍后的图片路径，图片保存有效期为2小时 |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 10028 | 抓图接口调用次数超限 | 抓图接口调用次数超限 |
| 10031 | 子账户或萤石用户没有权限 | 子账户或萤石用户没有权限 |
| 10051 | 无权限进行抓图 | 设备不属于当前用户或者未分享给当前用户 |
| 20002 | 设备不存在 | 账号下无此设备 |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁或者设备不支持萤石协议抓拍 |
| 20014 | deviceSerial不合法 | 设备序列号有误 |
| 20032 | 该用户下该通道不存在 | 检查设备是否包含该通道 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 设备抓图未知错误 | 可联系设备研发定位问题 |
| 60017 | 设备抓图失败,2030等 | 可联系设备研发定位问题 |
| 60020 | 不支持该命令 | 确认设备是否支持抓图 |
| 60058 | 设备存在高风险，需求确权 | 设备冻结 |