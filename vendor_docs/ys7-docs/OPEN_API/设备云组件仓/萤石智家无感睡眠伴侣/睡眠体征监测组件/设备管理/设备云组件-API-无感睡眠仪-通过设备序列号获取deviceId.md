# 设备云组件-API-无感睡眠仪-通过设备序列号获取deviceId

> 更新时间: 2026-06-25T20:32:06.000+08:00

> 文档ID: 1846 | 来源树: OPEN_API

---

## 通过设备序列号获取deviceId

- 接口功能

   通过设备序列号（MHR202-230000002）获取deviceId（1636656541417369602）

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/huayi/deviceId`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceCode | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/huayi/deviceId?deviceCode=MHR202-230000002' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "data": "1636656541417369602",
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
| data | String | 设备ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |