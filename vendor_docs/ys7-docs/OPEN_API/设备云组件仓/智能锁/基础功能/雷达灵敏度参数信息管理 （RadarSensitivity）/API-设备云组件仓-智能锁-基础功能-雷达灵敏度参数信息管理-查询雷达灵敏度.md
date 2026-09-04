# API-设备云组件仓-智能锁-基础功能-雷达灵敏度参数信息管理-查询雷达灵敏度

> 更新时间: 2026-07-09T13:47:21.000+08:00

> 文档ID: 836 | 来源树: OPEN_API

---

## 查询雷达灵敏度

- 接口功能

   该接口用于查询雷达灵敏度。本文档仅适用于设备型号：CS-DL30-V100系列和CS-Y3000F-V100系列智能门锁，其余型号不保证可用。如下接口调用需要联系萤石配置白名单，否则接口可能调用报错。

- 请求地址

`https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/RadarSensitivity/Sensitivity`

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
curl --location --request GET 'https://open.ys7.com/api/v3/otap/prop/{deviceSerial}/DoorLock/0/RadarSensitivity/Sensitivity' \
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
        "targetResidentTime": 1,
        "speedSensitivity": 1,
        "videoReCheck": true,
        "recoverSensitivityConfigure": true,
        "trailSensitivityLevel": 1,
        "signalSensitivityLevel": 1,
        "swingSensitivityLevel": 1,
        "sceneMode": "Expert",
        "autoSensitivityEnabled": true
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
| data | Object | 业务参数 |
| data.targetResidentTime | Integer | 目标驻留时间，取值范围[1,9] |
| data.speedSensitivity | Integer | 速度灵敏度，取值范围[1,9] |
| data.videoReCheck | Boolean | 视频复核 |
| data.recoverSensitivityConfigure | Boolean | 恢复灵敏度配置 |
| data.trailSensitivityLevel | Integer | 轨迹灵敏度等级，取值范围[1,9] |
| data.signalSensitivityLevel | Integer | 信号灵敏度等级，取值范围[1,9] |
| data.swingSensitivityLevel | Integer | 摆动灵敏度等级，取值范围[1,9] |
| data.sceneMode | String | 场景模式，取值范围[Expert,Open,Shrub,Mode1,Mode2]：Expert-专家模式，Open-空旷模式，Shrub-灌木模式，Mode1-模式1，Mode2-模式2 |
| data.autoSensitivityEnabled | Boolean | 自动调节灵敏度使能 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 成功 | 请求成功 |