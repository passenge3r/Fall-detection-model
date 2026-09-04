# API-设备云组件仓-智能温控器-显示屏-设置屏幕待机时长

> 更新时间: 2026-07-06T13:49:14.000+08:00

> 文档ID: 1167 | 来源树: OPEN_API

---

## 设置屏幕待机时长

- 接口功能

   设置屏幕待机时长。本文档仅适用于设备型号 CS-HAE-PH3-NWG，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/DisplayScreen/ScreenStandbyTime`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |
| body | time | Integer | 单位s，当 enabled 字段为 true 这个时间才有意义，取值范围[0,300] | N |
| body | enabled | Boolean | true 待机，false 一直亮着 | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/global/0/DisplayScreen/ScreenStandbyTime' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx' \
--data-raw '{
    "time": 12,
    "enabled": true
}'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "成功",
    "moreInfo": {
      "deviceMeta": {
        "code": "0x00000000",
        "errorMsg": "Succeeded."
      }
    }
  }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，参见返回码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |