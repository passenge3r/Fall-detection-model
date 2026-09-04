# 设备云组件-API-无感睡眠仪-属性：查询设备属性最新数据

> 更新时间: 2026-06-25T20:32:01.000+08:00

> 文档ID: 1845 | 来源树: OPEN_API

---

## 属性：查询设备属性最新数据

- 接口功能

   查询设备属性最新数据

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/open/v3/devices/{deviceId}/properties/latest`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | date | String | 查询日期 | Y |
| query | deviceId | String | 设备ID | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/open/v3/devices/{deviceId}/properties/latest?date=2023-05-20&deviceId=1636656541417369602' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "data": {}
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | Int | 请求结果，200=成功 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |