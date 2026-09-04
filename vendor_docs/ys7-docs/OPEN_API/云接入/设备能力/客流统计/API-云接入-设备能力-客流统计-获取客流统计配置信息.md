# API-云接入-设备能力-客流统计-获取客流统计配置信息

> 更新时间: 2026-07-09T13:39:49.000+08:00

> 文档ID: 693 | 来源树: OPEN_API

---

## 获取客流统计配置信息

- 接口功能

   该接口用于获取客流统计配置相关信息（接口需要设备支持客流统计功能） 子账户token请求所需最小权限："Permission":"Get" "Resource":"Cam:序列号:通道号"

- 请求地址

`https://open.ys7.com/api/lapp/passengerflow/config/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 非必选参数，不为空表示获取指定通道客流统计配置信息，为空表示获取设备本身配置信息 | N |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/passengerflow/config/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.dunwhxt2azk02hcn7phqygsybbw0wv6p' \
--data-urlencode 'deviceSerial=427734888'
```

- 返回数据

```
{
    "data": {
        "line": {
            "x1": "0.5000000",
            "y1": "0.0000000",
            "x2": "0.5000000",
            "y2": "1.0000000"
        },
        "direction": {
            "x1": "0.5000000",
            "y1": "0.5000000",
            "x2": "0.2500000",
            "y2": "0.5000000"
        }
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| line | Object | 统计线的两个坐标点，坐标范围为0到1之间的7位浮点数，(0,0)坐标在左上角，格式如{"x1": "0.0","y1": "0.5","x2": "1","y2": "0.5"} |
| direction | Object | 指示方向的两个坐标点，(x1,y1)为起始点，(x2,y2)为结束点格式如{"x1": "0.5","y1": "0.5","x2": "0.5","y2": "0.6"}，与统计线保持垂直 |

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
| 20032 | 该用户下通道不存在 | 该用户下通道不存在 |
| 49999 | 数据异常 | 接口调用异常 |
| 60020 | 不支持该命令 | 设备不支持客流统计功能 |
| 60022 | 已是当前状态 | 已是当前开关状态 |