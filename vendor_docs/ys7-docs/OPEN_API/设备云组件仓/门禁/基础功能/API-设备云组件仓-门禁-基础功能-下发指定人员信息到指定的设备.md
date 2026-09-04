# API-设备云组件仓-门禁-基础功能-下发指定人员信息到指定的设备

> 更新时间: 2026-07-06T13:47:38.000+08:00

> 文档ID: 1111 | 来源树: OPEN_API

---

## 下发指定人员信息到指定的设备

- 接口功能

   该接口用于下发指定人员信息到指定的设备上，需要先补充人员基础信息和人员扩展信息。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/info/send`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Body | empNo | String | 人员工号 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | doorNo | Integer | 授予的门权限:两位以下数字表示的门编号，多个以,分隔,默认为1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/company/member/info/send' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'empNo=' \
--data-urlencode 'deviceSerial=' \
--data-urlencode 'doorNo=1'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| data | Null | 返回数据 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |