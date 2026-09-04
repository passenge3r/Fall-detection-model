# MT2开合反转

> 更新时间: 2026-06-23T17:34:07.000+08:00

> 文档ID: 2818 | 来源树: OPEN_API

---

## MT2开合反转

- 接口功能

   窗帘开合反转，即正转变为反转、反转变为正转的过程。触发开合反转时，窗帘开合的百分比会发生反转，例如窗帘当前开百分比为42，反转后开百分比会变成58。支持托管及子账号，设备级，校验权限为Config。

- 请求地址

`https://open.ys7.com/api/v3/device/otap/action`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 萤石开放API访问令牌 | Y |
| Header | Content-Type | String | application/json | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 资源序号，描述资源类型下的序号 | Y |
| Header | resourceCategory | String | 资源种类，描述资源的类型，固定值：Curtain | Y |
| Header | domainIdentifier | String | 功能点领域，填写报备时的属性所在领域，固定值：CurtainCtrl | Y |
| Header | actionIdentifier | String | 功能点标识，填写报备时的操作标识符，固定值：OpeningClosingReverse | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/device/otap/action' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--header 'deviceSerial: {deviceSerial}' \
--header 'localIndex: 0' \
--header 'resourceCategory: Curtain' \
--header 'domainIdentifier: CurtainCtrl' \
--header 'actionIdentifier: OpeningClosingReverse'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": null,
        "moreInfo": {
            "deviceMeta": {
                "code": "0",
                "errorMsg": null
            }
        }
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，参见返回码说明 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Object | 无业务应答 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 10001 | 参数错误 | 参数错误 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 10031 | 账号无权限访问此设备 | 子账户或萤石用户没有权限 |
| 20007 | 设备不在线 | 设备不在线 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |
| 70018 | 资源不存在 | 资源不存在 |
| 50000 | 服务异常 | 服务异常 |