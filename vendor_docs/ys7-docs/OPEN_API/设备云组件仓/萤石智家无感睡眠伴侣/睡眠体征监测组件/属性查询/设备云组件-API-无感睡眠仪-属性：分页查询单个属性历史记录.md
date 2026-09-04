# 设备云组件-API-无感睡眠仪-属性：分页查询单个属性历史记录

> 更新时间: 2026-06-25T20:32:00.000+08:00

> 文档ID: 1844 | 来源树: OPEN_API

---

## 属性：分页查询单个属性历史记录

- 接口功能

   分页查询单个属性历史记录

- 请求地址

`https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/open/v3/devices/{deviceId}/properties/history`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceId | String | 设备ID | Y |
| query | sortBy | String | 排序规则，不区分大小写，默认不传=不排序。格式：字段名称+空格+升序或降序，如：xxx desc,xxx asc，多个字段用英文逗号隔开，asc=升序，desc=降序 | N |
| query | pageSize | Int | 每一页查询的数量，不传则查询全部 | N |
| query | page | Int | 当前页数，不传则默认为第一页 | N |
| query | startTime | String | 查询创建的开始时间（yyyy-MM-dd HH:mm:ss） | N |
| query | endTime | String | 查询创建的结束时间 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/sleepDetector/v3/third/forward/huayi/open/v3/devices/{deviceId}/properties/history?deviceId=1636656541417369602&page=1&pageSize=20' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "code": 200,
    "message": "success",
    "page": "1",
    "pageSize": "20",
    "total": "0",
    "pageCount": "0",
    "data": [
        {
            "heartRate": 0,
            "createTime": "2023-05-19T11:28:26.184+08:00",
            "state": 1,
            "breathRate": 0,
            "ts": "2023-05-15T04:27:48.897+08:00"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Array<Object> | 具体业务的数据对象 |
| --heartRate | Int | 心率 |
| --createTime | String | 创建时间 |
| --state | Int | 状态 |
| --breathRate | Int | 呼吸率 |
| --ts | String | 时间戳 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 400 | 参数错误 | 请检查请求参数 |