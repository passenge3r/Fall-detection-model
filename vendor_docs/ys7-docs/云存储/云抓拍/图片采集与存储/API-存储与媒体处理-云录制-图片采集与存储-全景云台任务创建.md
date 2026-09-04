# API-存储与媒体处理-云录制-图片采集与存储-全景云台任务创建

> 更新时间: 2026-06-30T17:53:27.000+08:00

> 文档ID: 1391 | 来源树: 云存储

---

## 全景云台任务创建

- 接口功能

   支持针对云台机创建全景抓拍任务。

- 请求地址

`https://open.ys7.com/api/service/cloudrecord/pic/panoramic/compose`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 用户令牌 | Y |
| Header | deviceSerial | String | 设备序列号 | Y |
| Header | localIndex | String | 设备通道 | Y |
| Body | projectId | String | 项目ID，项目的唯一标识，需输入已创建的项目ID | Y |
| Body | validateCode | String | 视频解密密钥，设备视频加密情况必需 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/pic/panoramic/compose' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: G12262381' \
--header 'localIndex: 1' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'projectId=001'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "taskId": "4d9d0a832dcf4d3882894c7b08031012"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Object | 返回任务信息 |
| data.taskId | String | 任务ID |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |