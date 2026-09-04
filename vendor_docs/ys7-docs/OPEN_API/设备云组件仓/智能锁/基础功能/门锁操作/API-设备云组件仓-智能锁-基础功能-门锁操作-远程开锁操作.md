# API-设备云组件仓-智能锁-基础功能-门锁操作-远程开锁操作

> 更新时间: 2026-07-09T13:44:23.000+08:00

> 文档ID: 760 | 来源树: OPEN_API

---

## 远程开锁操作

- 接口功能

   本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁。其余型号不保证可用。注：如下接口调用，需要联系萤石配置白名单，否则接口可能调用报错。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/remote/op`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Body | streamToken | String | 预览流中门锁密钥，[opensdk中获取](https://open.ys7.com/help/4158) | Y |
| Body | endpointId | String | 开门终端 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/remote/op' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'streamToken=xxxxx' \
--data-urlencode 'endpointId=xxxxx'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 返回消息 |
| code | String | 返回码 |
| data | Object | 业务数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 20623 | 远程解锁开关未开启 |  |
| 20007 | 设备不在线 |  |
| 20609 | 设备响应超时 | 门锁通信故障或者电量不足 |
| 20624 | 远程解锁失败 | （1）开锁接口下发过程中又触发了一次远程开锁（连续远程开门请求会报错） （2）Streamtoken 过期，需要及时获取 （3）需要按智能锁上的#号键，如果没有实际这样操作，那么再远程开门，就会返回20624 |