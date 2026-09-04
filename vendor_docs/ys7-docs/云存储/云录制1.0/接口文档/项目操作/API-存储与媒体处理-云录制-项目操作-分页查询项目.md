# API-存储与媒体处理-云录制-项目操作-分页查询项目

> 更新时间: 2026-07-01T18:45:16.000+08:00

> 文档ID: 1364 | 来源树: 云存储

---

## 分页查询项目

- 接口功能

   分页查询项目。

- 请求地址

`https://open.ys7.com/api/open/cloud/v1/projects`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Query | accessToken | String | 用户令牌 | Y |
| Query | pageNumber | Int | 分页查询页码，以0开始，默认0 | N |
| Query | pageSize | Int | 分页查询大小，取值范围[1,20]，默认10 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/open/cloud/v1/projects?accessToken=at.xxxxx&pageNumber=0&pageSize=3'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "projectId": "007",
            "projectName": "测试007",
            "expireDays": 0,
            "totalSize": 0,
            "providerType": "ali",
            "storageType": 1,
            "totalFlow": 0,
            "flowLimit": -1,
            "permission": 0,
            "projectTag": "",
            "createTime": "2021-04-30T10:42:45",
            "updateTime": "2021-04-30T10:42:45",
            "bizType": ""
        },
        {
            "projectId": "1",
            "projectName": "曹诗雨测试",
            "expireDays": 7,
            "totalSize": 0,
            "providerType": "ali",
            "storageType": 1,
            "totalFlow": 21716,
            "flowLimit": -1,
            "permission": 0,
            "projectTag": null,
            "createTime": "2022-06-01T10:47:53",
            "updateTime": "2022-11-25T16:15:02",
            "bizType": ""
        },
        {
            "projectId": "111",
            "projectName": "bao",
            "expireDays": 30,
            "totalSize": 22161499,
            "providerType": "ali",
            "storageType": 1,
            "totalFlow": 101285175,
            "flowLimit": -1,
            "permission": 0,
            "projectTag": null,
            "createTime": "2022-12-16T14:15:37",
            "updateTime": "2023-01-13T00:21:42",
            "bizType": ""
        }
    ]
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 返回状态码及信息 |
| data | Array | 项目信息列表 |
| data[].projectId | String | 项目ID |
| data[].projectName | String | 项目名称 |
| data[].expireDays | Int | 项目文件过期天数，0表示不过期 |
| data[].totalSize | Long | 项目文件总大小，单位：字节 |
| data[].providerType | String | 存储服务提供商类型 |
| data[].storageType | Int | 项目存储类型 1-标准存储 2-存档存储 |
| data[].totalFlow | Long | 项目已使用下载流量，单位：字节 |
| data[].flowLimit | Long | 项目下载流量限制，单位：字节，-1代表不限制 |
| data[].permission | Int | 项目权限 |
| data[].projectTag | String | 项目标签 |
| data[].createTime | String | 创建时间 |
| data[].updateTime | String | 更新时间 |
| data[].bizType | String | 业务类型 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 400 | 请求参数错误 | 请检查参数传递 |
| 403 | 权限问题 | 无权限操作，检查权限 |
| 404 | 资源不存在 | 检查资源是否存在 |
| 500 | 服务内部问题 | 请检查传递参数进行重试，如还是服务错误请联系客服 |