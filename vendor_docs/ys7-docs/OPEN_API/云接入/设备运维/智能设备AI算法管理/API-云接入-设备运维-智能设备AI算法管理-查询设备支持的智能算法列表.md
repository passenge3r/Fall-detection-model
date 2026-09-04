# API-云接入-设备运维-智能设备AI算法管理-查询设备支持的智能算法列表

> 更新时间: 2026-07-09T13:40:51.000+08:00

> 文档ID: 730 | 来源树: OPEN_API

---

## 查询设备支持算法列表

- 接口功能

   查询指定设备支持的智能算法列表

- 请求地址

`https://open.ys7.com/api/v3/intelligent/model/device/support`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Body | deviceSerial | String | 设备序列号（放在params中请求） | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/intelligent/model/device/support' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=xxxxx'
```

- 返回数据

```
{
    "data": [
        {
            "appId": "app_car_detect",
            "desc": "车辆检测"
        },
        {
            "appId": "app_departure_detect",
            "desc": "工作规范巡检"
        },
        {
            "appId": "app_face_recognize",
            "desc": "人脸识别"
        },
        {
            "appId": "app_video_change",
            "desc": "画面变化"
        },
        {
            "appId": "app_heterolight_detect",
            "desc": "异光检测"
        },
        {
            "appId": "app_heterophony_detect",
            "desc": "异声检测"
        },
        {
            "appId": "app_human_detect",
            "desc": "人形检测"
        },
        {
            "appId": "app_leave_post_detect",
            "desc": "离岗检测"
        },
        {
            "appId": "app_pet_detect",
            "desc": "宠物检测"
        },
        {
            "appId": "app_smog_detect",
            "desc": "烟雾检测"
        },
        {
            "appId": "app_tumble_detect",
            "desc": "跌倒检测"
        }
    ],
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| data | Array<object> | 设备支持的算法列表 |
| appId | String | 算法appid |
| desc | String | 算法描述 |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| moreInfo | String | 附加信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 2000 | 设备不存在 |  |
| 2001 | 通道不存在或不属于当前用户 |  |
| 500 | 操作失败 |  |