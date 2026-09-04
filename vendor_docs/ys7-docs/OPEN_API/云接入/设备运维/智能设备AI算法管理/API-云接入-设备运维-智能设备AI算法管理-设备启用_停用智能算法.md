# API-云接入-设备运维-智能设备AI算法管理-设备启用/停用智能算法

> 更新时间: 2026-07-09T13:41:54.000+08:00

> 文档ID: 733 | 来源树: OPEN_API

---

## 设备启用/停用智能算法

- 接口功能

   设备启用/停用智能算法，如果需要卸载算法，需要先停用算法，若设备内存不足会自动卸载已停用算法

- 请求地址

`https://open.ys7.com/api/v3/intelligent/model/device/onoffline`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | appId | String | 设备上的应用ID | Y |
| Body | status | String | 0：停用,1：启用 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/v3/intelligent/model/device/onoffline' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'appId=xxxxx' \
--data-urlencode 'status=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| moreInfo | String | 附加信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 参数错误 |  |
| 500 | 服务异常 |  |