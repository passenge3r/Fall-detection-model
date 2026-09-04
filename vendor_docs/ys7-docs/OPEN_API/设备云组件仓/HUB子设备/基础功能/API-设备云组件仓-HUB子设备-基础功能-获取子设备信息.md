# API-设备云组件仓-HUB子设备-基础功能-获取子设备信息

> API-设备云组件仓-HUB子设备-基础功能-获取子设备信息

> 更新时间: 2026-05-25T16:42:36.000+08:00

> 文档ID: 1357 | 来源树: OPEN_API

---

## 获取子设备信息

- 接口功能

该接口用于获取HUB设备的子设备详细信息

- 请求地址

  `https://open.ys7.com/api/lapp/hub/device/sub/info`
- 请求方式

  `POST`
- 子账户token请求所需最小权限

  `"Permission":"Get"` `"Resource":"dev:序列号"`
- 请求参数

| 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- |
| accessToken | String | 授权过程获取的access\_token | Y |
| deviceSerial | String | HUB子设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |

- HTTP请求报文

```
POST /api/lapp/hub/device/sub/info HTTP/1.1
Host: open.ys7.com
Content-Type: application/x-www-form-urlencoded

accessToken=at.9mqitppidgce4y8n54ranvyqc9fjtsrl&deviceSerial=596510888-E38012760
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
        "supportExtShort": "-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|0|0|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|0|0|5|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|1|-1|-1|-1|1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|-1|",
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
| name | String | 设备名称 |
| deviceSerial | String | 设备序列号 |
| fullSerial | int | 设备序列号(全) |
| deviceType | String | 设备类型 |
| deviceCoverUrl | String | 设备封面(全路径 |
| devicePicPrefix | Object | 设备图片前缀 |
| version | String | 版本 |
| supportExtShort | String | 设备短能力级 |
| status | int | 设备在线状态，0：初始化，1：在线，2：不在线，4：黑名单，5：待机模式(C1S 电池模式) |
| userDeviceCreateTime | String | 用户添加设备的时间 |
| casIp | String | CAS服务器IP |
| casPort | int | CAS服务器Port |
| channelNumber | int | 设备支持的通道数 |
| forceUpgrade | boolean | 设备是否需要强制升级,默认false |
| category | String | 设备类别 |
| isRelated | int | 是否与当前用户有关联,默认1.0:无关联,1:有关联 |
| ezDeviceCapability | String | ezDevice能力级,{'sc':'1','v3':'1'},说明,sc(Single connection) : 是否支持以设备为单位建立连接，1：支持，0：不支持；v3:是否支持p2p的v3版本，1：支持，0：不支持 |
| customType | String | 设备自定义类型 |
| userId | String | 设备拥有者用户id |
| offlineTime | String | 设备离线时间 |
| isGroupDisable | int | 0-支持分组,1-不支持分组 |
| detectorDefencePlanVo | Object | 子设备布撤防计划 |

##### 子设备布撤防计划：

| 字段名 | 类型 | 描述 |
|:--|:--|
|enable |int |开关状态 0-关闭 1-开启|
|plan|String|布撤防计划|

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
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |