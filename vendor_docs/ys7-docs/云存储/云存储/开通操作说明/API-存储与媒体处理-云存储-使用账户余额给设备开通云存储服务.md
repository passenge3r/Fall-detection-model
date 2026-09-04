# API-存储与媒体处理-云存储-使用账户余额给设备开通云存储服务

> API-存储与媒体处理-云存储-使用账户余额给设备开通云存储服务

> 更新时间: 2026-06-30T17:54:20.000+08:00

> 文档ID: 1400 | 来源树: 云存储

---

## 使用账户余额/账户资源包余量给设备开通云存储服务

- 接口功能

   该接口用于使用开放平台账户余额、开放平台资源包余量给指定用户的设备开通云存储。该接口目前只支持给开发者账号使用。云存储开通存在延迟，立即开通前建议先调用「获取设备云存储是否开通中」和「获取设备云存储信息」两个接口判断设备是否有云存储服务。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/service/open`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 开通云存储用户的设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | Y |
| body | isImmediately | Int | 是否立即开通：0-否，1-是，默认是0。为0表示不立即开通，当前云存储服务结束后再开始；为1表示立即开通，如果存在云服务且云服务类型一致则在当前云服务上续期，如果不一致直接覆盖。当设备存在延迟生效的云存储时，该参数选择立即开通时，设备的云存储会全部被覆盖，只剩下新开通的云存储。特别说明：对于AI云存和AI语音云存，当为0时也是立即生效，已生效套餐向后延期 | N |
| body | cloudType | String | 云存储类型，payment为1时由「获取设备支持的云存储类型」接口获取；payment为10时由「获取云存储套餐资源包信息」接口获取 | Y |
| body | requestId | String | 请求ID,建议使用UUID，注:相同的请求ID会被认为是同一个请求 | Y |
| body | payment | String | 付费方式，1-余额，10-资源包方式开通，默认是1 | N |
| body | upgradeIntelligentEnable | Int | 是否升级AI云存储，0:不升级，1:升级，新增入参 | N |
| body | deviceAuthEnable | Int | 是否授权设备秘钥托管，0:不授权，1:授权，新增入参，开通AI云存或AI语音云存时，如果设备开启了加密，需要进行授权 | N |
| body | intelligentId | String | 智能体id，由「AI云存储模型列表」接口获取，新增入参 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/service/open' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'isImmediately=0' \
--data-urlencode 'cloudType=400299960' \
--data-urlencode 'requestId=321e364ffc91451f8cd63a5f2521cf1' \
--data-urlencode 'payment=1' \
--data-urlencode 'channelNo=1' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=889278342'
```

- 返回数据

```
{
    "data": {
        "orderId": "open_1_20180929150542808_19924c8789c69a5b"
    },
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Object | 返回数据 |
| orderId | String | 订单ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 10013 | 非开发者账户无权限调用 |  |
| 10052 | 余额不足 |  |
| 10053 | 云存储开通中 | 云存储服务开通有延迟，正在开通后续可以通过「查询设备当前云存储状态」进行判断 |
| 10054 | 云存储操作异常 |  |
| 10060 | 设备不支持的云存储类型 | cloudType错误 |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 |  |
| 20007 | 设备不在线 |  |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |