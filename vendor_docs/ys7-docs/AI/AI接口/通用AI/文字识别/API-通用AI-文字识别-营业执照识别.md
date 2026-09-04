# API-通用AI-文字识别-营业执照识别

> 更新时间: 2026-07-06T13:51:25.000+08:00

> 文档ID: 1303 | 来源树: AI

---

## 营业执照识别

- 接口功能

   该接口用于提供对一张营业执照的识别能力，分析营业执照的相关数据。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/ocr/businessLicense`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0：图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据或URL，图片数据大小最大2M，图片大小288\*288px~4096\*4096px。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | operation | String | 默认仅返回文字，rect:返回文字坐标 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/ocr/businessLicense' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'operation=rect'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": {
        "words": {
            "社会信用代码": "9xxx109578965298C",
            "法人": "陈艳",
            "地址": "重庆市北碚区北温泉街道安礼路128号大学科技园科技创业中心2幢504",
            "单位名称": "重庆蓝维科技有限公司",
            "有效期": "2999年12月31日"
        },
        "locations": {
            "社会信用代码": { "x": 138, "y": 444, "width": 363, "height": 0 },
            "法人": { "x": 324, "y": 852, "width": 58, "height": 0 },
            "地址": { "x": 1428, "y": 913, "width": 606, "height": 1 },
            "单位名称": { "x": 325, "y": 723, "width": 272, "height": 2 },
            "有效期": { "x": 1426, "y": 850, "width": 271, "height": 0 }
        }
    },
    "requestId": "0e98ae707912417ca4364927b0fae534"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data.words | Map<String,String> | 每个字段信息（注：如果没有检测出文字则为空） |
| data.locations | Map<String,Location> | 每个字段对应的坐标信息（注：如果没有检测出文字则为空） |

**坐标（Location）**

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| height | Int | 文字的高度,单位px |
| width | Int | 文字的宽度,单位px |
| x | Int | 文字左上角的横坐标,单位px |
| y | Int | 文字左上角的纵坐标,单位px |

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