# API-设备云组件仓-客流统计相机-客流统计模板下发设备

>  

> 更新时间: 2026-06-30T11:48:46.000+08:00

> 文档ID: 1553 | 来源树: OPEN_API

---

## 客流统计模板下发设备

- 接口功能

   根据输入的设备序列号，将客流统计模板下发至设备

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/issue`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | regionTag | String | 绑定区域 | Y |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/peoplecounting/issue' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'regionTag=region01'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "online": 0,
        "offline": 0,
        "work": 0,
        "stop": 0,
        "pause": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |
| data | Object | 设备状态统计信息 |
| data.online | Int | 在线设备数量 |
| data.offline | Int | 离线设备数量 |
| data.work | Int | 工作的设备数，在线并且在统计计划时间内的设备数 |
| data.stop | Int | 停止统计的设备数，下线并且不在统计计划时间内的设备数 |
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