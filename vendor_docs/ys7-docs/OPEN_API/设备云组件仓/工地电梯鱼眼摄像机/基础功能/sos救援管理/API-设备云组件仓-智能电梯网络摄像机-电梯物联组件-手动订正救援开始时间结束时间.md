# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-手动订正救援开始时间结束时间

> 更新时间: 2026-06-30T11:55:38.000+08:00

> 文档ID: 1632 | 来源树: OPEN_API

---

## 救援时间更新

- 接口功能

   救援开始时间与结束时间会产生实际计算偏差，用于修正救援开始时间与结束时间

- 请求地址

`https://open.ys7.com/api/devicekit/elevator/sos/rescuetime/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | eventId | String | 事件id | Y |
| body | startTime | String | 救援开始时间，格式yyyy-MM-dd HH:mm:ss | Y |
| body | endTime | String | 救援结束时间，格式yyyy-MM-dd HH:mm:ss | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/devicekit/elevator/sos/rescuetime/update' \
--header 'accessToken: at.xxxxx' \
--header 'eventId: evt001' \
--header 'Content-Type: application/json' \
--data-raw '{
    "startTime": "2024-01-01 12:02:00",
    "endTime": "2024-01-01 12:09:00"
}'
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
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |