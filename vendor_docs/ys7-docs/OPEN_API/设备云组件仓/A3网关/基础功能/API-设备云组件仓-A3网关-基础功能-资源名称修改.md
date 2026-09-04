# API-设备云组件仓-A3网关-基础功能-资源名称修改

> 更新时间: 2026-07-06T17:46:04.000+08:00

> 文档ID: 884 | 来源树: OPEN_API

---

## 资源名称修改接口

- 接口功能

   资源名称修改接口。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/route/userdevicetob/v3/devices/resources/rename`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 资源编号，从资源列表中获取 | Y |
| Header | resourceCategory | String | 资源类型，从资源列表中获取 | N |
| Body | name | String | 修改后的资源名称 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/route/userdevicetob/v3/devices/resources/rename' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: 0' \
--header 'localIndex: 2' \
--header 'resourceCategory: Switch' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=5'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "string",
        "moreInfo": {}
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | OK | 请求成功 |
| 400 | 参数错误 |  |
| 403 | 用户无权限操作 |  |