# API-存储与媒体处理-云存储-使用卡密给设备开通云存储服务

> API-存储与媒体处理-云存储-使用卡密给设备开通云存储服务

> 更新时间: 2026-06-30T17:54:22.000+08:00

> 文档ID: 1402 | 来源树: 云存储

---

## 使用卡密给设备开通云存储

- 接口功能

   该接口用于使用萤石云存储卡密给设备开通云存储功能。子账户token请求所需最小权限：Permission:Config Resource:dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/open`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 开通云存储用户的设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | cardPassword | String | 云存储卡卡密 | Y |
| body | phone | String | 开通云存储用户的手机号，非必选参数，为空表示为当前用户开通云存储 | N |
| body | channelNo | Int | 非必选参数，不为空表示给指定通道开通云存储，为空表示给设备本身开通云存储，默认是1 | N |
| body | isImmediately | Int | 是否立即开通：0-否，1-是，默认是0。为0表示不立即开通，当前云存储服务结束后再开始；为1表示立即开通，会覆盖当前云存储服务 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/open' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510666' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'phone=18888888888' \
--data-urlencode 'cardPassword=4326717075050976' \
--data-urlencode 'isImmediately=0'
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
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | phone对应用户不拥有该设备 |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60012 | 未知错误 | 设备返回其他错误码或操作异常 |
| 60020 | 设备不支持云存储 | 设备不支持云存储或设备当前版本不支持云存储，升级后可支持 |
| 60030 | 卡密输入错误次数过多，24小时后再输入 | 卡密输入错误次数超过限制次数 |
| 60031 | 卡密信息不存在 | 确认输入的卡密是否正确 |
| 60032 | 卡密状态错误 | 卡密未激活或已使用或已过期 |
| 60033 | 卡密非卖品，只能开通对应的绑定设备 | 非卖品类型卡密 |
| 60035 | 开通云存储服务失败 | 出现此错误码或者"开通云存储参数错误"的提示请及时发送手机号、设备序列号、卡密密码等信息到open-team@ezvizlife.com |