# API-通用AI-人脸识别-创建人脸集合

> 更新时间: 2026-07-01T18:43:45.000+08:00

> 文档ID: 1309 | 来源树: AI

---

## 创建人脸集合

- 接口功能

   该接口用于创建人脸识别的人脸集合，可设置人脸集合在人脸识别中的模式、阈值、优先级等信息。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/set/create`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | setName | String | 集合名称，长度不大于 50 字节，不能包含特殊字符 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/set/create' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'setName=test'
```

- 返回数据

```
{
    "requestId": "2d2ef768294549349499331685a5caa7",
    "data": {
        "setToken": "5784971dSb58bE49b9Ta7d3S95e4023f18e9"
    },
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data.setToken | String | 人脸集合唯一标识 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 10001 | 参数错误 |  |
| 10002 | accessToken过期或异常 |  |
| 10004 | 用户不存在 |  |
| 10005 | appKey异常 |  |
| 10007 | 调用次数超限 |  |
| 10013 | 无权限调用 |  |
| 10029 | 接口调用太频繁 |  |
| 49999 | 操作异常 | 接口调用异常 |
| 50000 | 服务器异常 |  |
| 60200 | 非法的服务名 |  |
| 60201 | 缺失必传参数或参数校验错误 |  |
| 60202 | 参数解析错误 |  |
| 60203 | 未开通相关服务 |  |
| 60204 | 服务已开通 |  |
| 60205 | 服务内部错误 |  |
| 60206 | 并发数超限 |  |
| 60210 | 图片数据错误 |  |
| 60211 | 图片尺寸错误(太大或太小) |  |
| 60212 | 图片大小超过2M限制 |  |
| 60213 | 下载图片失败 |  |
| 60214 | 参数错误 |  |
| 60215 | 转存图片失败 |  |
| 60216 | 参数错误：无效服务名称 |  |
| 60220 | setToken不存在 |  |
| 60221 | setToken数量超过10个 |  |
| 60222 | faceToken数量超过10个 |  |
| 60223 | faceToken不存在 |  |
| 60404 | 找不到人脸 |  |
| 60405 | 图片地址错误 |  |
| 60406 | 仅支持一张人脸 |  |
| 60507 | 服务超时 |  |
| 60508 | 服务器繁忙 |  |
| 60509 | 该功能暂时不支持 |  |