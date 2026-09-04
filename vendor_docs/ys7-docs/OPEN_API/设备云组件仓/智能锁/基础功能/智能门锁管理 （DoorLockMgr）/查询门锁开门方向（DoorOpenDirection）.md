# 查询门锁开门方向（DoorOpenDirection）

> 更新时间: 2026-06-17T18:11:24.000+08:00

> 文档ID: 4049 | 来源树: OPEN_API

---

## 查询门锁开门方向（DoorOpenDirection）

- 接口功能

   开门方向查询接口，适配Z5000FVS系列设备，支持托管和子账号，权限类型为设备级的GET

- 请求地址

`https://open.ys7.com/api/v3/device/otap/prop`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| header | accessToken | string | 用户访问令牌 | Y |
| query | deviceSerial | string | 设备序列号 | Y |
| query | localIndex | string | 资源序号 | Y |
| query | resourceCategory | string | 资源种类，描述资源的类型 | Y |
| query | domainIdentifier | string | 功能点领域，填写报备时的属性所在领域 | Y |
| query | propIdentifier | string | 功能点标识，填写报备时的属性标识符 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/otap/prop?deviceSerial=value&localIndex=value&resourceCategory=value&domainIdentifier=value&propIdentifier=value' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "direction": "left"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| meta | object | 响应信息 |
| -code | int | 响应码 |
| -message | string | 响应码说明 |
| -moreInfo | object | 更多信息 |
| data | object | 设备响应信息 |
| -direction | String | 开门方向,left-左,right-右 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10031 | 账号无权限访问此设备 |  |
| 20007 | 设备不在线 |  |
| 20018 | 该用户不拥有该设备 |  |