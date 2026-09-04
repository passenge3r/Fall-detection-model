# API-设备云组件仓-执法记录仪-远程巡检组件-巡检事件-添加巡检事件

> 更新时间: 2026-07-09T13:42:10.000+08:00

> 文档ID: 747 | 来源树: OPEN_API

---

## 添加巡检事件

- 接口功能

   在巡检中可添加巡检事件进行存证，便于记录关键、异常信息等。在巡检进行过程中与后续查看巡检记录过程中均可添加巡检事件，存证文件可以是本地上传，也可以是云录制，存证类型有图片与视频两种。

- 请求地址

`https://open.ys7.com/api/service/devicekit/bodycamera/inspect/event`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，获取方式参考[accessToken获取接口](https://open.ys7.com/help/81) | Y |
| Body | inspectRecordId | Int | 巡检记录ID | Y |
| Body | eventType | String | 事件标签 | Y |
| Body | evidenceFileSource | String | 存证文件类型：local-本地上传，cloud\_record-云录制 | Y |
| Body | evidenceFileId | String | 存证文件ID，如果是云录制，填写录制taskId | Y |
| Body | eventTime | String | 事件时间（图片类型事件时间），格式yyyy-MM-dd HH:mm:ss | N |
| Body | eventBeginTime | String | 事件起始时间（视频录制类型事件时间），格式yyyy-MM-dd HH:mm:ss | N |
| Body | eventEndTime | String | 事件结束时间（视频录制类型事件时间），格式yyyy-MM-dd HH:mm:ss | N |
| Body | depositaryOfficer | String | 存证人员 | Y |
| Body | eventRemark | String | 事件备注 | N |
| Body | evidenceFileType | Int | 存证文件类型，0-图片，1-视频 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/bodycamera/inspect/event' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'inspectRecordId=xxxxx' \
--data-urlencode 'eventType=xxxxx' \
--data-urlencode 'evidenceFileSource=xxxxx' \
--data-urlencode 'evidenceFileId=xxxxx' \
--data-urlencode 'eventTime=xxxxx' \
--data-urlencode 'eventBeginTime=xxxxx' \
--data-urlencode 'eventEndTime=xxxxx' \
--data-urlencode 'depositaryOfficer=xxxxx' \
--data-urlencode 'eventRemark=xxxxx' \
--data-urlencode 'evidenceFileType=xxxxx'
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