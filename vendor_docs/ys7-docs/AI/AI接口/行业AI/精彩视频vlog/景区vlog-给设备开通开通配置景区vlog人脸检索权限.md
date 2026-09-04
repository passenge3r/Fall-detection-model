# 景区vlog-给设备开通开通配置景区vlog人脸检索权限

>  

> 更新时间: 2026-06-22T10:32:38.000+08:00

> 文档ID: 4067 | 来源树: AI

---

## 给设备开通配置景区vlog人脸检索权限

- 接口功能

   给设备开通配置景区vlog人脸检索权限。注意：设备需要有人脸抓拍能力且能支持事件云存储

- 请求地址

`https://open.ys7.com/api/service/open/scenic/spot/vlog/device/open`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | deviceSerial | String | 设备序列号 | Y |
| body | projectId | String | 项目id，长度0-31 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/open/scenic/spot/vlog/device/open' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'projectId=value' \
--data-urlencode 'deviceSerial=DEVICE_SERIAL'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": true
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta |
| -code | Int | code |
| -message | String | message |
| -moreInfo | Object | moreInfo |
| data | String | data |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 404 | 资源不存在 |  |
| 500 | 服务器异常 |  |
| 400 | 参数错误 |  |