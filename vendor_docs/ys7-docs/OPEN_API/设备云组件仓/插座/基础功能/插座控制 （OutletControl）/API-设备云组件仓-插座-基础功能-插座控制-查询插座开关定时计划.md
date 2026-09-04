# API-设备云组件仓-插座-基础功能-插座控制-查询插座开关定时计划

> 更新时间: 2026-07-06T13:50:45.000+08:00

> 文档ID: 1216 | 来源树: OPEN_API

---

## 查询插座开关定时计划

- 接口功能

   查询插座开关定时计划。本文档仅适用于设备型号 CS-HAE-S60-1WG、CS-HAE-S61-NWG，其它型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Outlet/0/OutletControl/OutletSwitchPlan`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | Content-Type | String | 固定值 application/json | Y |
| header | accessToken | String | 用户访问令牌，获取方式参见 [accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Outlet/0/OutletControl/OutletSwitchPlan' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
  "meta": {
    "code": 200,
    "message": "成功",
    "moreInfo": {
      "deviceMeta": {
        "code": "0x00000000",
        "errorMsg": "Succeeded."
      }
    }
  },
  "data": [
    [
      {
        "weekDays": "",
        "enable": false,
        "name": "",
        "action": [
          [
            {
              "identifier": "",
              "resourceIdentifier": "",
              "domianIdentifier": "",
              "type": "",
              "value": true
            }
          ]
        ],
        "startTime": "",
        "sustain": 149
      }
    ]
  ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Integer | 服务响应状态码，参见返回码解释 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data | Array | 计划列表，取值范围[0,16] |
| data.weekDays | String | 周期，取值范围[1,7] |
| data.enable | Boolean | 使能开关 |
| data.name | String | 计划名称，取值范围[0,256] |
| data.action | Array | 计划操作内容，取值范围[1,256] |
| data.action.identifier | String | 执行动作的identifier，取值范围[0,256] |
| data.action.resourceIdentifier | String | 资源标识符，取值范围[1,256] |
| data.action.domianIdentifier | String | 领域标识符，取值范围[0,256] |
| data.action.type | String | 功能点类型：prop-属性，action-操作，取值范围[prop,action] |
| data.action.value | Boolean | 执行动作的identifier的值（根据具体协议定制，类型） |
| data.startTime | String | 触发时间，取值范围[0,256] |
| data.sustain | Integer | 持续时间，取值范围[0,1440] |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |