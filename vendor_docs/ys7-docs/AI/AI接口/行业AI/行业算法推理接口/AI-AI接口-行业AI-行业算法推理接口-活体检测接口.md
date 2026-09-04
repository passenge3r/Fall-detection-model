# AI-AI接口-行业AI-行业算法推理接口-活体检测接口

> 更新时间: 2026-07-09T18:38:53.000+08:00

> 文档ID: 519 | 来源树: AI

---

## 活体检测接口

- 接口功能

   该接口可判断捕捉到的人脸是真实人脸，还是伪造的人脸（如：电子设备屏幕中的人脸数字图像等），适用于门禁等需要真人识别的应用场景。注：基于图片中人像的破绽判断目标是否为活体，分为静默式活体检测和动作式活体检测两种。静默式活体检测：单张图片中的人像是否为活体，支持可见光和红外两种成像类型；动作式活体检测：视频中的人像是否符合指定动作。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/liveness/analysis`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | livenessType | String | 检测类型：静默式-SILENT，动作式-ACTION | Y |
| Body | dataType | String | 输入数据类型 0-图片URL，1-Base64编码的二进制图片数据 | Y |
| Body | imageData | String | 输入的图像或视频URL或Base64编码数据，数据限制: 静默式：最大2M 动作式：最大8M，视频帧率不低于5，且视频时长不高于 动作数\*5s | Y |
| Body | imageType | String | 静默式活体检测 成像类型：可见光-RGB，红外-IR，默认值RGB | N |
| Body | squenceId | String | 动作序列id，动作式必填 | N |
| Body | option | String | 动作式活体检测选项(JSON字符串)，比如： { "bestFrame"：true // 是否需要返回最佳截图 } | N |
| Body | compareDataType | String | 活体比对数据类型 0-图片URL;1-base64 编码的二进制图片数据; 2-faceToken | N |
| Body | compareImageParam | String | 待比对人脸数据 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/liveness/analysis' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'livenessType=SILENT' \
--data-urlencode 'dataType=0' \
--data-urlencode 'imageData=xxxxx' \
--data-urlencode 'imageType=RGB' \
--data-urlencode 'squenceId=xxxxx' \
--data-urlencode 'option=xxxxx' \
--data-urlencode 'compareDataType=xxxxx' \
--data-urlencode 'compareImageParam=xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": {
        "score": 0.11978016048669815,
        "confidence": 0.0,
        "poseYaw": 40.0,
        "clearity": 0.910641,
        "eyeDistance": 55.233173,
        "posePitch": 6.515779
    },
    "requestId": "79e104ba5c3846949e41d51adfb6d177"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | Int | 状态码 |
| msg | String | 提示信息 |
| requestId | String | 识别的目标序号 |
| data | Object | 活体检测结果 |
| confidence | Double | 活体置信度 |
| clearity | Double | 人脸清晰度 |
| eyeDistance | Double | 人脸瞳距 |
| poseYaw | Double | 平面外左右偏转角，人脸朝左为正 |
| posePitch | Double | 平面外上下俯仰角，人脸朝上为正 |
| score | Double | 比对相似度 |

   静默式活体判断规则：接口输出的清晰度、瞳距、人脸左右以及上下角作为活体检测的辅助，需要先使用这几项值进行人脸质量评判，评判不通过则表示对于该图片中的人脸，活体置信度不可信。以下为评判项和活体置信度推荐阈值：清晰度不低于0.3；瞳距不低于30；左右偏转角在[-60°, 60°]；上下俯仰角在[-40°, 40°]；活体置信度阈值不低于0.3。

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |

   其余返回码请参见公共返回码。