# API-云接入-设备能力-云台控制-停止云台控制

> 更新时间: 2026-07-09T13:33:42.000+08:00

> 文档ID: 680 | 来源树: OPEN_API

---

## 停止云台控制

- 接口功能

设备停止云台控制 子账户token请求所需最小权限："Permission":"Ptz" "Resource":"Cam:序列号:通道号"。提示：建议停止云台接口带方向参数。

- 请求地址

`https://open.ys7.com/api/lapp/device/ptz/stop`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 通道号 | Y |
| Body | direction | Int | 操作命令：0-上，1-下，2-左，3-右，4-左上，5-左下，6-右上，7-右下，8-放大，9-缩小，10-近焦距，11-远焦距，16-自动控制 | N |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/device/ptz/stop' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.25ne3gkr6fa7coh34ys0fl1h9hryc2kr' \
--data-urlencode 'deviceSerial=568261888' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'direction=1'
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
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 | 检查设备网络状况，稍后再试 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 操作过于频繁，稍后再试 |
| 20014 | deviceSerial不合法 |  |
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60000 | 设备不支持云台控制 |  |
| 60001 | 用户无云台控制权限 |  |
| 60006 | 云台当前操作失败 | 稍候再试 |
| 60009 | 正在调用预置点 |  |
| 60020 | 不支持该命令 | 确认设备是否支持该操作 |