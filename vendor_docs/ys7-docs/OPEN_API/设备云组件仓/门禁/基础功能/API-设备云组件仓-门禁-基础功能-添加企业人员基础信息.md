# API-设备云组件仓-门禁-基础功能-添加企业人员基础信息

> 更新时间: 2026-07-06T13:46:54.000+08:00

> 文档ID: 1095 | 来源树: OPEN_API

---

## 添加企业人员基础信息

- 接口功能

   该接口用于添加开发者账号下的人员基础信息。本文档仅适用于设备型号 DS-K1T系列的人脸门禁，其余型号不保证可用。

- 请求地址

`https://open.ys7.com/api/v3/device/company/member/add`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Header | accessToken | String | 用户访问令牌，[accessToken获取方法](https://open.ys7.com/doc/zh/book/index/user.html) | Y |
| Body | empName | String | 人员姓名格式:32位以内的中文、英文、下划线及'.'组成的字符串 | Y |
| Body | empAge | Integer | 人员年龄，最大不超过150 | Y |
| Body | empNo | String | 人员工号:32位以内的数字或英文字母组成的字符串 | Y |
| Body | empGender | Integer | 人员性别:0-女，1-男 | Y |
| Body | mobile | String | 手机号 | Y |
| Body | orgId | String | 组织id,12位以内的数字 | N |
| Body | post | String | 职位:12位以内的中文,英文或者数字,下划线组成的字符串 | N |
| Body | memberType | Integer | 人员类型标识:0-企业内部成员，1-外部联系人,默认0 | N |
| Body | memberGroup | String | 所属分组,12位以内的数字或英文字母组成的字符串 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/company/member/add' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'empName=XX' \
--data-urlencode 'empAge=28' \
--data-urlencode 'empNo=280' \
--data-urlencode 'empGender=1' \
--data-urlencode 'mobile=XXXXX' \
--data-urlencode 'orgId=1100' \
--data-urlencode 'post=测试' \
--data-urlencode 'memberType=0' \
--data-urlencode 'memberGroup=abc'
```

- 返回数据

```
{
    "msg": "操作成功!",
    "code": "200",
    "data": {
        "empId": "9e52b0cc95f24e0c95fdd4501695a309"
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 返回码 |
| msg | String | 返回信息 |
| empId | String | 人员全局唯一id |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功! | 请求成功 |