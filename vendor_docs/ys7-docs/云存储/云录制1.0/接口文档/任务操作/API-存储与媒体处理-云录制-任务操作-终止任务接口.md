# API-存储与媒体处理-云录制-任务操作-终止任务接口

> 更新时间: 2026-06-30T17:51:50.000+08:00

> 文档ID: 1372 | 来源树: 云存储

---

## 终止任务接口

- 接口功能

   可以终止视频录制任务、抽帧任务、抓拍任务。需注意全景抓拍任务目前无法终止。

- 请求地址

`https://open.ys7.com/api/v3/open/cloud/video/frame/stop`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | taskId | String | 任务ID，已经完成的任务不支持终止 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/open/cloud/video/frame/stop' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'taskId=68057165e8fb4204aea0f94f3ac2e2f3'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |