# API-云接入-通用设备管理-设备信息查询-获取国标License列表

> 更新时间: 2026-07-09T18:38:34.000+08:00

> 文档ID: 671 | 来源树: OPEN_API

---

## 获取国标License列表

- 接口功能

   国标license查询。

- 请求地址

`https://open.ys7.com/api/v3/device/register/gb/license/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 访问令牌 | Y |
| Body | productKey | String | 项目编码 | Y |
| Body | pageIndex | Integer | 起始页，默认0 | N |
| Body | pageSize | Integer | 分页大小，默认10，最大50 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/register/gb/license/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'productKey=xxxxx' \
--data-urlencode 'pageIndex=0' \
--data-urlencode 'pageSize=10'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "idType": "1",
            "createTime": "1621415553000",
            "activatedTime": null,
            "devlogicId": "1394944048989024256",
            "reserve": null,
            "productKey": "33011064992527738959",
            "deviceName": "33011000991117704014",
            "deviceId": "33011064992527738959:33011000991117704014",
            "deviceLicense": "hgWQFujE971St6bwERg1ii",
            "activatedStatus": "0",
            "disableStatus": "-1"
        },
        {
            "idType": "1",
            "createTime": "1621415455000",
            "activatedTime": null,
            "devlogicId": "1394943640660946944",
            "reserve": null,
            "productKey": "33011064992527738959",
            "deviceName": "33011004991117602380",
            "deviceId": "33011064992527738959:33011004991117602380",
            "deviceLicense": "Px819NfJa51Y95Wwgw77kf",
            "activatedStatus": "0",
            "disableStatus": "-1"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回元信息 |
| code | Int | 返回码 |
| message | String | 返回消息 |
| moreInfo | Object | 更多信息 |
| data | Array<object> | 国标License列表 |
| idType | String | ID类型 |
| createTime | String | 创建时间 |
| activatedTime | String | 激活时间 |
| devlogicId | String | 设备逻辑ID |
| reserve | String | 保留字段 |
| productKey | String | 项目编码 |
| deviceName | String | 设备名称 |
| deviceId | String | 设备ID |
| deviceLicense | String | 设备License |
| activatedStatus | String | 激活状态 |
| disableStatus | String | 禁用状态 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |