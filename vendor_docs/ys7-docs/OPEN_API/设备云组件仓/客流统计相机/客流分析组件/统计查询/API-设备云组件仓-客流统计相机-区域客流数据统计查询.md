# API-设备云组件仓-客流统计相机-区域客流数据统计查询

>  

> 更新时间: 2026-06-30T11:48:50.000+08:00

> 文档ID: 1555 | 来源树: OPEN_API

---

## 区域客流数据统计查询

- 接口功能

   对指定区域的详细客流数据进行统计查询

- 请求地址

`https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/region`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 授权过程获取的access\_token | Y |
| body | regionTag | String | 绑定区域，最多32字符 | Y |
| body | startTime | String | 开始统计时间，格式yyyy-MM-dd HH:mm:ss | Y |
| body | endTime | String | 结束统计时间，格式yyyy-MM-dd HH:mm:ss | Y |
| body | id | String | 默认0 | N |
| body | pageSize | String | 查询的记录条数，默认100，最大每批1000条 | N |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/service/devicekit/peoplecounting/statistic/region' \
--header 'accessToken: at.xxxxx' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'regionTag=region01' \
--data-urlencode 'startTime=2024-01-01 00:00:00' \
--data-urlencode 'endTime=2024-01-01 23:59:59' \
--data-urlencode 'id=0' \
--data-urlencode 'pageSize=100'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    },
    "data": {
        "enter": 0,
        "exit": 0,
        "pass": 0,
        "gender": {
            "male": 0,
            "female": 0,
            "unknownGender": 0
        },
        "age": {
            "child": 0,
            "young": 0,
            "middle": 0,
            "old": 0,
            "teenager": 0,
            "prime": 0,
            "middleAged": 0,
            "unknownAge": 0
        },
        "mask": {
            "wearMask": 0,
            "noMask": 0,
            "unknownMask": 0
        },
        "glass": {
            "wear": 0,
            "wearSunglasses": 0,
            "noGlass": 0,
            "unknownGlass": 0
        }
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | 响应对象 |
| meta.code | Int | 错误码 |
| meta.message | String | 提示信息 |
| data | Object | 客流统计数据 |
| data.enter | Int | 进入人数 |
| data.exit | Int | 离开人数 |
| data.pass | Int | 通过人数 |
| data.gender | Object | 性别统计 |
| data.gender.male | Int | 男性 |
| data.gender.female | Int | 女性 |
| data.gender.unknownGender | Int | 未知性别 |
| data.age | Object | 年龄段统计 |
| data.age.child | Int | 少年 |
| data.age.young | Int | 青年 |
| data.age.middle | Int | 中年 |
| data.age.old | Int | 老年 |
| data.age.teenager | Int | 青少年 |
| data.age.prime | Int | 壮年 |
| data.age.middleAged | Int | 中老年 |
| data.age.unknownAge | Int | 未知年龄段 |
| data.mask | Object | 口罩统计 |
| data.mask.wearMask | Int | 戴口罩 |
| data.mask.noMask | Int | 未戴口罩 |
| data.mask.unknownMask | Int | 未知是否戴口罩 |
| data.glass | Object | 眼镜统计 |
| data.glass.wear | Int | 戴眼镜 |
| data.glass.wearSunglasses | Int | 戴墨镜 |
| data.glass.noGlass | Int | 不戴眼镜 |
| data.glass.unknownGlass | Int | 未知是否戴眼镜 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 请求成功 |
| 10001 | 参数错误 | 请检查请求参数 |
| 20015 | 设备不支持该功能 | 请确认设备是否支持该功能 |
| 49999 | 数据异常 | 数据异常 |
| 50000 | 服务器异常 | 可提交工单解决相关问题 |
| 404 | 资源不存在 | 请求的资源不存在 |