# API-设备云组件仓-门禁-基础功能-查询指定设备上的删除进展

> 更新时间: 2026-07-06T13:47:48.000+08:00

> 文档ID: 1117 | 来源树: OPEN_API

---

## 查询指定设备上的删除进展

- 接口功能

   该接口用于查询指定设备上的删除进展。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/query/device/delete/process`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Query | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/company/member/query/device/delete/process?deviceSerial=' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
"code": "200",
"msg": "操作成功"
data:{
"status":"",
"percent":
}
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| status | String | 状态 processing#处理中,success#成功,failed#失败 |
| percent | Integer | 进度值, range:[0,100] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |