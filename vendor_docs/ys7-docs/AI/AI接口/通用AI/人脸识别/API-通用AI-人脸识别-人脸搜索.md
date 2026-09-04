# API-通用AI-人脸识别-人脸搜索

> 更新时间: 2026-07-01T18:44:21.000+08:00

> 文档ID: 1326 | 来源树: AI

---

## 人脸搜索

- 接口功能

   该接口用于根据人脸在已注册的人脸库中检索的能力，给出最相似的人脸数据。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/analysis/search`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0：图片URL; 1:base64编码的二进制图片数据；2：已检测出人脸的faceToken)。图片数据大小最大2M，尺寸最大：1280\*1280。注：建议使用base64直接上传图片；不支持对获得的图片数据进行加解密操作；单张图片中必须仅一张人脸，多张人脸的图片无法比对成功 | Y |
| Body | image | String | 需要检索的人脸图片数据或faceToken | Y |
| Body | operation | Array | 搜索选项：需要检索的人脸集合唯一标识、阈值与最大匹配次数。示例：[ { "setToken":"a66f9f63-968d-4194-9e99-731be196e6ae", /\* 指定需要检索的人脸集合唯一标识 \*/ "threshold":80, /\* 识别阈值，范围为0~100之间，默认80 \*/ "matchCount":1 /\* 匹配成功计数，默认为1表示匹配成功一次后即结束识别，0表示需要识别集合中的所有人脸 \*/ } ]。检索的人脸集合可多个，建议最大数组长度20 | Y |
| Body | topNum | Int | 返回最相似人脸的个数，默认1个，最多返回5个 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/analysis/search' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=2' \
--data-urlencode 'image=FACE26e01398Hbde3I4244K91f8H988a6b618e9e' \
--data-urlencode 'operation=[{"setToken":"a66f9f63-968d-4194-9e99-731be196e6ae","threshold":80,"matchCount":1}]'
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
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data | Object | 响应数据 |
| data.results | Array | 检索出匹配的人脸列表信息，如果没有匹配则为空数组 |
| data.results[].faceToken | String | 人脸唯一标识 |
| data.results[].score | Double | 匹配得分 |

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