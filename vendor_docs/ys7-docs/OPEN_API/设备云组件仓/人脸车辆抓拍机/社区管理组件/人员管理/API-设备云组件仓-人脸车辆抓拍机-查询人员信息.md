# API-设备云组件仓-人脸车辆抓拍机-查询人员信息

> 更新时间: 2026-06-30T12:10:19.000+08:00

> 文档ID: 1695 | 来源树: OPEN_API

---

# 查询人员信息（GET）

> 查询人员的具体信息，包括人员编号、姓名、性别、年龄、所属小区id、证件类型及证件号码、人脸图片、创建及修改时间、所属人员类别等信息

---

## 接口URL

https://open.ys7.com/api/service/devicekit/aicamera/people/info

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 用户访问令牌 | [accessToken获取接口](https://open.ys7.com/help/81) |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| id | string | Y | 人员id |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 服务响应信息 |  |
| -code | int | 服务响应状态码。参见响应码解释 |  |
| -message | string | 服务响应状态描述 |  |
| data | object | 服务响应 |  |
| -peopleId | string | 人员id |  |
| -peopleNo | string | 人员编号 |  |
| -updateTime | string | 修改时间 |  |
| -createTime | string | 创建时间 |  |
| -peopleName | string | 人员姓名 |  |
| -peopleAge | int | 年龄 |  |
| -peopleGender | int | 性别,0-女,1-男 |  |
| -communityId | string | 小区id |  |
| -faceImageUrl | string | 人脸图片url |  |
| -cardNo | string | 证件号码 |  |
| -cardType | int | 证件类型 1-普通卡,2-巡更卡,3-胁迫卡,4-超级卡,5-解除卡,6-应急管理卡 |  |
| -remarks | string | 备注 |  |
| -peopleCategoryIds | array<object> | 所属的人员类别集合 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "peopleId": "0372b4a5378741acbd887200a2ed4780",
        "peopleNo": "000010",
        "updateTime": "2023-05-08 10:36:28",
        "createTime": "2023-05-08 10:34:57",
        "peopleName": "张三Update22",
        "peopleAge": 29,
        "peopleGender": 1,
        "communityId": "21befc41c31f4811ac8cf297d1b7618f",
        "faceImageUrl": "",
        "cardNo": "4100000012",
        "cardType": 1,
        "remarks": "备注",
        "peopleCategoryIds": []
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 10001 | 10001 | 请求参数异常 |  |
| 49999 | 49999 | 数据异常 |  |
| 50000 | 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |