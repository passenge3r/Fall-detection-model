# API-设备云组件仓-智能锁-基础功能-智能门锁控制-查询人脸解锁计划

> 更新时间: 2026-07-09T13:45:19.000+08:00

> 文档ID: 776 | 来源树: OPEN_API

---

## 查询人脸解锁计划

- 接口功能

   该接口用于查询人脸解锁计划，包含 触发时间、持续时间、使用开关等参数。 注：本文档仅适用于设备型号：CS-DL30-V100、CS-Y3000F-V100等系列智能门锁，其余型号不保证可用。 该接口不支持托管。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/DoorLockCtrl/FaceUnlockPlan`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/Video/1/DoorLockCtrl/FaceUnlockPlan' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": "{\"plan\":[{\"startTime\":\"07:00\",\"repeatPeriod\":[1,6],\"sustain\":960,\"enabled\":true,\"action\":[]},{\"startTime\":\"08:00\",\"repeatPeriod\":[2,3,4,5],\"sustain\":780,\"enabled\":true,\"action\":[]}]}"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码。参见响应码解释。 |
| meta.message | String | 服务响应状态描述 |
| meta.moreInfo | Object | 设备响应信息 |
| data | Object | 业务参数 |
| data.plan | Array | 计划列表，取值范围[0,8] |
| data.plan[].name | String | 计划名称，取值范围[0,32] |
| data.plan[].repeatPeriod | Array | 重复周期，为空执行一次，取值范围[1,16]：0-周一、1-周二、...、6-周日 |
| data.plan[].action | Array | 计划操作内容，取值范围[1,8] |
| data.plan[].action[].actionType | String | 执行动作URI，取值范围[1,2556] |
| data.plan[].action[].endValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,256] |
| data.plan[].action[].startValue | String | 执行动作的identifier的值(根据具体协议定制，类型)，取值范围[0,256] |
| data.plan[].startTime | String | 触发时间，格式：08:00，取值范围[1,32] |
| data.plan[].sustain | Integer | 持续时间，单位：分钟，取值范围[0,1440] |
| data.plan[].enabled | Boolean | 使能开关 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |