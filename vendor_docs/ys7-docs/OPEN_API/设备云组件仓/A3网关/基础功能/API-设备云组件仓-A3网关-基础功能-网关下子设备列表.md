# API-设备云组件仓-A3网关-基础功能-网关下子设备列表

> 更新时间: 2026-07-06T17:45:45.000+08:00

> 文档ID: 879 | 来源树: OPEN_API

---

## 网关下子设备列表接口

- 接口功能

   获取网关下子设备列表。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/route/userdevicetob/v3/devices/childDevice/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Header | deviceSerial | String | 网关序列号 | Y |
| Query | currentPage | Int | 当前页，默认从0开始 | N |
| Query | pageSize | Int | 分页大小，默认为10 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/route/userdevicetob/v3/devices/childDevice/list' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: C87654321'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "string"
    },
    "data": [
        {
            "subDeviceSerial": "C87654321-C12345678",
            "childDeviceSerial": "C12345678",
            "name": "开关",
            "deviceCategory": "Switch",
            "category": "SW1C",
            "childDeviceType": "CS-HAL-SW1C-03NWG",
            "version": "V1.0.0 build 190316"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| data | Array | 子设备列表 |
| data.deviceSerial | String | 子设备关联后在平台的设备唯一标识 |
| data.childDeviceSerial | String | 子设备序列号，同关联时的子设备序列号 |
| data.name | String | 子设备名称 |
| data.deviceCategory | String | 子设备一级类目 |
| data.category | String | 子设备二级类目 |
| data.childDeviceType | Integer | 子设备型号 |
| data.version | Integer | 子设备版本号 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | OK | 请求成功 |
| 400 | 参数错误 |  |
| 403 | 用户无权限操作 |  |