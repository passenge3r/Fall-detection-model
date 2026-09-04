# OPEN API-萤石用户连接-设备托管-集成开发回调-刷新授权token

> OPEN API-萤石用户连接-设备托管-集成开发回调-刷新授权token

> 更新时间: 2026-05-25T16:43:53.000+08:00

> 文档ID: 821 | 来源树: OPEN_API

---

## 刷新授权token

- 接口功能 该接口主要是用来刷新过期的设备托管 token
- 请求地址 https://openauth.ys7.com/oauth/token/refreshToken
- 请求方式 GET
- 请求参数 Key 类型 必选 Head refresh\_token String Y 授权用户刷新 token client\_id String Y 开发者 appKey open\_id String Y 授权码 grant\_type String Y 该参数请填写字符串”refresh\_token” access\_token String Y 开发者 token
- HTTP 请求报文 POST /oauth/token/refreshToken HTTP/1.1 Host: openauth.ys7.com Content-Type: application/x-www-form-urlencoded refresh\_token =dr.dunwhxt2azk02hcn7phqygsybbw0wv6p& client\_id =dshfksdhf&open\_id=asjdkasd&grant\_type= refresh\_token&access\_token=at.sadasdasd
- 返回信息 { "data": { "access\_token": "du.2svbvjn82ycx5weh54slfbuebmn6im7o-3np7vpbklx-0zxzdhk-fkzgcpc84", "expires\_in": 1541656437269, "refresh\_token": "rt.99oz60qc8hn1jfwp9ml4nttid9u3w9h0-8s2wqprgxs-0zhci16-sssvtcmdk", "openId": "b4a3edff6af84a71b8a12912094359b5", }, "code": "200", "msg": "操作成功" }
- 返回字段说明 字段名 类型 access\_token String 返回授权托管 token expires\_in Long 该 token 的过期时间, 单位为毫秒数 refresh\_token String 该 token 用来刷新授权托管 token openId String 授权码
- 返回码 code 提示信息 200 成功 10001 参数错误 10017 client\_id 不存在 10005 client\_id 异常 70003 refresh\_token 不存在 70004 refresh\_token 已过期 70005 refresh\_token 与 client\_id 不匹配 70006 refresh\_token 与 open\_id 不匹配