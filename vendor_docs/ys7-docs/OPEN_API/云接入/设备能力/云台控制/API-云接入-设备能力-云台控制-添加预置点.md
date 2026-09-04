# API-云接入-设备能力-云台控制-添加预置点

> 更新时间: 2026-07-09T13:33:54.000+08:00

> 文档ID: 682 | 来源树: OPEN_API

---

## 添加预置点

- 接口功能

   支持云台控制操作的设备添加预置点，该接口需要设备支持能力集：ptz\_preset=1 子账户token请求所需最小权限："Permission":"Ptz" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/device/preset/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 通道号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/preset/add' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "data": {
        "index": 3
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 业务数据 |
| index | Int | 预置点序号，C6设备是1-12，该参数需要开发者自行保存 |
| code | String | 返回码 |
| msg | String | 返回消息 |

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
| 60007 | 预置点个数超过最大值 |  |
| 60008 | C6预置点个数达到上限，无法添加 | C6预置点最大限制个数为12 |