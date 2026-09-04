# API-云接入-通用设备管理-设备信息查询-分页查询设备列表

> 更新时间: 2026-07-09T18:39:30.000+08:00

> 文档ID: 673 | 来源树: OPEN_API

---

## 分页查询设备列表

- 接口功能

   分页查询设备列表。起始页从0开始，不超过400页；每页默认查询数默认为10，不超过50。 支持子账号查询。可分页查询出授权给子账号的设备，最小授权权限"Permission":"Get" "Resource":"dev:序列号" 不支持查询托管设备

- 请求地址

`https://open.ys7.com/api/lapp/device/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 萤石开放API访问令牌 | Y |
| Body | pageStart | Integer | 分页页码，起始页从0开始，不超过400页 | N |
| Body | pageSize | Integer | 分页大小，默认为10，不超过50 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/device/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'pageStart=0' \
--data-urlencode 'pageSize=10'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": [
        {
            "id": "004368108f1444459901a063969a6c03",
            "deviceSerial": "33010343992967895520:33011062991327187933",
            "deviceName": "33010343992967895520:33011062991327187933",
            "deviceType": "33010343992967895520",
            "status": 0,
            "defence": 0,
            "deviceVersion": "V1.0.0 build 200811",
            "addTime": 1693806032741,
            "updateTime": 1693806032741,
            "parentCategory": "COMMON",
            "riskLevel": 0,
            "netAddress": null
        }
    ],
    "page": {
        "total": 416,
        "size": 1,
        "page": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| msg | String | 响应提示说明 |
| code | String | 响应结果状态码 |
| data | Array<object> | 设备列表 |
| id | String | 条目索引 |
| deviceSerial | String | 设备序列号 |
| deviceName | String | 设备名称 |
| deviceType | String | 设备型号 |
| status | Int | 设备在线状态，1-在线；0-离线 |
| defence | Int | 布撤防状态 |
| deviceVersion | String | 固件版本号 |
| addTime | Long | 用户添加时间 |
| updateTime | Long | 设备最后更新时间 |
| parentCategory | String | 设备二级类目名称 |
| riskLevel | Int | 设备风险安全等级，0-安全；大于0，有风险，风险越高，值越大 |
| netAddress | String | 设备IP地址 |
| page | Object | 分页信息 |
| total | Int | 数据总数 |
| size | Int | 分页大小 |
| page | Int | 分页页码 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 | appKey被冻结 |
| 49999 | 数据异常 | 接口调用异常 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10001 | 无效参数 | 参数为空或格式不正确 |