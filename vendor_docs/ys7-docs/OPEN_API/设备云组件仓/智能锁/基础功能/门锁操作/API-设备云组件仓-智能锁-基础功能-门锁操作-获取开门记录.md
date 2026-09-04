# API-设备云组件仓-智能锁-基础功能-门锁操作-获取开门记录

> 更新时间: 2026-07-09T13:45:13.000+08:00

> 文档ID: 771 | 来源树: OPEN_API

---

## 获取开门记录

- 接口功能

   本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁。其余型号不保证可用。 注：如下接口调用，需要联系萤石配置白名单，否则接口可能调用报错

- 请求地址

`https://open.ys7.com/api/lapp/keylock/open/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 用户访问令牌 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | pageStart | String | 分页起始页0开始 | Y |
| Body | pageSize | String | 分页大小，小于200 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/keylock/open/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'pageStart=xxxxx' \
--data-urlencode 'pageSize=xxxxx'
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
| msg | String | 返回消息 |
| code | String | 返回码 |
| data | Object | 业务数据 |
| lockUserName | String | 用户名 |
| openType | String | 开锁方式(0-指纹开锁,1-密码开锁,2-卡开锁,3-临时密码,4-人脸,5-室内开门,6-远程开门,7-掌静纹开门,8-机械方式开门) |
| openTime | String | 开锁时间,时间格式为1457420564508,精确到毫秒 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |