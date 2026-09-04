# API-通用AI-人体人形识别-人形检测

> 更新时间: 2026-07-01T18:43:43.000+08:00

> 文档ID: 1307 | 来源树: AI

---

## 人形检测

- 接口功能

   该接口用于对一张图片的人形分析，给出分析结论及图片中人形的坐标数据。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/human/analysis/detect`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型：1-传base64编码的二进制图片数据；0-传图片URL，一般支持png、jpg、bmp格式，其他格式的URL无法识别 | Y |
| Body | image | String | 待分析的图片数据或URL，图片数据大小最大2M，分辨率范围：288\*512~4800\*2704。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作。 | Y |
| Body | operation | String | 默认仅返回是否有人，可选属性列表：number-返回具体人数，rect-返回检测的人形坐标数据，只能二选一 | N |
| Body | confidence | Int | 置信度，范围为0-100。为空时将使用服务端推荐的置信度（60），置信度越高，识别结果越精准，但可能存在漏报 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/human/analysis/detect' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'operation=number'
```

- 返回数据

```
{
    "requestId": "985610d17fd9473484f53186b317c246",
    "data": {
        "locations": [
            {
                "x": 469,
                "y": 274,
                "width": 141,
                "height": 433
            },
            {
                "x": 139,
                "y": 289,
                "width": 191,
                "height": 409
            }
        ],
        "exists": true,
        "number": 3
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
| data.exists | Boolean | 是否有人：true-有人，false-无人 |
| data.number | Int | 检测出的具体人数 |
| data.locations | Array | 检测出的人形列表，如果没有检测出人形则为空数组 |
| data.locations[].x | Int | 人形框左上角的横坐标，单位 px |
| data.locations[].y | Int | 人形框左上角的纵坐标，单位 px |
| data.locations[].width | Int | 人形框的宽度，单位 px |
| data.locations[].height | Int | 人形框的高度，单位 px |

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