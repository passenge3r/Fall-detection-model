# API-设备云组件仓-指纹锁-基础功能-获取指纹锁用户列表

> 更新时间: 2026-07-01T18:45:12.000+08:00

> 文档ID: 1352 | 来源树: OPEN_API

---

## 获取指纹锁用户列表

- 接口功能

   该接口用于获取指纹锁上注册的用户列表。本节接口只支持萤石联网指纹门锁，[购买门锁](https://www.ys7.com/item/2056.html)。子账户token请求所需最小权限：Permission=Get，Resource=dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/user/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/user/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734203'
```

- 返回数据

```
{
    "data": [
        {
            "lockUserIndex": "27",
            "lockUserName": "阿姨",
            "lockUserType": "0",
            "fingerCount": 10,
            "pwdCount": 0,
            "cardCount": 0,
            "expiredEnable": 0,
            "beginTime": 1457420564508,
            "endTime": 1457420564508,
            "lockType": 1
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| data | Array | 指纹锁用户列表 |
| data[].lockUserIndex | Int | 唯一索引ID |
| data[].lockUserName | String | 用户名 |
| data[].lockUserType | Int | 锁用户类型(0:主用户,1:非主用户) |
| data[].fingerCount | Int | 开锁指纹数量 |
| data[].pwdCount | Int | 开锁数字密码数量 |
| data[].cardCount | Int | 开锁卡数量 |
| data[].expiredEnable | Int | 0为永久有效，1为非永久 |
| data[].beginTime | Long | 账户有效期开始时间，时间格式为1457420564508，精确到毫秒 |
| data[].endTime | Long | 账户有效期结束时间，时间格式为1457420564508，精确到毫秒 |
| data[].lockType | Int | 锁类型 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 | 设备序列号输入有误或者设备未被添加 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20014 | deviceSerial不合法 | 检查设备序列号是否正确 |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 20609 | 设备响应超时，门锁通信故障或者电量不足，请重试 | 稍后重试 |
| 49999 | 数据异常 | 接口调用异常 |