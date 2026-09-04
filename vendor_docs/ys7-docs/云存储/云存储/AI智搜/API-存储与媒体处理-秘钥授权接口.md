# API-存储与媒体处理-秘钥授权接口

> API-存储与媒体处理-秘钥授权接口

> 更新时间: 2026-06-16T17:20:53.000+08:00

> 文档ID: 5146 | 来源树: 云存储

---

## 秘钥授权接口

- 接口功能

   秘钥授权接口

- 请求地址

`https://open.ys7.com/api/service/cloud/storage/service/deviceAuth`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| header | localIndex | String | 设备通道号，默认1 | N |
| body | businessType | Int | 授权业务类型，1：AI云存；2：AI语音云存，默认为1 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloud/storage/service/deviceAuth' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: 889102086' \
--header 'localIndex: 1'
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
| meta | Object | meta信息 |
| meta.code | Int | 状态码 |
| meta.message | String | 状态消息 |
| meta.moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 10005 | appKey异常 | appKey异常 |
| 10013 | 应用没有权限调用此接口 | 应用没有权限调用此接口 |
| 20002 | 设备不存在 | 设备不存在 |
| 20007 | 设备不在线 | 设备不在线 |
| 50000 | 服务器异常 | 服务器异常 |
| 404 | 资源不存在 | 资源不存在 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 10001 | 无效参数 | 无效参数 |
| 429 | 请求过于频繁 | 请求过于频繁 |