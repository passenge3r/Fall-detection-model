# API-设备云组件仓-智能锁-基础功能-门锁操作-门锁用户列表

> 更新时间: 2026-07-09T13:45:10.000+08:00

> 文档ID: 769 | 来源树: OPEN_API

---

## 获取智能锁用户列表

- 接口功能

   获取智能锁用户列表

- 请求地址

`https://open.ys7.com/api/lapp/keylock/user/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/user/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": [
        {
            "lockUserIndex": "1",
            "lockUserName": "用户1",
            "lockRemarkName": "123",
            "fingerCount": 0,
            "pwdCount": 1,
            "cardCount": 0,
            "faceCount": 0,
            "volarVeinCount": 0,
            "doubleAuthStatus": 0,
            "antiHijackingPwdCount": 0,
            "antiHijackingFingerCount": 0,
            "expiredEnable": 0,
            "beginTime": -1,
            "endTime": -1,
            "timeQuantums": null,
            "lockType": 0
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 返回响应信息 |
| code | String | 返回响应码 |
| data | Array<object> | 返回响应数据 |
| data[].lockUserIndex | String | 用户编号 |
| data[].lockUserName | String | 用户名 |
| data[].lockRemarkName | String | 用户备注名 |
| data[].fingerCount | Int | 指纹密码数量 |
| data[].pwdCount | Int | 数字密码数量 |
| data[].cardCount | Int | 感应卡密码数量 |
| data[].faceCount | Int | 人脸密码数量 |
| data[].volarVeinCount | Int | 掌静脉密码数量 |
| data[].doubleAuthStatus | Int | 双向认证状态，0-关闭，1-开启 |
| data[].antiHijackingPwdCount | Int | 防挟持密码数量 |
| data[].antiHijackingFingerCount | Int | 防挟持指纹数量 |
| data[].expiredEnable | Int | 有效期，0-永久，1-非永久 |
| data[].beginTime | Int | 开始时间 |
| data[].endTime | Int | 结束时间 |
| data[].timeQuantums | Object | 时间段 |
| data[].lockType | Int | 锁用户类型，0-主用户，1-普通用户 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 |  |
| 20002 | 设备不存在 |  |
| 20014 | 设备序列号不正确 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 |  |
| 10002 | accessToken过期或异常 |  |
| 10001 | 无效参数 |  |
| 20018 | 该用户不拥有该设备 |  |
| 10031 | 子账号或开发者用户无权限 |  |