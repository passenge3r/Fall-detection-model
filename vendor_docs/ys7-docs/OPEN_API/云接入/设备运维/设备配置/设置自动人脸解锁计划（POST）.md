# 设置自动人脸解锁计划（POST）

> 设置自动人脸解锁计划（POST）

> 更新时间: 2026-06-16T17:20:51.000+08:00

> 文档ID: 5103 | 来源树: OPEN_API

---

## 设置自动人脸解锁计划

- 接口功能

   设置自动人脸解锁计划

   获取计划类指令

   托管/子账号：支持

   权限：设备级Config

- 请求地址

`https://open.ys7.com/api/v3/device/timing/plan/set/batch`

- 请求方式

`POST`

- 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | deviceSerial | String | 设备序列号 | Y |
| header | accessToken | String | 萤石开放API访问令牌 | Y |
| body | channelNo | Int | 设备通道号，默认为0 | N |
| body | enable | Int | 计划是否启用：1-启用，0-不启用 | Y |
| body | timingPlanType | Int | 定时计划类型：19-自动识别开锁计划 | Y |
| body | mergeEnable | String | 是否需要合并重叠时间段：true-需要合并重叠时间段，false-不需要合并重叠时间段，默认为true | N |
| body | secondDayEnable | String | 是否支持跨天：true-支持跨天，false-不支持跨天，默认为false | N |
| body | timingPlanQos | String | 计划信息json，格式：[{"startTime":"00:00","endTime":"11:00","week":["0","1","2","3","4","5","6"],"eventArg":"0"},{"startTime":"20:00","endTime":"23:59","week":["3"],"eventArg":"0"}]；week重复周期：0-周一，1-周二，2-周三，3-周四，4-周五，5-周六，6-周日；eventArg：1-执行后停用，0-执行后不停用；计划数量不能超过10个 | Y |

- 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/timing/plan/set/batch' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: BG9859941' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'channelNo=1&enable=1&timingPlanType=19&mergeEnable=true&secondDayEnable=false&timingPlanQos=[{"startTime":"00:00","endTime":"11:00","week":["0","1","2","3","4","5","6"],"eventArg":"0"},{"startTime":"20:00","endTime":"23:59","week":["3"],"eventArg":"0"}]'
```

- 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    }
}
```

- 返回字段

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| meta | Object | meta信息 |
| meta.code | Int | 状态码 |
| meta.message | String | 状态消息 |
| meta.moreInfo | Object | 更多信息 |

- 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 10001 | 参数错误 | 参数错误 |
| 10002 | accessToken过期或异常 | accessToken过期或异常 |
| 10031 | 账号无权限访问此设备 | 账号无权限访问此设备 |
| 50000 | 服务异常 | 服务异常 |
| 20007 | 设备不在线 | 设备不在线 |
| 20002 | 设备不存在 | 设备不存在 |
| 20011 | 设备不支持或者设备异常 | 设备不支持或者设备异常 |
| 60020 | 设备不支持该信令 | 设备不支持该信令 |