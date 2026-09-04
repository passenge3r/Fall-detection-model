# API-云接入-通用设备管理-设备添加与删除-设备基础信息查询

> 更新时间: 2026-07-09T18:39:00.000+08:00

> 文档ID: 660 | 来源树: OPEN_API

---

## 设备基础信息查询

- 接口功能

   该接口用于查询设备的必要基础信息，可以查询没有关联用户的设备。 注：如果设备已被其他用户添加，则无法查询相关信息。

- 请求地址

`https://open.ys7.com/api/v3/device/searchDeviceInfo`

- 请求方式

`GET、POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 开放平台用户凭证 | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | model | String | 设备型号（默认根据设备序列号查询，如果设备序列号查询不到信息，则根据型号查询） | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/searchDeviceInfo' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'model=xxxxx'
```

- 返回数据

```
{
    "result": {
        "msg": "操作成功",
        "code": "200",
        "data": {
            "displayName": "DS-3E1518P-E-230W(K96719611)",
            "subSerial": "K96719611",
            "fullSerial": "K96719611",
            "model": "DS-3E1500",
            "devType": "DS-3E1500",
            "customType": "DS-3E1518P-E-230W",
            "category": "UNKNOWN",
            "defaultPicPath": "https://statics.ys7.com/device/image/8464/101.jpeg",
            "status": 1,
            "supportWifi": 0,
            "releaseVersion": "1.7.0",
            "version": "V1.0.0 build 221213",
            "availableChannelCount": 1,
            "relatedDeviceCount": 0,
            "supportCloud": "0",
            "supportExt": "{\"support_device_light\":\"1\"}",
            "parentCategory": "COMMON"
        }
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| displayName | String | 设备展示名称，如C1(41956565) |
| subSerial | String | 设备短序列号 |
| fullSerial | String | 设备长序列号 |
| model | String | 设备型号 |
| devType | String | 设备型号 |
| customType | String | 定制型号 |
| category | String | 设备大类型 |
| status | Int | 设备在线状态：1-在线，0-不在线 |
| defaultPicPath | String | 设备图片 |
| supportWifi | Int | 是否支持wifi 0-不支持 1-支持 2-支持带userId的新的wifi配置方式 3-支持smartwifi |
| releaseVersion | String | 设备协议版本 |
| version | String | 设备真实版本号 |
| availableChannelCount | Int | 可用于添加的通道数 |
| relatedDeviceCount | Int | N1，R1，A1等设备关联的设备数 |
| supportCloud | Int | 设备是否支持云存储：0-不支持，1-支持 |
| supportExt | String | 能力级 |
| routerNamePre | String | 路由名称前缀，用于AP配网 |
| routerPasswordPre | String | 路由密码前缀，用于AP配网 |
| createTime | String | 设备首次上线时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 10004 | 用户不存在 |  |
| 20002 | 设备不存在 |  |
| 20013 | 设备已被别人添加 |  |
| 20014 | 设备序列不正确 |  |
| 20020 | 设备在线，被自己添加 |  |
| 20023 | 设备不在线，未被用户添加 |  |
| 20029 | 设备不在线，但是已经被自己添加 |  |
| 60107 | 不支持错误 |  |
| 49999 | 数据异常 |  |