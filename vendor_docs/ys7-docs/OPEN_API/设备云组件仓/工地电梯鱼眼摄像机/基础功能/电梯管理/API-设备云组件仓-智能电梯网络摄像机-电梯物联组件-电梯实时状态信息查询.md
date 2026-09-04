# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-电梯实时状态信息查询

> 更新时间: 2026-06-30T11:54:38.000+08:00

> 文档ID: 1612 | 来源树: OPEN_API

---

## 电梯实时状态信息查询

- 接口功能

   向电梯绑定的设备下发状态查询指令，查询实时检测到的电梯状态

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/status/get`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | elevatorSerial | String | 电梯唯一标识，电梯列表查询接口响应的elevatorSerial | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/status/get?elevatorSerial=2dea4ab0051142eea09cd64853b6eb97' \
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
        "temperature": {
            "value": 25,
            "tag": "celsius"
        },
        "speed": 0,
        "direction": "static",
        "acceleration": {
            "forwardBackwardAcceleration": 0,
            "leftRightAcceleration": 0,
            "upDownAcceleration": 0
        },
        "floor": 1,
        "customFloorName": "1",
        "alarmButtonStat": 0,
        "doorStatType": 1,
        "doorStat": 0,
        "personStatType": 1,
        "personStat": 2,
        "personNum": 0,
        "levelingStat": 0,
        "maintenanceStatus": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Object | 响应体 |
| data.temperature | Object | 电梯温度 |
| data.temperature.value | Float | 温度值 |
| data.temperature.tag | String | 温度单位，枚举：celsius-摄氏度，fahrenheit-华氏度 |
| data.speed | Float | 运行速度 |
| data.direction | String | 运行方向，枚举：up-上，down-下，static-静止 |
| data.acceleration | Object | 加速度 |
| data.acceleration.forwardBackwardAcceleration | Float | 左右加速度，取值范围[0,99999] |
| data.acceleration.leftRightAcceleration | Float | 前后加速度，取值范围[0,99999] |
| data.acceleration.upDownAcceleration | Float | 上下加速度，取值范围[0,99999] |
| data.floor | Int | 楼层 |
| data.customFloorName | String | 楼层名称 |
| data.alarmButtonStat | Int | 报警按钮状态，枚举：0-未启用，1-已启用，2-报警中 |
| data.doorStatType | Int | 电梯门状态检测类型，枚举：0-传感器，1-智能分析 |
| data.doorStat | Int | 电梯门状态，枚举：0-未启用，1-开门，2-关门 |
| data.personStatType | Int | 梯内人员状态检测类型，枚举：0-传感器，1-智能分析 |
| data.personStat | Int | 梯内人员状态，枚举：0-未启用，1-有人，2-无人 |
| data.personNum | Int | 梯内人员数量，取值范围[0,1000] |
| data.levelingStat | Int | 平层状态，枚举：0-未启用，1-平层，2-非平层，3-冲顶，4-蹲底，5-正常 |
| data.maintenanceStatus | Int | 维保状态，枚举：0-正常，1-维保中 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |