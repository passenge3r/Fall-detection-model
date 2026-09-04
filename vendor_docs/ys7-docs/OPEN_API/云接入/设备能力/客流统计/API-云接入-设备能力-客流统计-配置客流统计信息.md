# API-云接入-设备能力-客流统计-配置客流统计信息

> 更新时间: 2026-07-09T13:39:47.000+08:00

> 文档ID: 692 | 来源树: OPEN_API

---

## 配置客流统计信息

- 接口功能

   该接口用于配置客流统计相关信息（接口需要设备支持客流统计功能） 子账户token请求所需最小权限："Permission":"Config" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/passengerflow/config/set`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | line | String | 统计线的两个坐标点，坐标范围为0到1之间的7位浮点数，(0,0)坐标在左上角，格式如{"x1": "0.0","y1": "0.5","x2": "1","y2": "0.5"} | Y |
| Body | direction | Int | 指示方向的两个坐标点，(x1,y1)为起始点，(x2,y2)为结束点格式如{"x1": "0.5","y1": "0.5","x2": "0.5","y2": "0.6"}，最好与统计线保持垂直 | Y |
| Body | channelNo | Int | 非必选参数，不为空表示配置指定通道客流统计信息，为空表示配置设备本身信息 | N |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/passengerflow/config/set' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.dunwhxt2azk02hcn7phqygsybbw0wv6p' \
--data-urlencode 'deviceSerial=427734888' \
--data-urlencode 'line=%7B%22x1%22%3A+%220.0%22%2C%22y1%22%3A+%220.5%22%2C%22x2%22%3A+%220.5%22%2C%22y2%22%3A+%220.5%22%7D' \
--data-urlencode 'direction=%7B%22x1%22%3A+%220.5%22%2C%22y1%22%3A+%220.5%22%2C%22x2%22%3A+%220.5%22%2C%22y2%22%3A+%220.6%22%7D'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持客流统计功能 |
| 60022 | 已是当前状态 | 已是当前开关状态 |
| 60025 | 客流统计配置失败 | 设备返回其他错误码 |