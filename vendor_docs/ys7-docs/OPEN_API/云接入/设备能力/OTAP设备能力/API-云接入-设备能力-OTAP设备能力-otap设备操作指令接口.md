# API-云接入-设备能力-OTAP设备能力-otap设备操作指令接口

>  

> 更新时间: 2026-06-30T10:58:22.000+08:00

> 文档ID: 1514 | 来源树: OPEN_API

---

## OTAP设备操作指令接口

- 接口功能

   OTAP设备操作。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/action`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 资源序号 | Y |
| header | resourceCategory | String | 资源种类，描述资源的类型 | Y |
| header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域 | Y |
| header | actionIdentifier | String | 功能点标识，填写报备时的操作标识符 | Y |
| header | Content-Type | String | 请设置为application/json | Y |
| body | Body | String | JSON结构，格式参见操作报备时的示例报文 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/action' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: L46493049' \
--header 'resourceCategory: global' \
--header 'localIndex: 0' \
--header 'domainIdentifier: TimeMgr' \
--header 'actionIdentifier: TimeZone' \
--header 'Content-Type: application/json' \
--data-raw '{"timeZone":"CST-8:00:00"}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "Succeeded.",
        "moreInfo": {
            "deviceMeta": {
                "code": "0x00000000",
                "errorMsg": "Succeeded."
            }
        }
    },
    "data": {}
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 更多响应信息 |
| meta.moreInfo.deviceMeta | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备错误信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10031 | 子账户或萤石用户没有权限 | 无权限操作 |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |