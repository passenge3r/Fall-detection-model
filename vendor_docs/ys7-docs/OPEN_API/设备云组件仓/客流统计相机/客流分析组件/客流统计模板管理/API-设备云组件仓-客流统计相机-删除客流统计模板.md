# API-设备云组件仓-客流统计相机-删除客流统计模板

>  

> 更新时间: 2026-06-30T11:48:42.000+08:00

> 文档ID: 1551 | 来源树: OPEN_API

---

## 删除客流统计模板

- 接口功能

   删除客流统计模板

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/template/del`

- 请求方式

`DELETE`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | regionTag | String | 绑定区域，最多32字符 | Y |

- 请求示例

```
curl --location --request DELETE 'https://open.ys7.com/api/service/devicekit/peoplecounting/template/del' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'regionTag=region01'
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
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 20015 | 设备不支持该功能 | 请确认设备是否支持该功能 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 404 | 资源不存在 | 请求的资源不存在 |