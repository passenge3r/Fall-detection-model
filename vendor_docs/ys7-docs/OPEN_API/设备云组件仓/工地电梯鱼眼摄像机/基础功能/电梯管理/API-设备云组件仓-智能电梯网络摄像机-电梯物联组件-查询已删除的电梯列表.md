# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-查询已删除的电梯列表

> 更新时间: 2026-06-30T11:55:12.000+08:00

> 文档ID: 1620 | 来源树: OPEN_API

---

## 查询已删除的电梯列表

- 接口功能

   分页查询当前已经删除的电梯列表

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/info/query/delete`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | size | Int | 分页大小，每一页响应多少条记录，size最大不超50，超过50按50处理 | Y |
| query | startTime | String | 查询的开始时间，与电梯信息创建时间对比，查询创建时间大于开始时间的电梯列表，格式：2023-04-18 12:00:00 | Y |
| query | endTime | String | 查询的结束时间，与电梯信息创建时间对比，查询创建时间小于结束时间的电梯列表，格式：2023-04-18 12:00:00 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/info/query/delete?size=10&startTime=2023-04-18 12:00:00&endTime=2024-04-18 12:00:00' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": [
        {
            "elevatorSerial": "5da2a656f2a946b8a759496b0572b599",
            "deviceSerial": null,
            "customSerial": "123",
            "elevatorNum": "12",
            "buildingNum": "12",
            "address": "海威市",
            "worksiteId": "f2412cec91c4461a9f64fdc6b618e105",
            "elevatorType": "freight",
            "productModel": "VT-120",
            "productDate": "2022-01-10 00:00:00",
            "propertyName": "绿城集团",
            "propertyPhone": "95061877",
            "maintEnterprise": "绿城",
            "maintName": "王琳",
            "maintPhone": "12345678",
            "maintCycle": 1,
            "useEnterprise": "融侨",
            "useStauts": "using",
            "createTime": "2024-01-01 12:00:00",
            "modifyTime": "2024-01-01 12:00:00",
            "elevatorPersonsLimit": 21,
            "elevatorLoadLimit": 21,
            "status": 1
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应状态信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Array | 响应体信息 |
| data[].elevatorSerial | String | 电梯唯一编号 |
| data[].deviceSerial | String | 电梯绑定设备序列号 |
| data[].customSerial | String | 电梯自定义唯一标识 |
| data[].elevatorNum | String | 电梯在物业编号 |
| data[].buildingNum | String | 电梯所在建筑物编号，开发者自定义 |
| data[].worksiteId | String | 关联区域id |
| data[].address | String | 详细地址 |
| data[].elevatorType | String | 电梯类型：passenger-乘客电梯，freight-载货电梯，escalator-自动扶梯，fire-消防员电梯，villa-别墅电梯 |
| data[].productModel | String | 电梯型号，厂家生产型号信息 |
| data[].productDate | String | 电梯出厂日期 |
| data[].propertyName | String | 电梯所属物业联系人员姓名 |
| data[].maintEnterprise | String | 电梯所属维保单位 |
| data[].maintName | String | 维保人姓名 |
| data[].maintPhone | String | 维保人手机号 |
| data[].maintCycle | Int | 维保周期，取值范围(0,90) |
| data[].useEnterprise | String | 电梯使用单位 |
| data[].useStauts | String | 电梯状态：using-在用，scrapped-报废，disabled-停用，logout-注销 |
| data[].createTime | String | 电梯首次录入系统时间 |
| data[].modifyTime | String | 电梯最近一次信息更新时间 |
| data[].status | Int | 电梯绑定设备在线状态：0-不在线，1-在线 |
| data[].propertyPhone | String | 电梯所属物业联系人员手机号 |
| data[].elevatorPersonsLimit | Int | 电梯载人上限(人) |
| data[].elevatorLoadLimit | Int | 电梯载重上限(kg) |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |