# API-通用AI-人脸识别-人脸对比

> 更新时间: 2026-07-01T18:44:19.000+08:00

> 文档ID: 1325 | 来源树: AI

---

## 人脸比对

- 接口功能

   该接口用于两张图片中的人脸进行检测分析与比对。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/analysis/compare`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型：0-图片URL；1-base64编码的二进制图片数据；2-已检测出人脸的faceToken。两张需要比对的图片数据/URL/faceToken，单张图片数据大小最大2M，尺寸最大：1280\*1280。注：建议使用base64直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | imageParam1 | String | 需要比对的faceToken1或图片数据1。注：单张图片中必须仅一张人脸，多张人脸的图片无法比对成功 | Y |
| Body | imageParam2 | String | 需要比对的faceToken2或图片数据2。注：单张图片中必须仅一张人脸，多张人脸的图片无法比对成功。imageParam1和imageParam2数据类型需为同一dataType | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/analysis/compare' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=0' \
--data-urlencode 'imageParam1=https://xxx.xxx.com/1.jpg' \
--data-urlencode 'imageParam2=https://xxx.xxx.com/2.jpg'
```

- 返回数据

```
{
    "requestId": "fce534349b954378992b269d2b5b6cba",
    "data": {
        "score": 0.9996836185455322
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
| data | Object | 响应数据 |
| data.score | Double | 比对得分，介于0~1之间，越大标识两张图片相似度越高 |

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
| 60404 | 找不到人脸 | 找不到人脸 |
| 60405 | 图片地址错误 | 图片地址错误 |
| 60406 | 仅支持一张人脸 | 仅支持一张人脸 |
| 60507 | 服务超时 | 服务超时 |
| 60508 | 服务器繁忙 | 服务器繁忙 |
| 60509 | 该功能暂时不支持 | 该功能暂时不支持 |

**QA记录**

**问题1** 问：返回图片下载失败。答：检查url是不是能够被外网访问；检查url是不是放到了query里面，如果放到了query里面并且有特殊字符的话会被转义，导致url无法访问。

**问题2** 问：返回图片有人脸，但是找不到人脸。答：检查图片是不是横着的，目前只支持竖着的人脸识别。