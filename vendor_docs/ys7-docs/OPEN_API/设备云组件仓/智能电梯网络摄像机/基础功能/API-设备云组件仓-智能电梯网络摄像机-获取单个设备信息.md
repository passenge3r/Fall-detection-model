# API-设备云组件仓-智能电梯网络摄像机-获取单个设备信息

>  

> 更新时间: 2026-06-30T11:47:56.000+08:00

> 文档ID: 1596 | 来源树: OPEN_API

---

# 获取单个设备信息

- 接口功能

查询用户下指定设备的基本信息。针对电梯物联摄像机（DS-2XD8D25E），支持查询：设备序列号、设备名称、设备上报名称、设备型号、在线状态、设备布撤防状态、是否加密、告警声音模式、修改时间、网络类型、设备风险安全等级、设备IP地址 （设备大类、设备二级类目不支持）

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera`

## 电梯设备查询

- 接口功能

电梯业务服务组件，电梯设备查询。

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/query`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 开放平台访问令牌，由萤石开放平台向租户颁发的ak/sk获取 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/query' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 0,
        "message": "string"
    },
    "data": {
        "deviceSerial": "string",
        "deviceName": "string",
        "addTime": "string",
        "status": 0,
        "offLineTime": "string",
        "elevatorSerial": "string"
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
| data.status | Int | 在线状态 1-在线，0-离线 |
| data.offLineTime | String | 最近下线时间 |
| data.elevatorSerial | String | 关联的电梯id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 20018 | 该用户不拥有该设备 | 该用户不拥有该设备 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交"[工单](https://open.ys7.com/console/work.html)"解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |