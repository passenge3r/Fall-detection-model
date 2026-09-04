# API-设备云组件仓-客流统计相机-更新客流统计模板

>  

> 更新时间: 2026-06-30T11:48:45.000+08:00

> 文档ID: 1552 | 来源树: OPEN_API

---

## 更新客流统计模板

- 接口功能

   对已拥有的客流统计模板进行更改

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/template/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | regionTag | String | 绑定区域，最多32字符 | Y |
| body | dayOfWeek | String | 布防周期，1-星期一，2-星期二，...，7-星期日，多个用逗号隔开，示例：1,2,3,4,5,6,7 | Y |
| body | alarmThreshold | String | 告警短信发送的客流阈值，达到阈值后会发送短信给用户在运营中心配置的余额信息接收人 | Y |
| body | startCountingTime | String | 开始统计时间，格式HH:mm:ss | Y |
| body | endCountingTime | String | 结束统计时间，格式HH:mm:ss | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/peoplecounting/template/update' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'regionTag=region01' \
--data-urlencode 'dayOfWeek=1,2,3,4,5,6,7' \
--data-urlencode 'alarmThreshold=1000' \
--data-urlencode 'startCountingTime=08:00:00' \
--data-urlencode 'endCountingTime=22:00:00'
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
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 20015 | 设备不支持该功能 | 请确认设备是否支持该功能 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 404 | 资源不存在 | 请求的资源不存在 |