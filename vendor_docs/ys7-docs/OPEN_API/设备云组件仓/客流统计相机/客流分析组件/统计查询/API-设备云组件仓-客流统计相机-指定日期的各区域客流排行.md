# API-设备云组件仓-客流统计相机-指定日期的各区域客流排行

>  

> 更新时间: 2026-06-30T11:48:52.000+08:00

> 文档ID: 1556 | 来源树: OPEN_API

---

## 指定日期的各区域客流排行

- 接口功能

   对指定日期的各区域客流进行排行

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/ranking/passenger/flow`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | queryDate | String | 日期，格式yyyy-MM-dd | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/ranking/passenger/flow' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'queryDate=2024-01-01'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "1210": "苏州"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |
| data | Object | <key,value>结构，key为客流人数(Integer)，value为区域(String) |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 20015 | 设备不支持该功能 | 请确认设备是否支持该功能 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 404 | 资源不存在 | 请求的资源不存在 |