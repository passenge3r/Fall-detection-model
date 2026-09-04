# API-设备云组件仓-客流统计相机-添加客流统计模板

>  

> 更新时间: 2026-06-30T11:48:34.000+08:00

> 文档ID: 1548 | 来源树: OPEN_API

---

## 添加客流统计模板

- 接口功能

   可定义客流统计模板（定义布防周期、绑定区域、告警阈值、开始、结束统计时间）并进行添加。

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/template/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| body | regionTag | String | 绑定区域，最多32字符 | Y |
| body | dayOfWeek | String | 布防周期，1-星期一，2-星期二，……，7-星期日，多个用逗号隔开，示例：1,2,3,4,5,6,7 | Y |
| body | alarmThreshold | String | 告警短信发送的客流阈值，达到阈值后会发送短信给用户在运营中心配置的余额信息接收人 | Y |
| body | startCountingTime | String | 开始统计时间，格式-HH:mm:ss | Y |
| body | endCountingTime | String | 结束统计时间，格式-HH:mm:ss | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/peoplecounting/template/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"regionTag":"region01","dayOfWeek":"1,2,3,4,5,6,7","alarmThreshold":"100","startCountingTime":"08:00:00","endCountingTime":"20:00:00"}'
```

- 返回数据

```
{
    "meta": {
        "code": 0,
        "message": "string"
    },
    "data": {
        "templateId": "string"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |
| data | Object | 模板信息 |
| data.templateId | String | 模板id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 20015 | 设备不支持该功能 | 设备不支持该功能 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |