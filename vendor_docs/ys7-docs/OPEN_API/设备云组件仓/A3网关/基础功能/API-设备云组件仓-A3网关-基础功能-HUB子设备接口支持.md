# API-设备云组件仓-A3网关-基础功能-HUB子设备接口支持

> 更新时间: 2026-07-06T17:45:59.000+08:00

> 文档ID: 881 | 来源树: OPEN_API

---

## 查询HUB子设备列表

- 接口功能

   该接口用于查询指定HUB设备关联的子设备列表。子账户token请求所需最小权限：`"Permission":"Get"` `"Resource":"dev:序列号"`。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/lapp/hub/device/sub/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | HUB设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/hub/device/sub/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510888'
```

- 返回数据

```
{
    "data": [
        {
            "deviceSerial": "596510888-E38012760",
            "deviceName": null,
            "type": 1,
            "deviceCoverUrl": "https://i.ys7.com/image/CS-T3-A/1.jpeg",
            "deviceType": "CS-T3-A",
            "subDeviceStatusVos": [
                {
                    "channelNo": 0,
                    "key": "DetectorDefencePlan",
                    "value": "1"
                }
            ]
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data.deviceSerial | String | 子设备序列号 |
| data.deviceName | String | 子设备名称 |
| data.type | Int | 子设备类型：1-探测器，2-开关 |
| data.deviceCoverUrl | String | 设备封面(全路径) |
| data.deviceType | String | 设备类型 |
| data.subDeviceStatusVos | Object | 子设备状态 |
| code | String | 返回码 |
| msg | String | 返回信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |

## 获取HUB子设备详细信息

- 接口功能

   该接口用于获取HUB设备的子设备详细信息。子账户token请求所需最小权限：`"Permission":"Get"` `"Resource":"dev:序列号"`。本节为A3网关相关接口，适用网关型号：CS-A3-W、CS-ATQ3-W。

- 请求地址

`https://open.ys7.com/api/lapp/hub/device/sub/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | HUB子设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/hub/device/sub/info' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=596510888-E38012760'
```

- 返回数据

```
{
    "data": {
        "name": null,
        "deviceSerial": "596510888-E38012760",
        "fullSerial": null,
        "deviceType": "CS-HAL-P1-02NWR",
        "deviceCoverUrl": "https://statics.ys7.com/device/image/iDS-2CD9545-BSUC/1.png",
        "devicePicPrefix": "https://statics.ys7.com/device/image/iDS-2CD9545-BSUC/1.png",
        "version": "V4.3.2 build 200508",
        "supportExtShort": "-1|-1|...(设备短能力级，此处省略)",
        "status": 1,
        "userDeviceCreateTime": null,
        "casIp": null,
        "casPort": 0,
        "channelNumber": 0,
        "forceUpgrade": false,
        "category": null,
        "isRelated": 1,
        "ezDeviceCapability": null,
        "customType": null,
        "userId": "",
        "offlineTime": null,
        "isGroupDisable": 1,
        "detectorDefencePlanVo": {
            "enable": 0,
            "plan": null
        }
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data.name | String | 设备名称 |
| data.deviceSerial | String | 设备序列号 |
| data.fullSerial | Int | 设备序列号(全) |
| data.deviceType | String | 设备类型 |
| data.deviceCoverUrl | String | 设备封面(全路径) |
| data.devicePicPrefix | Object | 设备图片前缀 |
| data.version | String | 版本 |
| data.supportExtShort | String | 设备短能力级 |
| data.status | Int | 设备在线状态，0：初始化，1：在线，2：不在线，4：黑名单，5：待机模式(C1S 电池模式) |
| data.userDeviceCreateTime | String | 用户添加设备的时间 |
| data.casIp | String | CAS服务器IP |
| data.casPort | Int | CAS服务器Port |
| data.channelNumber | Int | 设备支持的通道数 |
| data.forceUpgrade | Boolean | 设备是否需要强制升级,默认false |
| data.category | String | 设备类别 |
| data.isRelated | Int | 是否与当前用户有关联,默认1。0:无关联,1:有关联 |
| data.ezDeviceCapability | String | ezDevice能力级,{'sc':'1','v3':'1'}，说明：sc(Single connection)是否支持以设备为单位建立连接，1：支持，0：不支持；v3是否支持p2p的v3版本，1：支持，0：不支持 |
| data.customType | String | 设备自定义类型 |
| data.userId | String | 设备拥有者用户id |
| data.offlineTime | String | 设备离线时间 |
| data.isGroupDisable | Int | 0-支持分组,1-不支持分组 |
| data.detectorDefencePlanVo | Object | 子设备布撤防计划 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |