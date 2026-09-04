# API-设备云组件仓-指纹锁-基础功能-分页获取开门记录

> 更新时间: 2026-07-01T18:45:25.000+08:00

> 文档ID: 1353 | 来源树: OPEN_API

---

## 分页获取开门记录

- 接口功能

   该接口用于分页获取指纹锁所在门的开门记录。本节接口只支持萤石联网指纹门锁。子账户token请求所需最小权限：Permission=Get，Resource=dev:序列号。

- 请求地址

`https://open.ys7.com/api/lapp/keylock/open/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 萤石云设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | pageStart | Int | 分页起始页，从0开始 | N |
| Body | pageSize | Int | 分页大小，默认为10，最大为50 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/keylock/open/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734203' \
--data-urlencode 'pageStart=0' \
--data-urlencode 'pageSize=2'
```

- 返回数据

```
{
    "data": [
        {
            "lockUserName": "家人1",
            "openType": 1,
            "openTime": 1457420564508
        },
        {
            "lockUserName": "家人2",
            "openType": 0,
            "openTime": 1457420564508
        }
    ],
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| data | Array | 开门记录列表 |
| data[].lockUserName | String | 用户名 |
| data[].openType | Int | 开锁方式(0-指纹开锁,1-密码开锁,2-卡开锁,3-临时密码,4-人脸,5-室内开门,6-远程开门,7-掌静纹开门,8-机械方式开门) |
| data[].openTime | Long | 开锁时间，时间格式为1457420564508，精确到毫秒 |

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
| 49999 | 数据异常 | 接口调用异常 |