# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-添加区域信息

> 更新时间: 2026-06-30T11:55:15.000+08:00

> 文档ID: 1621 | 来源树: OPEN_API

---

## 添加区域信息

- 接口功能

   录入区域信息，电梯可与区域进行绑定

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/worksite/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | worksiteName | String | 工地名称 | Y |
| body | province | String | 省 | N |
| body | city | String | 市 | Y |
| body | district | String | 区 | Y |
| body | street | String | 街道 | N |
| body | longitude | Float | 经度 | N |
| body | latitude | Float | 纬度 | Y |
| body | worksiteRegion | String | 工地区域 | Y |
| body | note | String | 备注信息 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/elevator/worksite/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'worksiteName=示例区域' \
--data-urlencode 'province=浙江省' \
--data-urlencode 'city=杭州市' \
--data-urlencode 'district=滨江区' \
--data-urlencode 'street=西兴街道' \
--data-urlencode 'longitude=120.21' \
--data-urlencode 'latitude=30.21' \
--data-urlencode 'worksiteRegion=区域信息' \
--data-urlencode 'note='
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "worksiteId": "b877b4bbbc734d4386d77beb85164766"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应信息 |
| meta.code | Int | 响应码 |
| meta.message | String | 响应码描述 |
| data | Object | 响应体 |
| data.worksiteId | String | 区域唯一标识 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |