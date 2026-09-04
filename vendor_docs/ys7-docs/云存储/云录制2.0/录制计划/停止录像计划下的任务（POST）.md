# 停止录像计划下的任务（POST）

>  

> 更新时间: 2026-06-11T14:49:54.000+08:00

> 文档ID: 4862 | 来源树: 云存储

---

## 停止录像计划下的任务

- 接口功能

   停止录像计划下的任务

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/video/plan/task/stop`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | id | Long | 任务主键id，可通过[录像计划下的任务列表查询](https://open.ys7.com/help/4860)或[根据设备序列号和通道号查询该执行中的任务列表](https://open.ys7.com/help/4861)获取 | Y |
| body | planId | Long | 计划id | Y |
| body | spaceId | Long | 空间id | Y |

- 请求示例

```
curl --location 'https://open.ys7.com/api/service/cloudrecord/video/plan/task/stop' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'spaceId=4028' \
--data-urlencode 'planId=263666' \
--data-urlencode 'id=1662208'
```

- 返回数据

```
{
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
| meta | Object | meta信息 |
| -code | Int | 状态码 |
| -message | String | 状态信息 |
| -moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 404 | 资源不存在 | 请求的资源不存在 |
| 500 | 服务器异常 | 服务器内部错误 |
| 400 | 参数错误 | 请求参数有误 |