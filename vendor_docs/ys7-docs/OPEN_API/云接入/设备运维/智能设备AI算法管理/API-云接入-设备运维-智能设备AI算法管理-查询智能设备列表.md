# API-云接入-设备运维-智能设备AI算法管理-查询智能设备列表

> 更新时间: 2026-07-09T13:40:53.000+08:00

> 文档ID: 731 | 来源树: OPEN_API

---

## 查询智能设备列表

- 接口功能

   查询智能设备列表（设备上已加载的算法）

- 请求地址

`https://open.ys7.com/api/v3/intelligent/model/device`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取方法](https://open.ys7.com/help/81) | Y |
| Body | deviceSerial | String | 关键字查询 分页参数与设备序列号两者 只可输入其一 | N |
| Body | pageStart | Integer | 页码，从0开始，默认为0 | N |
| Body | pageSize | Integer | 单页数量（单页限制数量8~50个） | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/intelligent/model/device' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'deviceSerial=xxxxx' \
--data-urlencode 'pageStart=xxxxx' \
--data-urlencode 'pageSize=xxxxx'
```

- 返回数据

```
{
    "data": [
        {
            "deviceName": "设备名称",
            "deviceSerial": "设备序列号",
            "deviceType": "设备型号",
            "status": 0,
            "models": [
                {
                    "appId": "1231323",
                    "modelName": "模型测试测试测试测试",
                    "version": "V1.0.0",
                    "loadStatus": 1
                }
            ]
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
| data | Array<object> | 智能设备列表 |
| deviceName | String | 设备名称 |
| deviceSerial | String | 设备序列号 |
| deviceType | String | 设备型号 |
| status | Int | 设备状态 |
| models | Array<object> | 算法模型列表 |
| appId | String | 算法appid |
| modelName | String | 模型名称 |
| version | String | 版本 |
| loadStatus | Int | 加载状态 |
| meta | Object | 服务响应信息 |
| code | Int | 错误码 |
| message | String | 错误描述 |
| moreInfo | String | 附加信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 400 | 参数错误 |  |
| 500 | 服务异常 |  |