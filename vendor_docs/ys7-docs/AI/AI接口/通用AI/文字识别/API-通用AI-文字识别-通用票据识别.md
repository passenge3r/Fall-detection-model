# API-通用AI-文字识别-通用票据识别

> 更新时间: 2026-07-01T18:43:38.000+08:00

> 文档ID: 1304 | 来源树: AI

---

## 通用票据识别

- 接口功能

   该接口用于提供对一张票据的识别能力，分析票据的相关数据。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/ocr/receipt`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0:图片URL;1:base64 编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据或URL，图片数据大小最大2M，图片大小800\*600px~4096\*2160px（但宽不能大于4096px且高不能大于2160px）。注：下载图片时可能由于网络等原因导致下载图片时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | operation | String | 默认仅返回文字，rect:返回文字坐标 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/ocr/receipt' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'operation=rect'
```

- 返回数据

```
{
    "requestId": "36cdc191e89a42c9938771177e757f9d",
    "data": {
        "words": [
            "广东省行政事业型收费统一票据",
            "AdmnistatonandlerpiseschargeUntaryi",
            "ofGuangdongProvnce",
            "广东省",
            "AC4965752",
            "缴款单位(人):",
            "2013年9月18日",
            "Payer",
            "改",
            "M",
            "D",
            "执收单位代码项目编码",
            "项目名称|计费单位计费数量收费标准金额",
            "Unitword",
            "ltemcode",
            "Chargetem",
            "Unit",
            "Quantity|ChageSandad",
            "Amount",
            "30086001301|往来港澳通行证",
            "40.00",
            "第",
            "联",
            "存8",
            "合计十人民币(大写)佰拾万\\4四贔零元零角￥￥40.0",
            "①",
            "金",
            "缴款通知书编号",
            "缴款方",
            "(03)",
            "根",
            "AdvceNoteNo",
            "PaymentMethod",
            "现金",
            "备注",
            "Notes",
            "收款单位(盖章):",
            "开票人:周婉玲",
            "收款人:",
            "广东省财政厅印制",
            "Receiver(seal)",
            "Drawe",
            "Payee",
            "printedbyGuangdongPr",
            "Bureau",
            "(机打票据,手写无效)"
        ]
    },
    "code": "200",
    "msg": "操作成功"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 状态码(200-成功,其余失败) |
| msg | String | 提示信息 |
| requestId | String | 请求ID |
| data.words | Array<String> | 每行文字 |
| data.locations | Array<Location> | 每行文字对应的坐标信息 |

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