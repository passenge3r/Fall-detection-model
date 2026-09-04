# API-云接入-设备运维-设备配置-设置设备的OSD名称

> 更新时间: 2026-07-09T13:40:33.000+08:00

> 文档ID: 725 | 来源树: OPEN_API

---

## 设置设备的OSD名称

- 接口功能

   该接口用于设置设备osd名称(只用于支持osd设置的设备，需要设备支持能力集：support\_osd=1) 子账户token请求所需最小权限："Permission":"Config" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/device/update/osd/name`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | osdName | String | 需设置的osd内容 | Y |
| Body | channelNo | String | 通道号,默认为1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/update/osd/name' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'osdName=名称' \
--data-urlencode 'channelNo=1'
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
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |