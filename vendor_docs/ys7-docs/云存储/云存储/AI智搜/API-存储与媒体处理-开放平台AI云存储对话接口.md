# API-存储与媒体处理-开放平台AI云存储对话接口

> API-存储与媒体处理-开放平台AI云存储对话接口

> 更新时间: 2026-05-25T16:36:56.000+08:00

> 文档ID: 5147 | 来源树: 云存储

---

# 开放平台AI云存储对话接口（POST）

> 开放平台AI云存储对话接口

---

## 接口URL

https://open.ys7.com/api/service/open/cloud/intelligent/storage/chat/completions

### **请求方式**

POST

## 请求

请求示例

```
curl --location 'https://open.ys7.com/api/service/open/cloud/intelligent/storage/chat/completions' \
--header 'Content-Type: application/json' \
--header 'accessToken: at.b9z3v3dgbg6x2q3k0ezfaoce6eoo8v7u' \
--data '{
    "messages":[
        {
            "content":"搜索有人的时刻", 
            "role":"user"
        }
    ],
    "deviceSerial":"889327292", 
    "localIndex":"1"
}'
```

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | N | 萤石开放API访问令牌, 萤石令牌 |  |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| messages | array<object> | Y | 对话的消息列表。 |  |
| -content | string | Y | 对话的内容 ，如输入  **请帮我找出今天的录像；对今天的视频进行总结； 请帮我找出今天的总结文案** |  |
| -role | string | N | 角色，默认为user |  |
| deviceSerial | string | Y | 设备序列号 |  |
| localIndex | string | N | 设备通道号,默认1 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | meta |  |
| -code | int | code |  |
| -message | string | message |  |
| -moreInfo | object | moreInfo |  |
| data | object | data |  |
| -object | string | object |  |
| -usage | object | usage |  |
| --prompt\_tokens | int | prompt\_tokens |  |
| --completion\_tokens | int | completion\_tokens |  |
| --total\_tokens | int | total\_tokens |  |
| -created | int | created |  |
| -model | string | model |  |
| -id | string | id |  |
| -choices | array<object> | choices |  |
| --message | object | message |  |
| ---content | object | content |  |
| ---role | string | role |  |
| ---searchVideoList | array<object> | searchVideoList |  |
| ----segId | string | segId |  |
| ----storageVersion | object | storageVersion |  |
| ----expireTime | int | expireTime |  |
| ----totalDay | object | totalDay |  |
| ----videoKeyword | string | videoKeyword |  |
| ----videoKeywordInt | int | videoKeywordInt |  |
| ----videoSummary | string | videoSummary |  |
| ----videoTags | string | videoTags |  |
| ----relatedType | int | relatedType |  |
| ----activePicTime | object | activePicTime |  |
| ----startTime | int | startTime |  |
| ----endTime | int | endTime |  |
| ----deviceSerial | string | deviceSerial |  |
| ----channelNo | int | channelNo |  |
| ----localType | object | localType |  |
| ----channelType | object | channelType |  |
| ----id | int | id |  |
| ----fileId | string | fileId |  |
| ----ownerId | string | ownerId |  |
| ----fileType | int | fileType |  |
| ----fileName | string | fileName |  |
| ----cloudType | int | cloudType |  |
| ----fileIndex | string | fileIndex |  |
| ----fileSize | int | fileSize |  |
| ----locked | int | locked |  |
| ----createTime | int | createTime |  |
| ----crypt | int | crypt |  |
| ----keyChecksum | string | keyChecksum |  |
| ----videoLong | int | videoLong |  |
| ----coverPic | string | coverPic |  |
| ----downloadPath | string | downloadPath |  |
| ----type | int | type |  |
| ----iStorageVersion | int | iStorageVersion |  |
| ----videoType | int | videoType |  |
| ---reasoning\_content | object | reasoning\_content |  |
| --delta | object | delta |  |
| --finish\_reason | string | finish\_reason |  |
| --index | int | index |  |
| --logprobs | object | logprobs |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "object": "chat.completion",
        "usage": {
            "prompt_tokens": 2229,
            "completion_tokens": 67,
            "total_tokens": 2296
        },
        "created": 1774600748,
        "model": "2",
        "id": "chatcmpl-ee12871f61be406c94d030f35572d83d",
        "choices": [
            {
                "message": {
                    "content": "为您找到了如下18条视频,女士走动11条,男士走动6条,女士吃东西1条",
                    "role": "assistant",
                    "searchVideoList": [
                        {
                            "segId": "20260327160000-889327332-1-00",
                            "storageVersion": 2,
                            "expireTime": 0,
                            "totalDay": 7,
                            "videoSummary": null,
                            "videoTags": null,
                            "videoKeyword": "女士走动",
                            "videoKeywordInt": 1,
                            "relatedType": null,
                            "activePicTime": 0,
                            "startTime": 1774600099000,
                            "endTime": 1774600115000,
                            "deviceSerial": "889327332",
                            "channelNo": 1,
                            "localType": null,
                            "channelType": null,
                            "id": 4969925423,
                            "fileId": "20260327160000-889327332-1-00",
                            "ownerId": "openteam",
                            "fileType": 1,
                            "fileName": "",
                            "cloudType": 4,
                            "fileIndex": "20260327160000-889327332-1-00",
                            "fileSize": 983263,
                            "locked": 0,
                            "createTime": 1774598405000,
                            "crypt": 13,
                            "keyChecksum": "",
                            "videoLong": 16000,
                            "coverPic": "https://alicloud.ys7.com:8089/api/cloud?method=download&fid=20260327160000-889327332-1-00&fileType=1&startTime=1774600104000&storageVersion=2&expireTime=20260403170005&ticket=RkJucTdEUnZ6UVJ5UXp5NXFBNGRaOEdiMWpzWVI2MUdTRWhwZlp4M0Z1VT0kMSQyMDI2MDQyNjE2MzkwOCRvcGVudGVhbQ==&bizCode=ALARM-PIC-SHARE",
                            "downloadPath": "alicloud.ys7.com:32723",
                            "type": 1,
                            "videoType": 2,
                            "istorageVersion": null
                        }
                    ],
                    "reasoning_content": null
                },
                "delta": null,
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null
            }
        ]
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 401 | 401 | 用户认证失败 |  |