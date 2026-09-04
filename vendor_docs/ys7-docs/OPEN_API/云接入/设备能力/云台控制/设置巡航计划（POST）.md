# 设置巡航计划（POST）

> 设置巡航计划（POST）

> 更新时间: 2026-07-20T14:36:46.000+08:00

> 文档ID: 5066 | 来源树: OPEN_API

---

## 设置巡航计划

- 接口功能：设置巡航的时间计划，指定在哪些时间段、哪些星期几执行自动巡航。开启计划后，设备将只在指定时段内进行巡航。
- 请求地址：`https://open.ys7.com/api/v3/device/ptz/cruise/timePlan`
- 请求方式：`POST`
- 能力集要求：`support_ptz_cruise_plan`

### 前置条件

> ⚠️ 本接口仅设置巡航的**执行时间段**，不涉及巡航路径。调用前需确保已完成以下步骤，否则设备不知道巡航目标位置，计划不会生效。

| 步骤 | 接口 | 说明 |
| --- | --- | --- |
| 1 | `POST /api/v3/device/ptz/cruise/preset/set` | 设置巡航预置点（将当前云台位置添加为巡航点，最多4个） |
| 2 | `POST /api/v3/device/ptz/cruise/preset/effect` | 生效巡航点位（激活已设置的N个点，参数 effectNum 范围[1,4]） |
| 3 | `POST /api/v3/device/ptz/cruise/auto/switch` | 开启自动巡航开关（enable=true） |
| 4 | **本接口** | （可选）设置巡航时间计划，指定什么时间段自动巡航 |

### 请求参数

| 参数位置 | 参数名 | 类型 | 描述 | 是否必选 |
| --- | --- | --- | --- | --- |
| header | accessToken | String | 用户令牌 | Y |
| header | deviceSerial | String | 设备序列号 | Y |
| body | enable | Int | 计划开关：`0`-关闭计划，`1`-开启计划 | Y |
| body | timerDefenceQos | String | 巡航时间计划JSON数组，格式见下方说明 | Y |

### timerDefenceQos 参数说明

JSON 数组格式，每个元素代表一个时间段计划：

```
[
    {"startTime": "08:00", "endTime": "12:00", "week": "0,1,2,3,4"},
    {"startTime": "14:00", "endTime": "18:00", "week": "0,1,2,3,4,5,6"}
]
```

| 子字段 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| startTime | String | Y | 巡航开始时间，格式 `HH:mm`，如 `"08:00"` |
| endTime | String | Y | 巡航结束时间，格式 `HH:mm`，如 `"18:00"`，必须晚于 startTime |
| week | String | Y | 生效星期，逗号分隔。0=周一，1=周二，2=周三，3=周四，4=周五，5=周六，6=周日。示例：`"0,1,2,3,4"` 表示工作日，`"0,1,2,3,4,5,6"` 表示每天 |

### 请求示例

```
curl --location --request POST 'https://open.ys7.com/api/v3/device/ptz/cruise/timePlan' \
--header 'accessToken: at.xxxxx' \
--header 'deviceSerial: BF7513110' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'enable=1' \
--data-urlencode 'timerDefenceQos=[{"startTime":"08:00","endTime":"12:00","week":"0,1,2,3,4"},{"startTime":"14:00","endTime":"18:00","week":"0,1,2,3,4,5,6"}]'
```

### 返回数据

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": null
}
```

### 返回码

| 返回码 | 返回消息 | 描述 |
| --- | --- | --- |
| 200 | 操作成功 | 操作成功 |
| 10001 | 参数异常 | timerDefenceQos 格式错误或 enable 格式非 0/1 |
| 20001 | 设备不存在 | 设备序列号不正确 |
| 20007 | 设备不在线 | 设备离线，无法下发计划 |
| 20010 | 设备能力集不支持 | 设备不支持巡航计划，需报备 `support_ptz_cruise_plan` 能力集 |
| 20015 | 设备异常 | 设备通信异常或指令执行失败 |

### 补充说明

- **本接口只管时间段**：巡航路径（走哪些点）由 `cruise/preset/set` + `cruise/preset/effect` 决定，本接口只控制"什么时候巡"。
- **计划覆盖**：每次调用会覆盖之前的计划，不是追加。