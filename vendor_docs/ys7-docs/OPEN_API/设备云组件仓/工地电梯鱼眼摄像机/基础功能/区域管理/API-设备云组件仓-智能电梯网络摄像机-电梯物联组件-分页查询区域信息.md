# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-分页查询区域信息

> 更新时间: 2026-06-30T11:55:21.000+08:00

> 文档ID: 1624 | 来源树: OPEN_API

---

## 分页查询区域信息

- 接口功能

   区域列表查询

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/worksite/list`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| query | pageStart | Int | 开始页码，默认0 | N |
| query | pageSize | Int | 每页条数，取值范围[1,50] | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/service/devicekit/elevator/worksite/list?pageStart=0&pageSize=10' \
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
            "worksiteId": "b877b4bbbc734d4386d77beb85164766",
            "province": "尼日利亚",
            "city": "瓜多",
            "district": "特立尼西亚",
            "street": "章鱼街",
            "worksiteName": "敖德萨2",
            "longitude": 10.21,
            "latitude": 52.21,
            "worksiteRegion": "",
            "note": "",
            "createTime": "2023-07-11 11:56:58",
            "updateTime": "2023-07-11 11:56:58"
        },
        {
            "worksiteId": "f2412cec91c4461a9f64fdc6b618e105",
            "province": "尼日利亚",
            "city": "瓜多",
            "district": "特立尼西亚",
            "street": "章鱼街",
            "worksiteName": "可多",
            "longitude": 10.21,
            "latitude": 52.21,
            "worksiteRegion": "",
            "note": "",
            "createTime": "2023-07-10 20:30:55",
            "updateTime": "2023-07-10 20:31:08"
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Array | 响应体 |
| data[].worksiteName | String | 区域名称 |
| data[].worksiteId | String | 区域id |
| data[].province | String | 省 |
| data[].city | String | 市 |
| data[].district | String | 区 |
| data[].street | String | 街道 |
| data[].longitude | Float | 经度 |
| data[].latitude | Float | 纬度 |
| data[].worksiteRegion | String | 所属区域 |
| data[].note | String | 备注信息 |
| data[].createTime | String | 创建时间 |
| data[].updateTime | String | 更新时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |