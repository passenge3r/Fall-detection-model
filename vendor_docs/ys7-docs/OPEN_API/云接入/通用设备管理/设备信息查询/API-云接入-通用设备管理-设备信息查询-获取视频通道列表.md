# API-云接入-通用设备管理-设备信息查询-获取视频通道列表

> 更新时间: 2026-07-09T18:39:32.000+08:00

> 文档ID: 674 | 来源树: OPEN_API

---

## 获取视频通道列表

- 接口功能

   获取监控点列表 子账户token请求所需最小权限："Permission":"Get" "Resource":"dev:序列号"

- 请求地址

`https://open.ys7.com/api/lapp/camera/list`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| Header | Content-Type | String | application/x-www-form-urlencoded | Y |
| Body | accessToken | String | 授权过程获取的access\_token | Y |
| Body | pageStart | Int | 分页起始页，从0开始 | N |
| Body | pageSize | Int | 分页大小，默认为10，最大为50 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/lapp/camera/list' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'accessToken=at.xxxxx' \
--data-urlencode 'pageStart=0' \
--data-urlencode 'pageSize=2'
```

- 返回数据

```
{
    "page": {
        "total": 2,
        "page": 0,
        "size": 10
    },
    "data": [
        {
            "deviceSerial": "427734444",
            "channelNo": 1,
            "channelName": "C1(427734444)",
            "status": 1,
            "isShared": "1",
            "picUrl": "http://img.ys7.com/group1/M00/02/B4/CmGCA1dRGyuAdJ_RAABJBCB_Re4796.jpg",
            "isEncrypt": 1,
            "videoLevel": 2,
            "permission": -1
        },
        {
            "deviceSerial": "519544444",
            "channelNo": 1,
            "channelName": "C2C(519544444)",
            "status": 0,
            "isShared": "2",
            "picUrl": "https://i.ys7.com/assets/imgs/public/homeDevice.jpeg",
            "isEncrypt": 0,
            "videoLevel": 2,
            "permission": -1
        }
    ],
    "code": "200",
    "msg": "操作成功!"
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| deviceSerial | String | 设备序列号 |
| channelNo | Int | 通道号 |
| channelName | String | 通道名 |
| status | Int | 在线状态：0-不在线，1-在线（该字段已废弃） |
| picUrl | String | 图片地址（大图），若在萤石客户端设置封面则返回封面图片，未设置则返回默认图片 |
| isEncrypt | Int | 是否加密，0：不加密，1：加密 |
| videoLevel | Int | 视频质量：0-流畅，1-均衡，2-高清，3-超清 |
| permission | Int | 分享设备的权限字段 |
| isAdd | Int | 0:隐藏，1:显示 |

   permission权限解析方式：判断是否有该权限样例代码：

```
public boolean hasThisPermission(int permission) {
        return (this.code & permission) == this.code;
    }
```

   code类型：预览权限：1，回放权限：1<<1，告警权限：1<<2，对讲权限：1<<3 （<<表示位或）

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 参数为空或格式不正确 |
| 10002 | accessToken异常或过期 | 重新获取accessToken |
| 10005 | appKey异常 | appKey被冻结 |
| 20002 | 设备不存在 |  |
| 20014 | deviceSerial不合法 |  |
| 20018 | 该用户不拥有该设备 | 检查设备是否属于当前账户 |
| 49999 | 数据异常 | 接口调用异常 |