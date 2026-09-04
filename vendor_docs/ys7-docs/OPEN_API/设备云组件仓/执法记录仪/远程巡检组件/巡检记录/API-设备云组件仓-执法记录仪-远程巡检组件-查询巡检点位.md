# API-设备云组件仓-执法记录仪-远程巡检组件-查询巡检点位

>  

> 更新时间: 2026-06-30T11:48:18.000+08:00

> 文档ID: 1538 | 来源树: OPEN_API

---

## 查询巡检点位

- 接口功能

   可查询某次巡检记录中的重点巡检点位信息。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect/point`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| query | inspectRecordId | String | 巡检记录id | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect/point?inspectRecordId=1' \
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
            "inspectPointId": "xxxx",
            "inspectPointName": "巡检1",
            "latitude": 40.2273,
            "longitude": 116.263379,
            "radius": 5
        },
        {
            "inspectPointId": "xxxx",
            "inspectPointName": "巡检2",
            "latitude": 40.2273,
            "longitude": 116.263379,
            "radius": 5
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
| data | Array<Object> | 巡检点位列表 |
| data.inspectPointId | String | 点位编号 |
| data.inspectPointName | String | 点位名称 |
| data.longitude | Float | 经度，用于标识点位的位置经度，支持小数点后六位，不传默认为0 |
| data.latitude | Float | 纬度，用于标识点位的位置纬度，支持小数点后六位，不传默认为0 |
| data.radius | Int | 巡检半径 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 接口调用异常 |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |