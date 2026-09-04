# API-设备云组件仓-智能电梯网络摄像机-电梯物联组件-电梯信息删除

> 更新时间: 2026-06-30T11:55:10.000+08:00

> 文档ID: 1619 | 来源树: OPEN_API

---

## 电梯信息删除

- 接口功能

   删除电梯信息

- 请求地址

`https://open.ys7.com/api/service/devicekit/elevator/info/delete`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| header | elevatorSerial | String | 电梯唯一id | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/devicekit/elevator/info/delete' \
--header 'accessToken: at.xxxxx' \
--header 'elevatorSerial: 2dea4ab0051142eea09cd64853b6eb97'
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
| meta | Object | 响应状态 |
| meta.code | Int | 错误码 |
| meta.message | String | code描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 10001 | 请求参数错误 | 请检查请求参数 |
| 20018 | 该用户不拥有该设备 | 请检查设备归属 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |