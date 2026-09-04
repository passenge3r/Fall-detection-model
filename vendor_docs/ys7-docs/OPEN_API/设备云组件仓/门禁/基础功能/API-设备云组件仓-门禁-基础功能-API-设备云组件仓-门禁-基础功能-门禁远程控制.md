# API-设备云组件仓-门禁-基础功能-API-设备云组件仓-门禁-基础功能-门禁远程控制

> 更新时间: 2026-07-06T13:48:00.000+08:00

> 文档ID: 1121 | 来源树: OPEN_API

---

## 门禁远程控制

- 接口功能

   该接口用于门禁远程控制，支持子账号的Config权限。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/acs/remote/door`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Body | cmd | String | 控制命令:open-开门,close-关门(受控),alwaysOpen-常开(自由),alwaysClose-常关(禁用) | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | doorNumber | Integer | 门禁设备下门的编号(65535代表所有门，默认所有门)，门禁一体机一般一个门禁一个门 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/acs/remote/door' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'cmd=' \
--data-urlencode 'deviceSerial=' \
--data-urlencode 'doorNumber='
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |