# API-设备云组件仓-楼宇设备-基础功能-获取通话状态

> 更新时间: 2026-07-01T18:44:25.000+08:00

> 文档ID: 1327 | 来源树: OPEN_API

---

## 获取通话状态

- 接口功能

   该接口用于获取楼宇可视对讲设备通话状态。本节为楼宇可视对讲透传相关接口，该接口只支持楼宇相关设备。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/building/device/call/status`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | msgSeq | String | 唯一标识，建议UUID | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/building/device/call/status' \
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
        "callStatus": 1,
        "verFlag": 1,
        "callerInfo": {
            "buildingNo": 2,
            "floorNo": 23,
            "zoneNo": 2,
            "unitNo": 2,
            "devNo": 1,
            "devType": 1
        }
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
| data | Object | 通话状态信息 |
| data.deviceSerial | String | 萤石云设备序列号 |
| data.callStatus | Int | 获取通话状态，1-无呼叫、2-响铃、3-正在通话 |
| data.verFlag | String | 1，代表非V1.4.0版本，后续版本再定 |
| data.callerInfo | Object | 主叫信息 |
| data.callerInfo.buildingNo | Long | 楼号 |
| data.callerInfo.floorNo | String | 层号 |
| data.callerInfo.zoneNo | String | 期号 |
| data.callerInfo.unitNo | Int | 单元号 |
| data.callerInfo.devNo | String | 设备编号 |
| data.callerInfo.devType | Int | 设备类型，1-门口机，2-管理机，3-室内机，4-围墙机，5-别墅门口机，6-二次确认机，7-8700客户端，8-4200客户端，9-APP，10-可视门铃，11-VOIP客户端，12-监控点（IPC/NVR/DVR）设备 |

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
| 20500 | 获取数据错误或没有呼叫 | 获取数据错误或没有呼叫 |
| 20505 | 设备操作失败 | 设备返回其他错误码或者设备响应格式问题 |
| 49999 | 操作异常 | 接口调用异常 |