# API-设备云组件仓-门禁-基础功能-分页查询权限记录

> 更新时间: 2026-07-06T13:47:53.000+08:00

> 文档ID: 1119 | 来源树: OPEN_API

---

## 分页查询权限记录

- 接口功能

   该接口用于分页查询权限记录：1、人员工号为空、设备不为空，查询指定设备的下发人员记录；2、人员号不为空、设备为空，查询指定人员下发的所有记录；3、都不为空，查询指定设备和人员的下发记录；4、全部为空，查询开发者id下所有的记录。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/query/authority/records`

- 请求方式

`GET`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Query | empNo | String | 人员工号 | N |
| Query | deviceSerial | String | 设备序列号 | N |
| Query | pageStart | Long | 页码,默认0 | N |
| Query | pageSize | Integer | 条数[0,100],默认10 | N |

- 请求示例

```
curl --location --request GET 'https://open.ys7.com/api/v3/device/company/member/query/authority/records?empNo=&deviceSerial=&pageStart=&pageSize=' \
--header 'accessToken: at.xxxxx'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": [
        {
            "empId": "cc669311040744b1b4f0f99821ae248",
            "deviceSerial": "J49882687",
            "empName": "管理员",
            "empNo": "202200011",
            "doorNo": "1",
            "authorityStatus": 1,
            "storageId": "8e4233e23d294f104e3d7043c688b4b",
            "empType": 1,
            "validEnable": "1",
            "closeDelayEnable": "false",
            "maxOpenDoorTime": 0,
            "userVerifyMode": "face",
            "beginTime": "2022-06-22 10:00:00",
            "endTime": "2024-12-29 00:23:00",
            "updateTime": 1662190262000,
            "createTime": 1662030177000
        }
    ],
    "page": {
        "total": 3,
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
| total | Integer | 总条数 |
| size | Integer | 页面大小 |
| page.page | Boolean | 页码 |
| resultList | Object | 结果集合 |
| empId | String | 人员全局唯一id |
| deviceSerial | String | 设备序列号 |
| empName | String | 人员姓名 |
| empNo | String | 工号 |
| doorNo | String | 门权限 |
| authorityStatus | Integer | 下发状态0-失败,1成功 |
| storageId | String | 人脸图片下载唯一id |
| empType | Integer | 用户类型 1-管理员,2-普通用户,3-工程用户,4-来宾（访客）,5-黑名单人,默认普通用户,下发时会适配设备支持的类型 |
| userVerifyMode | String | 人员验证方式 |
| closeDelayEnable | String | 是否关门延迟:0或false-否,1或true-是,默认否 |
| maxOpenDoorTime | Integer | 最大验证次数,0为无次数限制 |
| validEnable | String | 有效期使能,0-使能,1-不使能 |
| beginTime | String | 有效期起始时间,yyyy-MM-dd HH:mm:ss |
| endTime | String | 有效期结束时间,yyyy-MM-dd HH:mm:ss |
| updateTime | String | 更新时间 |
| createTime | String | 创建时间 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |