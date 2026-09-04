# API-设备云组件仓-门禁-基础功能-分页查询人员详细信息

> 更新时间: 2026-07-06T13:47:19.000+08:00

> 文档ID: 1108 | 来源树: OPEN_API

---

## 分页查询人员详细信息

- 接口功能

   该接口用于分页查询人员详细信息。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/queryByPage`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Query | pageStart | Long | 起始页码,取值范围[0,n],默认0 | N |
| Query | pageSize | Integer | 每页条数,默认10条,取值范围[1,100] | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/company/member/queryByPage?pageStart=0&pageSize=10' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": [
        {
            "empId": "0477b99e5ba842a8a512f47d13b017d0",
            "empName": "uio",
            "empAge": 89,
            "empNo": "1000023",
            "empGender": 1,
            "mobile": "17612889889",
            "orgId": null,
            "post": "政客",
            "memberType": 1,
            "memberGroup": "12",
            "companyMemberExtResp": null
        },
        {
            "empId": "a9282c14f99e4c7a98d90cfda1579b90",
            "empName": "工程用户3",
            "empAge": 25,
            "empNo": "202200033",
            "empGender": 0,
            "mobile": "18758781411",
            "orgId": "44747",
            "post": "11",
            "memberType": 0,
            "memberGroup": "003",
            "companyMemberExtResp": {
                "storageId": "6642846f597649a9bd826ff249043915",
                "faceToken": "FACE18c5fe081dd64425b04d9a1991774001",
                "empType": 2,
                "userVerifyMode": "face",
                "closeDelayEnable": "1",
                "maxOpenDoorTime": 12,
                "validEnable": "1",
                "beginTime": "2022-08-12 12:22:22",
                "endTime": "2023-08-12 12:22:22",
                "label": "请问",
                "remarks": "工程用户_one_111"
            }
        }
    ],
    "page": {
        "total": 14,
        "size": 10,
        "page": 0
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| page | Object | 分页信息 |
| size | Integer | 分页大小 |
| page.page | Integer | 页码 |
| total | Long | 总条数 |
| data | Object | 结果集合 |
| empId | String | 人员全局唯一id |
| empName | String | 人员姓名 |
| empAge | Integer | 年龄 |
| empNo | String | 工号 |
| empGender | Integer | 性别 |
| mobile | String | 联系方式 |
| orgId | String | 组织id |
| post | String | 职位 |
| memberType | Integer | 人员归属类型（0:企业内部成员；1：外部联系人）,默认内部成员 |
| memberGroup | String | 用户分组 |
| companyMemberExtResp | Object | 人员扩展信息 |
| storageId | String | 人脸图片下载唯一id |
| faceToken | String | 人脸唯一标识 |
| empType | Integer | 用户类型 1-管理员,2-普通用户,3-工程用户,4-来宾（访客）,5-黑名单人,默认普通用户,下发时会适配设备支持的类型 |
| userVerifyMode | String | 人员验证方式 |
| closeDelayEnable | String | 是否关门延迟:0或false-否,1或true-是,默认否 |
| maxOpenDoorTime | Integer | 最大验证次数,0为无次数限制 |
| validEnable | String | 最大验证次数,0为无次数限制 |
| beginTime | String | 有效期起始时间,yyyy-MM-dd HH:mm:ss |
| endTime | String | 有效期结束时间,yyyy-MM-dd HH:mm:ss |
| label | String | 人员标签 |
| remarks | String | 备注 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |