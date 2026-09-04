# API-通用AI-文字识别-车牌识别

> 更新时间: 2026-07-01T18:43:40.000+08:00

> 文档ID: 1305 | 来源树: AI

---

## 车牌识别

- 接口功能

   该接口用于识别车牌号，返回每个关键字及坐标。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/ocr/licensePlate`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0:图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据或URL，图片数据大小最大2M，图片大小288\*288px~4096\*4096px。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | scene | String | 可选值：lpr，general；默认值general。lpr：表示大角度(车牌相对地面水平线的角度)的车牌识别场景；general：通用的车牌识别场景，即正常角度的车牌识别，并且支持粤港澳车牌 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/ocr/licensePlate' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image='
```

- 返回数据

```
{
    "requestId": "e25c5b62d67b43039a04fb48e5a34b89",
    "code": "200",
    "msg": "操作成功",
    "data": {
        "number": "浙A12303",
        "words": [
            {
                "number": "浙A12303",
                "color": "blue",
                "confidence": [
                    0.901937,
                    0.901405,
                    0.901709,
                    0.899689,
                    0.901991,
                    0.891825,
                    0.917735
                ],
                "location": [
                    { "y": 299, "x": 349 },
                    { "y": 299, "x": 401 },
                    { "y": 343, "x": 401 },
                    { "y": 343, "x": 349 }
                ]
            }
        ]
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data.number | String | 车牌号码 |
| data.words | Array | 多车牌识别信息 |
| words[].number | String | 车牌号码 |
| words[].color | String | 车牌颜色：blue-蓝牌，green-绿牌，yellow-黄牌 |
| words[].confidence | Array<Float> | 车牌中每个字符的置信度，区间为0-1 |
| words[].location | Array | 多边形顶点位置信息 |
| words[].location[].x | Int | 顶点横坐标 |
| words[].location[].y | Int | 顶点纵坐标 |

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
| 60405 | 图片地址错误 |  |
| 60507 | 服务超时 |  |
| 60508 | 服务器繁忙 |  |
| 60509 | 该功能暂时不支持 |  |
| 60511 | OCR识别失败 |  |