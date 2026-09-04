# API-设备云组件仓-执法记录仪-远程巡检组件-巡检事件-更新巡检事件

> 更新时间: 2026-07-09T13:42:43.000+08:00

> 文档ID: 748 | 来源树: OPEN_API

---

## 更新巡检事件

- 接口功能

   如果添加的巡检事件出现未录到关键信息等问题，可以更新巡检事件。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect/event`

- 请求方式

`PUT`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Body | inspectRecordId | Int | 巡检记录ID | Y |
| Body | inspectEventId | Int | 巡检事件ID | Y |
| Body | eventType | String | 事件标签 | N |
| Body | evidenceFileSource | String | 存证文件类型： local-本地上传，cloud\_record-云录制 | N |
| Body | evidenceFileId | String | 存证文件ID，如果是云录制，填写录制taskId | N |
| Body | eventRemark | String | 事件备注 | N |

- 请求示例

```
curl --location --request PUT 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect/event' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'inspectRecordId=xxxxx' \
--data-urlencode 'inspectEventId=xxxxx' \
--data-urlencode 'eventType=xxxxx' \
--data-urlencode 'evidenceFileSource=xxxxx' \
--data-urlencode 'evidenceFileId=xxxxx' \
--data-urlencode 'eventRemark=xxxxx'
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
| code | Int | 错误码 |
| message | String | 错误描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 |  |
| 49999 | 数据异常 |  |
| 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 资源不存在 |  |