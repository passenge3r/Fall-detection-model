# API-通用AI-文字识别-身份证识别

> 更新时间: 2026-07-01T18:43:13.000+08:00

> 文档ID: 1296 | 来源树: AI

---

## 身份证识别

- 接口功能

   该接口用于提供对一张身份证的识别能力，分析身份证的相关数据。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/ocr/idCard`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0：图片URL; 1:base64 编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据或URL，图片数据大小最大2M，图片大小288\*288px~4096\*4096px。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | front | Boolean | 是否身份证正面带照片的一面，true-正面，false-反面 | Y |
| Body | operation | String | 默认仅返回文字，rect-返回文字坐标 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/ocr/idCard' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'front=true'
```

- 返回数据

```
{
    "requestId": "ba37e869a03946288edc36d413I013d3",
    "data": {
        "words": {
            "姓名": "刘伟",
            "民族": "彝",
            "住址": "云南省临沧市凤庆县新华彝族乡刘家小组23号",
            "公民身份号码": "533522199107060816",
            "出生": "19910706",
            "性别": "男"
        },
        "locations": {
            "姓名": { "x": 324, "y": 284, "width": 100, "height": 42 },
            "民族": { "x": 541, "y": 366, "width": 29, "height": 36 },
            "住址": { "x": 325, "y": 519, "width": 417, "height": 103 },
            "公民身份号码": { "x": 490, "y": 717, "width": 550, "height": 59 },
            "出生": { "x": 319, "y": 435, "width": 351, "height": 48 },
            "性别": { "x": 326, "y": 371, "width": 29, "height": 37 }
        }
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
| data.words | Map<String,String> | 每个字段信息 |
| data.locations | Map<String,Location> | 每个字段对应的坐标信息(注:如果没有检测出文字则为空) |

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