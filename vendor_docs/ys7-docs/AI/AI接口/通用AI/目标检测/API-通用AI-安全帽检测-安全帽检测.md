# API-通用AI-安全帽检测-安全帽检测

> 更新时间: 2026-07-01T18:44:48.000+08:00

> 文档ID: 1337 | 来源树: AI

---

## 安全帽检测

- 接口功能

   该接口用于识别用户上传照片中的人体安全帽佩戴情况。安全帽检测建议图片范围：最小640\*480，最大3840\*2160。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/target/analysis`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0:图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 分辨率范围：10\*10 ~ 6000\*6000；图片最大2M。安全帽检测建议图片范围：最小640\*480，最大3840\*2160。注：下载图片时可能由于网络等原因导致下载时间过长，建议使用base64参数直接上传图片；不支持对获得的图片数据进行加解密操作 | Y |
| Body | serviceType | String | 服务类型(只能选一个)："helmet"(安全帽检测) | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/target/analysis' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'serviceType=helmet'
```

- 返回数据

```
{
    "requestId": "123456",
    "data": [
        {
            "id": "temp_a4c2afae56644a48858897a891624332",
            "height": "542",
            "target_list": [
                {
                    "body_rect": {
                        "vmodel_h_f": "0.000000",
                        "vmodel_w_f": "0.000000",
                        "vmodel_x_f": "0.000000",
                        "vmodel_y_f": "0.000000"
                    },
                    "alarm_flg": 0,
                    "uniform_type": 0,
                    "ID": 0,
                    "helmet_type": 1,
                    "head_rect": {
                        "vmodel_h_f": "0.674677",
                        "vmodel_w_f": "0.401227",
                        "vmodel_x_f": "0.240491",
                        "vmodel_y_f": "0.105360"
                    },
                    "color_type": 2
                }
            ],
            "width": "816",
            "rule_info": [],
            "rule_list": [
                [
                    { "y": "0.000000", "x": "0.000000" },
                    { "y": "0.000000", "x": "1.000000" },
                    { "y": "1.000000", "x": "1.000000" },
                    { "y": "1.000000", "x": "0.000000" }
                ]
            ],
            "errorCode": 0
        }
    ],
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
| data | Array | 检测结果列表 |
| data[].id | String | 识别任务临时ID |
| data[].height | Int | 图片高 |
| data[].width | Int | 图片宽 |
| data[].errorCode | Int | 单次任务推理结果 |
| data[].rule\_info | String | 规则信息（无实际含义） |
| data[].rule\_list | Location | 规则坐标（无实际含义） |
| data[].target\_list | Array | 识别目标列表 |
| data[].target\_list[].ID | String | 识别的目标序号 |
| data[].target\_list[].helmet\_type | Int | 安全帽类型（0-未知，1-合法，2-非法） |
| data[].target\_list[].color\_type | Int | 安全帽颜色（1-红，2-黄，3-蓝，4-白，5-其他） |
| data[].target\_list[].head\_rect | Location | 头的坐标 |
| data[].target\_list[].body\_rect | Location | 身体坐标（该字段目前版本无效） |
| data[].target\_list[].alarm\_flg | Int | 报警标志（该字段目前版本无效） |
| data[].target\_list[].uniform\_type | Int | 制服类型（该字段目前版本无效） |
| vmodel\_h\_f | Float | 人头的高度，单位px |
| vmodel\_w\_f | Float | 人头的宽度，单位px |
| vmodel\_x\_f | Float | 人头在图片中左上角的横坐标，单位px |
| vmodel\_y\_f | Float | 人头在图片中左上角的纵坐标，单位px |

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
| 60405 | 图片地址错误 | 图片地址错误 |
| 60507 | 服务超时 | 服务超时 |
| 60508 | 服务器繁忙 | 服务器繁忙 |
| 60509 | 该功能暂时不支持 | 该功能暂时不支持 |
| 60511 | OCR识别失败 | OCR识别失败 |