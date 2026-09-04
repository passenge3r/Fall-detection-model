# API-设备云组件仓-A3网关-基础功能-删除子设备

> 更新时间: 2026-07-06T17:45:43.000+08:00

> 文档ID: 878 | 来源树: OPEN_API

---

## 删除子设备接口

- 接口功能

   在网关下，解除子设备关联。本节为A3网关相关接口，网关核心功能是管理子设备，适用网关型号：CS-A3-W、CS-ATQ3-W。注：网关下子设备相关接口需用长序列号调用，例：C87654321-C12345678。

- 请求地址

`https://open.ys7.com/api/route/userdevicetob/v3/devices/childDevice/unlink`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Body | deviceSerial | String | 网关序列号 | Y |
| Body | childDevices | Array | 子设备列表（当前只支持删除单个子设备） | Y |
| Body | childDevices.childDeviceSerial | String | 子设备序列号，萤石子设备一般为设备或外包装上的9位序列号 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/route/userdevicetob/v3/devices/childDevice/unlink' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "deviceSerial": "123456789",
    "childDevices": [
        {
            "childDeviceSerial": "987654321"
        }
    ]
}'
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
| 2003 | 设备不在线 |  |
| 2009 | 设备请求响应超时 |  |
| 2030 | 设备不支持批量解除关联 |  |