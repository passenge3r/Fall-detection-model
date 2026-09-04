# API-云接入-设备运维-设备配置-获取镜头遮蔽开关状态

> 更新时间: 2026-07-09T13:40:03.000+08:00

> 文档ID: 706 | 来源树: OPEN_API

---

## 获取镜头遮蔽开关状态

- 接口功能

   该接口用于获取设备镜头遮蔽开关状态（需要设备支持镜头遮蔽功能） 子账户token请求所需最小权限："Permission":"Get" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/device/scene/switch/status`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/scene/switch/status' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx'
```

- 返回数据

```
{
    "data": {
        "deviceSerial": "596510666",
        "channelNo": 1,
        "enable": 1
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Object | 业务数据 |
| deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 |
| channelNo | Int | 通道号 |
| enable | Int | 状态：0-关闭，1-开启 |
| code | String | 返回码 |
| msg | String | 返回消息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持镜头遮蔽功能 |