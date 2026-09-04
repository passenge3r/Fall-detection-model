# API-设备云组件仓-A3网关-基础功能-子设备下资源列表

> 更新时间: 2026-07-06T17:46:01.000+08:00

> 文档ID: 883 | 来源树: OPEN_API

---

## 获取指定设备的资源列表接口

- 接口功能

   获取指定设备的资源列表及资源基本信息。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/route/userdevicetob/v3/devices/resources/{deviceSerial}`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Path | deviceSerial | String | 指定的设备 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/route/userdevicetob/v3/devices/resources/{deviceSerial}' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "string"
    },
    "data": [
        {
            "resourceId": "a3fd0c3e6cdc449fae764251c35esdfg",
            "deviceSerial": "C12345678",
            "resourceCategory": "video",
            "localIndex": "1",
            "name": "视频1",
            "isShared": 0,
            "permission": -1,
            "resourceidentifier": "videoIdentifier",
            "deviceCategory": "IPC",
            "category": "C6C",
            "deviceType": "CS-C6C-S"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| data | Array | 子设备列表 |
| data.resourceId | String | 资源ID（数据库标识） |
| data.deviceSerial | String | 设备序列号（资源全局标识） |
| data.resourceCategory | String | 资源类型（功能描述） |
| data.localIndex | String | 资源局部标识 |
| data.name | String | 资源名称（设备名称、通道名称、子设备名称、按键名称等） |
| data.isShared | Integer | 是否共享，0:未分享，1:共享所有者，2:共享用户，3:所有者已结束，4:分享邀请不在时间段内，5:二维码扫描关注者 |
| data.permission | Integer | 权限 |
| data.resourceIdeatifier | String | 资源描述标识 |
| data.deviceCategory | String | 一级类目 |
| data.category | String | 二级类目 |
| data.deviceType | String | 设备型号（PID） |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | OK | 请求成功 |
| 400 | 参数错误 |  |
| 500 | 服务器异常 |  |