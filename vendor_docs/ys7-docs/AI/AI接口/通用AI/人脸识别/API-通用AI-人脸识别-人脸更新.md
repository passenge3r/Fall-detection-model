# API-通用AI-人脸识别-人脸更新

> 更新时间: 2026-07-01T18:44:27.000+08:00

> 文档ID: 1328 | 来源树: AI

---

## 人脸更新

- 接口功能

   提供将已注册的人脸转移到指定人脸集合的能力。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/set/update`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | faceTokens | String | 已检测的人脸唯一标识，多个以英文逗号分割，一次最多支持10个 | Y |
| Body | setToken | String | 注册的人脸集合唯一标识 | Y |
| Body | userDatas | String | 用户数据，json格式，成员id，可选值，可以为null或空。如：{"memberId":"xxx"} | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/set/update' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'faceTokens=a66f9f63-968d-4194-9e99-731be196e6ae' \
--data-urlencode 'setToken=xxxxx' \
--data-urlencode 'userDatas={"memberId":"xxx"}'
```

- 返回数据

```
{
    "data": {
        "results": [
            {
                "faceToken": "a66f9f63-968d-4194-9e99-731be196e6ae",
                "score": 0.99
            }
        ]
    },
    "requestId": "asdfasdfb954378992b269d2b5b6cba",
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码，参考智能服务错误码 |
| msg | String | 提示信息 |
| requestId | String | 请求ID |
| data | Object | 响应数据 |
| data.results | Array | 更新结果列表 |
| data.results[].faceToken | String | 人脸唯一标识 |
| data.results[].score | Float | 相似度得分 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken过期或异常 | 重新获取accessToken |
| 10004 | 用户不存在 | 用户不存在 |
| 10005 | appKey异常 | appKey被冻结 |
| 10007 | 调用次数超限 | 调用次数超限 |
| 10013 | 无权限调用 | 无权限调用 |
| 10029 | 接口调用太频繁 | 降低调用频率 |
| 49999 | 操作异常 | 接口调用异常 |
| 50000 | 服务器异常 | 服务器异常 |
| 60200 | 非法的服务名 | 非法的服务名 |
| 60201 | 缺失必传参数或参数校验错误 | 缺失必传参数或参数校验错误 |
| 60202 | 参数解析错误 | 参数解析错误 |
| 60203 | 未开通相关服务 | 未开通相关服务 |
| 60204 | 服务已开通 | 服务已开通 |
| 60205 | 服务内部错误 | 服务内部错误 |
| 60206 | 并发数超限 | 并发数超限 |
| 60210 | 图片数据错误 | 图片数据错误 |
| 60211 | 图片尺寸错误(太大或太小) | 图片尺寸错误 |
| 60212 | 图片大小超过2M限制 | 图片大小超过2M限制 |
| 60213 | 下载图片失败 | 下载图片失败 |
| 60214 | 参数错误 | 参数错误 |
| 60215 | 转存图片失败 | 转存图片失败 |
| 60216 | 参数错误：无效服务名称 | 无效服务名称 |
| 60220 | setToken不存在 | setToken不存在 |
| 60221 | setToken数量超过10个 | setToken数量超过10个 |
| 60222 | faceToken数量超过10个 | faceToken数量超过10个 |
| 60223 | faceToken不存在 | faceToken不存在 |
| 60404 | 找不到人脸 | 找不到人脸 |
| 60405 | 图片地址错误 | 图片地址错误 |
| 60406 | 仅支持一张人脸 | 仅支持一张人脸 |
| 60507 | 服务超时 | 服务超时 |
| 60508 | 服务器繁忙 | 服务器繁忙 |
| 60509 | 该功能暂时不支持 | 该功能暂时不支持 |