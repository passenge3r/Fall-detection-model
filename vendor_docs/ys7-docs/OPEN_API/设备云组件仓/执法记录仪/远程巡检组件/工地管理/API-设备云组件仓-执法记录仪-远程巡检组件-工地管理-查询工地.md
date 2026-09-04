# API-设备云组件仓-执法记录仪-远程巡检组件-工地管理-查询工地

>  

> 更新时间: 2026-06-30T11:48:08.000+08:00

> 文档ID: 1535 | 来源树: OPEN_API

---

## 查询工地列表

- 接口功能

   对工地信息进行统一查询，每一个工地的具体工地信息（工地ID、工地名称、工地经度、工地纬度、工地范围、工地备注）以列表形式展现。

- 请求地址

`https://open.ys7.com/api/service/devicekit/common/worksite`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| query | pageStart | Int | 起始页，从0开始 | Y |
| query | pageSize | Int | 分页大小 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/common/worksite?pageStart=0&pageSize=10' \
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
            "worksiteId": "07b7ef7a815f40e08d89b86da392b138",
            "worksiteName": "工地1",
            "longitude": 75.0,
            "latitude": -83.0,
            "worksiteRegion": "-120.123,46.33;-120.30,45.33;-120.45,45.27;-120.123,46.33 ",
            "note": "备注"
        },
        {
            "worksiteId": "0b4a59cc427e404d96bc500c4823aa58",
            "worksiteName": "工地2",
            "longitude": -134.0,
            "latitude": -38.0,
            "worksiteRegion": "-120.123,46.33;-120.30,45.33;-120.45,45.27;-120.123,46.33 ",
            "note": "备注"
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
| data | Array<Object> | 工地列表 |
| data.worksiteId | String | 工地id |
| data.worksiteName | String | 工地名称 |
| data.longitude | Int | 经度 |
| data.latitude | Int | 纬度 |
| data.worksiteRegion | String | 工地区域 |
| data.note | String | 备注 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交[工单](https://open.ys7.com/console/work.html)解决相关问题 |
| 404 | 资源不存在 | 资源不存在 |