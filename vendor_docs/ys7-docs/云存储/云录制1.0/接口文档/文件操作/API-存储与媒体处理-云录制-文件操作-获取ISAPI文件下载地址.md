# API-存储与媒体处理-云录制-文件操作-获取ISAPI文件下载地址

> 更新时间: 2026-06-30T17:52:04.000+08:00

> 文档ID: 1376 | 来源树: 云存储

---

## 获取ISAPI文件下载地址

- 接口功能

   获取ISAPI文件下载地址。

- 请求地址

`https://open.ys7.com/api/lapp/mq/downloadurl`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | appKey | String | 开发者appKey | Y |
| Query | fileKey | String | ISAPI上行报文中的picUrl字段 | Y |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/lapp/mq/downloadurl?appKey=xxxxx&fileKey=ISAPI_FILES/F998xxxxx_1/2021061021xxxx-F99xxxx-1-10000'
```

- 返回数据

```
{
    "code": "200",
    "msg": "操作成功!",
    "data": "http://xxx.xxx.com/xxx.jpg"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| data | String | ISAPI文件下载地址 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10005 | appKey异常 | appKey被冻结 |
| 49999 | 数据异常 | 接口调用异常 |