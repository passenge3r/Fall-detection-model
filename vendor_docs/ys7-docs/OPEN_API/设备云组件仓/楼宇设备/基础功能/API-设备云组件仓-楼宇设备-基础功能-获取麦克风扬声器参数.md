# API-设备云组件仓-楼宇设备-基础功能-获取麦克风扬声器参数

> 更新时间: 2026-07-01T18:44:46.000+08:00

> 文档ID: 1336 | 来源树: OPEN_API

---

## 获取麦克风扬声器参数

- 接口功能

   该接口用于获取楼宇可视对讲设备麦克风扬声器参数。本节为楼宇可视对讲透传相关接口，该接口只支持楼宇相关设备。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/building/device/audio/config/get`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 萤石云设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | msgSeq | String | 唯一标识，建议UUID | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/building/device/audio/config/get' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=427734203' \
--data-urlencode 'msgSeq=c543d24d81914071a7f74769d9c5e2a1'
```

- 返回数据

```
{
    "msgSeq": "c543d24d81914071a7f74769d9c5e2a1",
    "data": {
        "deviceSerial": "427734203",
        "auOut": 3,
        "auIn": 3
    },
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| msgSeq | String | 消息唯一标识，与请求传入的msgSeq对应 |
| data | Object | 麦克风扬声器参数 |
| data.deviceSerial | String | 萤石云设备序列号 |
| data.auOut | Int | 0-10之间的数字，表示扬声器音量大小 |
| data.auIn | Int | 0-10之间的数字，表示麦克风音量大小 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 10011 | 未开通萤石服务 | 设备对应用户未注册至应用下 |
| 20002 | 设备不存在 | 设备序列号输入有误或者设备未被添加或者通道异常 |
| 20007 | 设备不在线 | 检查设备是否在线 |
| 20008 | 设备响应超时 | 稍后重试 |
| 20014 | deviceSerial不合法 | 检查设备序列号是否正确 |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 20500 | 参数不合法 | 检查参数 |
| 20505 | 设备操作失败 | 设备返回其他错误码或者设备响应格式问题 |
| 49999 | 操作异常 | 接口调用异常 |