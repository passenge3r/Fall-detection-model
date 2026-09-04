# API-设备云组件仓-执法记录仪-远程巡检组件-工地管理-删除工地

>  

> 更新时间: 2026-06-30T11:48:11.000+08:00

> 文档ID: 1536 | 来源树: OPEN_API

---

## 删除工地

- 接口功能

   删除选定工地的信息以及相关记录，与其相关联的记录都会被删除。注：建议尽量勿删除工地，与其相关联的各项信息及记录可能受到影响。

- 请求地址

`https://open.ys7.com/api/service/devicekit/common/worksite`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| body | worksiteId | String | 工地id | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/devicekit/common/worksite' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"worksiteId":"07b7ef7a815f40e08d89b86da392b138"}'
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