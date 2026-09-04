# API-设备云组件仓-客流统计相机-客流设备状态统计

>  

> 更新时间: 2026-06-30T11:48:48.000+08:00

> 文档ID: 1554 | 来源树: OPEN_API

---

## 客流设备状态统计

- 接口功能

   对客流的设备状态进行统计

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/region/device/status`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/region/device/status' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "online": 10,
        "offline": 100,
        "work": 5,
        "stop": 100,
        "pause": 5
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |
| data | Object | 响应体信息 |
| data.online | Int | 在线设备数量 |
| data.offline | Int | 离线设备数量 |
| data.work | Int | 工作的设备数，在线并且在统计计划时间内的设备 |
| data.stop | Int | 停止统计的设备数，下线并且不在统计计划时间内的设备 |
| data.pause | Int | 暂停统计的设备数，在线并且不在统计计划时间内的设备，或者下线但是在统计计划时间内的设备 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 20015 | 设备不支持该功能 | 请确认设备是否支持该功能 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 404 | 资源不存在 | 请求的资源不存在 |