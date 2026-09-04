# API-云接入-设备运维-智能设备AI算法管理-设备智能算法下发

> 更新时间: 2026-07-09T13:40:55.000+08:00

> 文档ID: 732 | 来源树: OPEN_API

---

## 设备智能算法下发

- 接口功能

   设备智能算法下发

- 请求地址

`https://open.ys7.com/api/v3/intelligent/model/app/load`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Body | deviceSerial | String | 设备序列号 | Y |
| Body | appId | String | 算法appid | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/intelligent/model/app/load' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'appId=xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| code | Int | 详见code描述 |
| message | String | 详见code描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 2004 | 设备目前不支持动态加载 |  |
| 400 | 该设备算法不存在 |  |
| 500 | 操作失败 |  |