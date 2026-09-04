# OPEN API-萤石用户连接-设备托管-获取授权信息-获取设备托管列表

> 更新时间: 2026-07-09T13:46:41.000+08:00

> 文档ID: 824 | 来源树: OPEN_API

---

## 查询托管设备列表

- 接口功能

   查询当前账号下的托管设备列表，支持分页查询。

- 请求地址

`https://open.ys7.com/api/lapp/trust/device/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | version | String | 接口版本，固定填写3.0 | Y |
| Body | pageStart | String | 分页起始页，默认为0 | Y |
| Body | pageSize | String | 每页数量，默认10，最大50 | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/lapp/trust/device/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'pageStart=0' \
--data-urlencode 'pageSize=50' \
--data-urlencode 'version=3.0'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": [
        {
            "deviceSerial": "889336636",
            "deviceName": "DS-7816NB-K2(889336636)",
            "cameraName": "视频6@DS-7816NB-K2(889336636)",
            "channelNo": 1,
            "customName": "",
            "deviceTrustId": "18d1840cdbfa40e3aad2f5d4e528245c",
            "status": -1,
            "isAdd": 1
        }
    ],
    "page": {
        "total": 452,
        "size": 20,
        "page": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回消息 |
| data | Array | 托管设备列表 |
| data[].deviceSerial | String | 设备序列号 |
| data[].deviceName | String | 设备名称 |
| data[].cameraName | String | 通道名称 |
| data[].channelNo | Int | 通道号 |
| data[].customName | String | C端用户自定义设备信息 |
| data[].deviceTrustId | String | 设备授权Id，用来标识授权用户 |
| data[].status | Int | 在线状态：0表示不在线，1表示在线 |
| data[].isAdd | Int | 显示状态：0表示隐藏，1表示显示 |
| page | Object | 分页信息 |
| page.total | Int | 总记录数 |
| page.size | Int | 每页数量 |
| page.page | Int | 当前页码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10002 | accessToken过期或异常 | 请重新获取accessToken |
| 10004 | 用户不存在 | 检查accessToken对应的用户是否存在 |
| 10005 | client\_id异常 | 检查应用的appKey是否正确 |
| 10031 | 账号无权限访问此设备 | 确认账号是否有设备的访问权限 |
| 49999 | 数据异常 | 请检查请求参数是否正确 |