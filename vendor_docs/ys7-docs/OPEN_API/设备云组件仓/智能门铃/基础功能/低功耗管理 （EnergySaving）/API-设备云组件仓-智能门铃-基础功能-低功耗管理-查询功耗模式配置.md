# API-设备云组件仓-智能门铃-基础功能-低功耗管理-查询功耗模式配置

> 更新时间: 2026-07-06T17:45:21.000+08:00

> 文档ID: 869 | 来源树: OPEN_API

---

## 查询功耗模式配置

- 接口功能

   该接口用于查询功耗模式配置。本文档仅适用于设备型号 CS-CMT-CHIME-B，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Default/0/EnergySaving/EnergyModeCfg`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/json | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Path | deviceSerial | String | 设备序列号 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Default/0/EnergySaving/EnergyModeCfg' \
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
    "data": {
        "energyMode": "normal"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| meta.moreInfo.deviceMeta.code | String | 设备响应状态码 |
| meta.moreInfo.deviceMeta.errorMsg | String | 设备响应状态描述 |
| data.energyMode | String | 功耗模式，取值范围[perf,saving,super-saving,plan,non-sleep,normal,user]：perf-性能模式，saving-省电模式，super-saving-超级省电模式，plan-计划模式，non-sleep-不休眠模式，normal-常规模式，user-用户模式 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |