# API-设备云组件仓-人脸车辆抓拍机-新增人员额外信息

> 更新时间: 2026-06-30T12:10:07.000+08:00

> 文档ID: 1692 | 来源树: OPEN_API

---

## 新增人员额外信息

- 接口功能

   新增人员额外信息，可新增人员的人脸图片/人脸图片信息、证件类型、证件号码及备注

- 请求地址

`https://open.ys7.com/api/service/devicekit/aicamera/peopleExt/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | peopleId | String | 人员id | Y |
| body | faceImageUrl | String | 人脸图片URL，与base64FaceImageFile二选一透传即可 | Y |
| body | base64FaceImageFile | String | 人脸图片base64，与faceImageUrl二选一透传即可 | Y |
| body | cardType | Int | 证件类型，1-普通卡，2-巡更卡，3-胁迫卡，4-超级卡，5-解除卡，6-应急管理卡 | Y |
| body | cardNo | String | 证件号码 | Y |
| body | remarks | String | 备注 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/aicamera/peopleExt/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'peopleId=0372b4a5378741acbd887200a2ed4780' \
--data-urlencode 'faceImageUrl=https://example.com/face.jpg' \
--data-urlencode 'cardType=1' \
--data-urlencode 'cardNo=123456' \
--data-urlencode 'remarks=备注信息'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 服务响应信息 |
| meta.code | Int | 服务响应状态码，参见响应码解释 |
| meta.message | String | 服务响应状态描述 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 请求参数异常 | 请检查请求参数 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |