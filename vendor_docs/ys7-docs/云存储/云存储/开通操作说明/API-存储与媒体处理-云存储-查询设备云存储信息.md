# API-存储与媒体处理-云存储-查询设备云存储信息

> API-存储与媒体处理-云存储-查询设备云存储信息

> 更新时间: 2026-06-30T17:54:26.000+08:00

> 文档ID: 1404 | 来源树: 云存储

---

## 查询设备云存储信息

- 接口功能

   该接口用于查询设备当前的云存储信息。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/v2/storage/device/info`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | application/x-www-form-urlencoded | Y |
| body | accessToken | String | 授权过程获取的access\_token | Y |
| body | deviceSerial | String | 设备序列号,存在英文字母的设备序列号，字母需为大写 | Y |
| body | channelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/v2/storage/device/info' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=BB94809' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": [
        {
            "deviceSerial": "J70807475",
            "totalDays": 7,
            "userEnable": 1,
            "serviceType": "3",
            "expireTime": 1836827148000,
            "serviceTime": 12,
            "serviceTimeUnit": 3,
            "storageTime": 7,
            "storageTimeUnit": 1,
            "isContinueCloud": 0,
            "cloudProductName": "7天循环智能AI事件存储1年套餐",
            "intelligentName": "通用AI智能云存储模板",
            "intelligentId": "cloud_common_template_001",
            "upgradeIntelligent": 0,
            "currentAiCapacity": [
                12
            ],
            "storageMode": 0,
            "supportServiceCodes": [
                1
            ],
            "cloudStorageServiceRespList": [
                {
                    "businessOrderId": "open_1_20260317220511892_66846e5ae8f01b1",
                    "serviceTime": 12,
                    "serviceTimeUnit": 3,
                    "storageTime": 7,
                    "storageTimeUnit": 1,
                    "productPayType": 1,
                    "effectTime": 1773756012000,
                    "expireTime": 1805292312000,
                    "status": 2,
                    "userActiveStatus": 1,
                    "effectImmediately": 1,
                    "cloudProductType": 2,
                    "cloudProductName": "7天循环智能AI事件存储1年套餐",
                    "isContinueCloud": 0,
                    "aiCapacity": 12
                }
            ]
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回消息 |
| data | Array | 返回数据列表 |
| deviceSerial | String | 设备序列号 |
| totalDays | Int | 存储时长 |
| userEnable | Int | 当前云存储服务状态 1:开启 0:暂停 |
| serviceType | Int | 服务类型 |
| expireTime | Long | 过期时间,时间戳 |
| serviceTime | Int | 当前云存储的服务时长 |
| serviceTimeUnit | Int | 当前云存储的服务时间单位 1:天 2:周 3:月 4:年 |
| storageTime | Int | 当前云存储的存储时长 |
| storageTimeUnit | Int | 当前云存储的存储时间单位 1:天 2:周 3:月 4:年 |
| isContinueCloud | Int | 是否是连续云存储 1:是,0:不是 |
| cloudProductName | String | 云存储套餐名称 |
| intelligentName | String | 智能体名称,AI云存储新增 |
| intelligentId | String | 智能体id,AI云存储新增 |
| upgradeIntelligent | Int | 是否支持AI升级,0:不支持，1:支持,AI云存储新增 |
| storageMode | Int | 支持的存储模式 -1:不支持, 0:推流云存储, 1:拉流云存储 |
| supportServiceCodes | Array | 支持录像类型：是否支持连续云存储，storageMode为0且supportServiceCodes包含2；或 storageMode为1且supportServiceCodes包含8 |
| cloudStorageServiceRespList | Array | 云存储服务对象，包含所有可用的云存储 |
| businessOrderId | String | 订单号 |
| productPayType | Int | 产品付费类型 1:付费 2:试用 3:其他 |
| effectTime | Long | 生效时间,时间戳 |
| status | Int | 云存储状态 1:待使用 2:使用中 3:已使用 |
| userActiveStatus | Int | 用户激活状态 1:激活状态 2:暂停状态 |
| effectImmediately | Int | 服务是否立即生效 1:立即生效 2:延迟生效 |
| cloudProductType | Int | 云存储产品类型 2:云存储套餐 |
| aiCapacity | Int | AI能力容量 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 10013 | 非开发者账户无权限调用 |  |
| 20002 | 设备不存在 |  |
| 20006 | 网络异常 |  |
| 20007 | 设备不在线 |  |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |