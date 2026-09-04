# 人脸特征转换接口（POST）

> 更新时间: 2026-06-17T18:17:57.000+08:00

> 文档ID: 4188 | 来源树: AI

---

## 人脸特征转换接口（POST）

- 接口功能

   封装算法接口，分析图片中的人脸特征

- 请求地址

`https://open.ys7.com/api/service/intelligence/algorithm/analysis/face_recognition_feature_extraction`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| header | accessToken | string | 萤石开放API访问令牌 | Y |
| body | requestId | string | 请求Id，请使用uuid | N |
| body | modelVersion | string | 模型版本 | Y |
| body | dataInfo | array<object> | 请求的输入数据内容 | Y |
| body | -modal | string | 数据模态：image | Y |
| body | -type | string | 数据类型: url;base64 | Y |
| body | -data | object | url地址;base64数据 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/intelligence/algorithm/analysis/face_recognition_feature_extraction' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/json' \
--data-raw '{"requestId":"value", "modelVersion":"value", "dataInfo":"value"}'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "success",
        "moreInfo": null
    },
    "data": {
        "requestId": "AA999",
        "taskType": "face_recognition_feature_extraction",
        "images": [
            {
                "frameIdx": 0,
                "imageHeight": 750,
                "imageWidth": 500,
                "contentAnn": {
                    "bboxes": [
                        {
                            "points": [
                                {
                                    "x": 0.46322152,
                                    "y": 0.042714354
                                },
                                {
                                    "x": 0.69026816,
                                    "y": 0.26233456
                                }
                            ],
                            "care": 1,
                            "weight": 0.99887246,
                            "negflag": 0,
                            "index": 0,
                            "tagInfo": {
                                "tag": "face",
                                "labels": null
                            }
                        }
                    ],
                    "textInfos": null
                },
                "contentAnn2": {
                    "embedding": [
                        "WzAuMCwgLTEuMCwgLTEuMCwMi4wLCAyLjAsICAtMy4wXQ=="
                    ],
                    "embedding_length": [
                        1024
                    ],
                    "embedding_version": [
                        "V5.0.0 Build 240925"
                    ]
                }
            }
        ],
        "completion": null,
        "audio": null,
        "text": null,
        "health": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| meta | object | meta |
| -code | int | code |
| -message | string | message |
| -moreInfo | object | moreInfo |
| data | object | data |
| -requestId | string | requestId |
| -taskType | string | taskType |
| -images | array<object> | images |
| --frameIdx | int | frameIdx |
| --imageHeight | int | imageHeight |
| --imageWidth | int | imageWidth |
| --contentAnn | object | contentAnn |
| ---bboxes | array<object> | bboxes |
| ----points | array<object> | points |
| -----x | number | x |
| -----y | number | y |
| ----care | int | care |
| ----weight | number | weight |
| ----negflag | int | negflag |
| ----index | int | index |
| ----tagInfo | object | tagInfo |
| -----tag | string | tag |
| -----labels | object | labels |
| ---textInfos | object | textInfos |
| --contentAnn2 | object | contentAnn2 |
| ---embedding | array<string> | embedding |
| ---embedding\_length | array<integer> | embedding\_length |
| ---embedding\_version | array<string> | embedding\_version |
| -completion | object | completion |
| -audio | object | audio |
| -text | object | text |
| -health | object | health |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
|  |  |  |
| --- | --- | --- |
| 200 | 操作成功 |  |
| 500 | 服务器异常 |  |
| 10002 | accessToken过期或异常 |  |
| 60202 | 参数解析错误 |  |
| 7000 | 用户请求参数非法 |  |