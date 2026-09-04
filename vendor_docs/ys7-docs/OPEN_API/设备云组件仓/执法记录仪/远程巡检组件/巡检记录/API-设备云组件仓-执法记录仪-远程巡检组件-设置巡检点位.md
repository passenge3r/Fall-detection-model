# API-设备云组件仓-执法记录仪-远程巡检组件-设置巡检点位

>  

> 更新时间: 2026-06-30T11:48:16.000+08:00

> 文档ID: 1537 | 来源树: OPEN_API

---

## 设置巡检点位

- 接口功能

   可以为某巡检任务设置所需巡检的重点点位，对该点位进行巡检要求，例如某次巡检必须巡检到A楼北面建设点。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect/point`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| body | inspectRecordId | Int | 巡检记录id | Y |
| body | inspectPointName | String | 点位名称 | Y |
| body | longitude | Float | 经度，用于标识点位的位置经度，支持小数点后六位，不传默认为0，示例：116.263379 | N |
| body | latitude | Float | 纬度，用于标识点位的位置纬度，支持小数点后六位，不传默认为0，示例：40.2273 | N |
| body | radius | Int | 巡检半径，默认为0 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect/point' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"inspectRecordId":1,"inspectPointName":"A楼北面建设点","longitude":116.263379,"latitude":40.2273,"radius":100}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 错误码 |
| meta.message | String | 错误描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交[工单](https://open.ys7.com/console/work.html)解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |