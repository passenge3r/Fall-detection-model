# API-通用AI-人脸识别-人脸检测

> 更新时间: 2026-07-01T18:43:59.000+08:00

> 文档ID: 1316 | 来源树: AI

---

## 人脸检测

- 接口功能

   该接口用于对一张图片中的人脸进行检测分析。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/face/analysis/detect`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Body | accessToken | String | 授权过程获取的accessToken | Y |
| Body | dataType | Int | 数据类型(0：图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据(base64编码格式)，图片数据大小最大2M，尺寸最大：1280\*1280 | Y |
| Body | operation | String | 可以是none或者由逗号分割的属性列表。可选：gender:开启性别检测，age:开启年龄检测，glass:开启是否戴眼镜检测，faceScore:人脸评分，expression:微笑检测，singleface:单人脸（默认多人脸检测），faceMark:人脸关键点，mask:是否戴口罩，hat:是否戴帽子，beard:是否有胡须。默认均会检测人脸位置，若检测成功则查询时faceRect均会返回，若指定了其他项则检测查询时返回对应的结果值 | N |
| Body | rol | String | 检测区域矩形框：{"x":0.5, "y":0, "w":0.5, "h":1.0} | N |
| Body | totalQuality | Int | 人脸评分阈值 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/face/analysis/detect' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'dataType=1' \
--data-urlencode 'image=' \
--data-urlencode 'operation=gender,age,glass'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": {
        "faces": [
            {
                "faceToken": "FACE0ae3ca2fHae8aI405cK8be6Hc15c9f151404",
                "location": { "x": 110.00002, "y": 15.000048, "width": 105.0, "height": 105.0 },
                "age": { "range": 5, "value": 68, "ageGroup": 4 },
                "gender": { "confidence": 0.708546, "value": "female" },
                "glass": { "confidence": 0.999958, "has": false, "value": 0 },
                "mask": { "confidence": 0.999992, "value": 1 },
                "beard": { "confidence": 0.989617, "value": 1 },
                "hat": { "confidence": 0.999862, "value": 1 },
                "smile": { "confidence": 0.906362, "value": 2 },
                "faceIQA": {
                    "pointsQuality": 0.897608,
                    "eyeDistance": 37.941441,
                    "colorful": 1.0,
                    "grayScale": 142,
                    "grayMean": 104.341087,
                    "grayVar": 60.181107,
                    "clearity": 0.4,
                    "posePitch": 14.971128,
                    "poseYaw": 9.000212,
                    "uncovered": 0.1,
                    "totalQuality": 0.362628
                },
                "faceMark": {
                    "leftEye": { "x": 143.75156, "y": 49.792847 },
                    "rightEye": { "x": 181.67386, "y": 50.9964 },
                    "leftMouth": { "x": 137.58595, "y": 92.46552 },
                    "rightMouth": { "x": 172.18892, "y": 96.35069 },
                    "noseTip": { "x": 155.31567, "y": 64.133995 }
                }
            }
        ]
    },
    "requestId": "sadfadsfasdfadsd111118987"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data.faces | Array | 检测出的人脸列表，如果没有检测出人脸则为空数组 |
| data.faces[].faceToken | String | 人脸唯一标识，一天内未注册集合内自动过期，如需再次注册/比对请重新检测 |
| data.faces[].location | Object | 人脸框坐标(x横坐标/y纵坐标/width宽/height高，单位px) |
| data.faces[].age | Object | 年龄(range波动范围/value年龄/ageGroup年龄区间:0小孩1少年2青年3中年4老年) |
| data.faces[].gender | Object | 性别(confidence置信度/value:female或male) |
| data.faces[].glass | Object | 是否戴眼镜(confidence置信度/value:1不带2戴眼镜3戴墨镜) |
| data.faces[].smile | Object | 表情(confidence置信度/value:1中性2高兴3惊讶4害怕5厌恶6难过7愤怒) |
| data.faces[].mask | Object | 口罩(confidence置信度/value:1不戴2戴) |
| data.faces[].hat | Object | 帽子(confidence置信度/value:1不戴2戴) |
| data.faces[].beard | Object | 胡须(confidence置信度/value:1无2有) |
| data.faces[].faceIQA | Object | 人脸评分（详见下方人脸评分表） |
| data.faces[].faceMark | Object | 人脸关键点（详见下方人脸关键点表） |

**人脸评分（faceIQA）**

| 字段名 | 类型 | 取值范围 | 描述 |
| --- | --- | --- | --- |
| pointsQuality | Float | [0-1] | 特征点置信度：数值越大特征点定位越准 |
| eyeDistance | Float | 实际像素点 | 瞳距：左右眼中心距离 |
| colorful | Float | [0,1] | 彩色置信度：数值越高彩色可能性越大，0表示黑白图，1表示彩图 |
| grayScale | Int | 1,2,...,256 | 灰阶数：全图Y通道灰阶数量，过曝和过暗都会导致灰阶数变少 |
| grayMean | Float | [0,255] | 灰度均值：白色区域越多灰度均值越大，黑色区域越多灰度均值越小 |
| grayVar | Float | [0,255] | 灰度均方差：阴阳脸会导致灰度方差变大 |
| clearity | Float | [0,1] | 清晰度：人脸的清晰程度，数值越大越清晰 |
| posePitch | Float | [-90,90] | 俯仰角：低头为负抬头为正，绝对值越大姿态越大，0表示正面 |
| poseYaw | Float | [-90,90] | 左右角：左转为负右转为正，绝对值越大姿态越大，0表示正面 |
| uncovered | Float | [0,1] | 可见性评分：即不遮挡评分，数值越小标识遮挡越严重，1表示完全未遮挡 |
| totalQuality | Float | [0,1] | 人脸总评分：综合所有评分项得到的人脸总评分，数值越大人脸质量越高 |

**人脸关键点（faceMark）**

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| leftEye | Object | 左眼位置（x横坐标，y纵坐标） |
| rightEye | Object | 右眼位置（x横坐标，y纵坐标） |
| leftMouth | Object | 左嘴角位置（x横坐标，y纵坐标） |
| rightMouth | Object | 右嘴角位置（x横坐标，y纵坐标） |
| noseTip | Object | 鼻尖位置（x横坐标，y纵坐标） |

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