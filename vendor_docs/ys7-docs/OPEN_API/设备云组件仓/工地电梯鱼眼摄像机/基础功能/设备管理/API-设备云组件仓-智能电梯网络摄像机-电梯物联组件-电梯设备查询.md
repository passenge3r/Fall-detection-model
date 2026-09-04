# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-电梯设备查询

> 更新时间: 2026-06-30T11:54:50.000+08:00

> 文档ID: 1614 | 来源树: OPEN_API

---

## 电梯设备查询

- 接口功能

   可以根据设备序列号查询相应电梯设备的信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/query`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/query?deviceSerial=AD2580467' \
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
        "deviceSerial": "AD2580467",
        "deviceName": "安全帽相机",
        "addTime": "2024-01-01 12:00:00",
        "status": 1,
        "offLineTime": "2024-01-01 12:00:00",
        "elevatorSerial": "2dea4ab0051142eea09cd64853b6eb97"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应状态 |
| meta.code | Int | 错误码 |
| meta.message | String | code描述 |
| data | Object | 响应体 |
| data.deviceSerial | String | 设备序列号 |
| data.deviceName | String | 设备名称 |
| data.addTime | String | 绑定时间 |
| data.status | Int | 在线状态，1-在线，0-离线 |
| data.offLineTime | String | 最近下线时间 |
| data.elevatorSerial | String | 关联的电梯id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |