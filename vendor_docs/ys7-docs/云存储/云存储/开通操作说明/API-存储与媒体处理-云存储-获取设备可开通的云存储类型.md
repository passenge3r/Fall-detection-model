# API-存储与媒体处理-云存储-获取设备可开通的云存储类型

> 更新时间: 2026-07-06T17:46:07.000+08:00

> 文档ID: 1405 | 来源树: 云存储

---

## 获取设备可开通的云存储类型

- 接口功能

该接口用于获取设备可以开通的云存储类型，以及对应的价格。

- 请求地址

`https://open.ys7.com/api/lapp/cloud/storage/device/support`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | deviceSerial | String | 设备序列号，存在英文字母的设备序列号，字母需为大写 | Y |
| Body | channelNo | Int | 非必选参数，不为空表示操作指定通道云存储，为空表示操作设备本身云存储，默认是1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/cloud/storage/device/support' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'deviceSerial=889326928' \
--data-urlencode 'channelNo=1'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": [
        {
            "cloudProductName": "7天循环月套餐", // 云存储套餐名称
            "cloudType": "400299958", // 云存储类型
            "serviceTime": 1, // 云存储 服务时长
            "serviceTimeUnit": 3, // 云存储 服务时间单位 1:天 2:周 3:月 4 年
            "storageTime": 7, // 云存储 存储时长
            "storageTimeUnit": 1, // 云存储 存储时间单位 1:天 2:周 3:月 4 年
            "price": 1200, // 云存储服务价格 单位 分
            "userProductPrice": 1100, // 云存储服务折扣价,单位分
            "cloudProductType": "事件云存储" // 云存储套餐类型，事件云存储,连续云存储,AI云存储
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| cloudProductName | String | 云存储套餐名称 |
| cloudType | String | 云存储类型 |
| serviceTime | Int | 云存储 服务时长 |
| serviceTimeUnit | Int | 云存储 服务时间单位 1:天 2:周 3:月 4 年 |
| storageTime | Int | 云存储 存储时长 |
| storageTimeUnit | Int | 云存储 存储时间单位 1:天 2:周 3:月 4 年 |
| price | Int | 云存储服务价格 单位 分 |
| productStatus | Int | 云存储套餐状态 1:启用 0:停用 |
| userProductPrice | Int | 云存储服务折扣价 单位 分 |
| cloudProductType | String | 云存储套餐类型，事件云存储,连续云存储,AI云存储 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 10013 | 非开发者账户无权限调用 | 非开发者账户无权限调用 |
| 10054 | 云存储操作异常 | 云存储操作异常 |
| 20002 | 设备不存在 | 设备不存在 |
| 20006 | 网络异常 | 网络异常 |
| 20007 | 设备不在线 | 设备不在线 |
| 20008 | 设备响应超时 | 设备网络不佳，稍候请重试 |
| 20014 | deviceSerial不合法 | deviceSerial不合法 |
| 20018 | 该用户不拥有该设备 | 用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |