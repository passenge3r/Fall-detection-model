# API-设备云组件仓-执法记录仪-远程巡检组件-巡检设备使用情况统计

>  

> 更新时间: 2026-06-30T11:48:23.000+08:00

> 文档ID: 1540 | 来源树: OPEN_API

---

## 巡检设备使用情况统计

- 接口功能

   巡检设备使用情况统计。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/stats/device`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| query | inspectDistrictId | String | 巡检区域id | Y |
| query | inspectDistrictCode | String | 巡检区域标识，worksite-工地，worksite即为工地场景的标识 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/stats/device?inspectDistrictId=1&inspectDistrictCode=worksite' \
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
            "deviceTag": "body_worn_camera",
            "deviceTagDesc": "执法记录仪",
            "deviceCount": 1,
            "onlineDeviceCount": 1,
            "onlineDeviceRate": 100
        },
        {
            "deviceTag": "helmet_camera",
            "deviceTagDesc": "头盔摄像机",
            "deviceCount": 1,
            "onlineDeviceCount": 1,
            "onlineDeviceRate": 100
        },
        {
            "deviceTag": "safety_hat_camera",
            "deviceTagDesc": "安全帽相机",
            "deviceCount": 3,
            "onlineDeviceCount": 2,
            "onlineDeviceRate": 66.67
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |
| data | Array<Object> | 设备统计列表 |
| data.deviceTag | String | 设备标签 |
| data.deviceTagDesc | String | 设备标签描述 |
| data.deviceCount | Int | 设备总数 |
| data.onlineDeviceCount | Int | 设备在线数量 |
| data.onlineDeviceRate | String | 在线设备率(在线设备数/总设备数) |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |