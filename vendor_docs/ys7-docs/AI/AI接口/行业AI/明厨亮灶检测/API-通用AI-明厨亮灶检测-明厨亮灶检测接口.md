# API-通用AI-明厨亮灶检测-明厨亮灶检测接口

> 更新时间: 2026-07-01T18:44:54.000+08:00

> 文档ID: 1340 | 来源树: AI

---

## 明厨亮灶检测接口

- 接口功能

   检测画面中的每个人员的头部是否佩戴厨师帽、是否穿厨师服、是否戴口罩、检测画面中是否有老鼠，输出目标属性和类别。目前只能将白色厨师帽识别为厨师帽，主体颜色为白色的厨师服进行识别，其他颜色的厨师帽和厨师服无法确保正确识别。子账户token请求所需最小权限：无。

- 请求地址

`https://open.ys7.com/api/lapp/intelligence/reasoning/5A9D1AB536854B8AAF7224C2508571A1`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | accessToken | String | 授权过程获取的accessToken | Y |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | dataType | Int | 数据类型(0:图片URL; 1:base64编码的二进制图片数据) | Y |
| Body | image | String | 待分析的图片数据 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/intelligence/reasoning/5A9D1AB536854B8AAF7224C2508571A1' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'dataType=0' \
--data-urlencode 'image=https://xxx.xxx.com/xxx.jpg'
```

- 返回数据

```
{
    "msg": "操作成功",
    "code": "200",
    "data": [
        {
            "errorcode": "0",
            "width": "944",
            "height": "574",
            "frameNum": 0,
            "timeStamp": 0,
            "aitype": 0,
            "targets": [
                {
                    "obj": {
                        "id": 0,
                        "modelID": "00012021102901006det_kitchenRule",
                        "rect": {
                            "w": "0.046094",
                            "x": "0.808594",
                            "h": "0.081944",
                            "y": "0.519444"
                        },
                        "confidence": 956,
                        "tag": "戴口罩",
                        "type": 1
                    },
                    "properties": null
                },
                {
                    "obj": {
                        "id": 2,
                        "modelID": "00012021102901006det_kitchenRule",
                        "rect": {
                            "w": "0.039844",
                            "x": "0.400781",
                            "h": "0.088889",
                            "y": "0.462500"
                        },
                        "confidence": 927,
                        "tag": "戴厨师帽",
                        "type": 3
                    },
                    "properties": null
                },
                {
                    "obj": {
                        "id": 6,
                        "modelID": "00012021102901006det_kitchenRule",
                        "rect": {
                            "w": "0.100000",
                            "x": "0.306250",
                            "h": "0.241667",
                            "y": "0.509722"
                        },
                        "confidence": 994,
                        "tag": "穿厨师服",
                        "type": 5
                    },
                    "properties": null
                },
                {
                    "obj": {
                        "id": 10,
                        "modelID": "00012021102901006det_kitchenRule",
                        "rect": {
                            "w": "0.221875",
                            "x": "0.710156",
                            "h": "0.402778",
                            "y": "0.472222"
                        },
                        "confidence": 329,
                        "tag": "未穿厨师服",
                        "type": 6
                    },
                    "properties": null
                }
            ]
        }
    ],
    "requestId": "f2dcb6b315fb466cb2a95d82ebf02f19"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码，200表示成功 |
| msg | String | 返回信息 |
| requestId | String | 请求ID |
| data | Array | 检测结果列表 |
| data[].errorcode | Int | 单次任务推理结果 |
| data[].width | Int | 单帧图片宽度 |
| data[].height | Int | 单帧图片高度 |
| data[].frameNum | Int | 帧号 |
| data[].timeStamp | Int | 时间戳 |
| data[].aitype | Int | 检测算法是1000，分类算法是1001 |
| data[].targets | Array | 目标列表 |
| data[].targets[].obj | Object | 模型目标内容 |
| data[].targets[].obj.id | Int | 目标id |
| data[].targets[].obj.modelID | String | 模型id |
| data[].targets[].obj.rect | Object | 矩形框（w宽/x横坐标/h高/y纵坐标，归一化比例） |
| data[].targets[].obj.confidence | Int | 检测结果置信度 |
| data[].targets[].obj.tag | String | 目标类型 |
| data[].targets[].obj.type | Int | 目标类型枚举值(1对应戴口罩，2对应未戴口罩，3对应戴厨师帽，4对应未戴厨师帽，5对应穿厨师服，6对应未穿厨师服，7对应老鼠) |
| data[].targets[].properties | Object | 目标属性 |

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
| 60405 | 图片地址错误 | 图片地址错误 |
| 60507 | 服务超时 | 服务超时 |
| 60508 | 服务器繁忙 | 服务器繁忙 |
| 60509 | 该功能暂时不支持 | 该功能暂时不支持 |