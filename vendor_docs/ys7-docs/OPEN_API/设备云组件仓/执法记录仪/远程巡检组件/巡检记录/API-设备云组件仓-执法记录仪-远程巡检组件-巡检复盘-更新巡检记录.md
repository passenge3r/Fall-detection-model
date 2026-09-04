# API-设备云组件仓-执法记录仪-远程巡检组件-巡检复盘-更新巡检记录

> API-设备云组件仓-执法记录仪-远程巡检组件-巡检复盘-更新巡检记录

> 更新时间: 2026-05-25T16:38:46.000+08:00

> 文档ID: 746 | 来源树: OPEN_API

---

# 更新巡检记录（PUT）

> 对巡检记录信息进行更新。

---

## 接口URL

https://open.ys7.comdevicekit/bodycamera/inspect

## 请求

### Header

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| accessToken | string | Y | 用户访问令牌 | [accessToken获取接口](https://open.ys7.com/help/81) |

### body

| 名称 | 类型 | 必填 | 描述 | 示例指及参考API |
| --- | --- | --- | --- | --- |
| inspectRecordId | int | Y | 巡检记录ID |  |
| inspectDistrict | string | N | 巡检区域。巡检记录存储时，将默认读取设备所属区域作为巡检区域，作为此次巡检记录巡检的区域，例如巡检A工地。不超过60个字符 |  |
| inspectPerson | string | N | 巡检人员。不超过60个字符。 |  |
| remoteInspectPerson | string | N | 远程巡检人员。不超过60个字符。 |  |
| inspectStatus | int | N | 0-巡检中 1-巡检完成（仅用于异常场景下纠正设备当前状态） |  |
| remoteInspectStatus | int | N | 0-无远程巡检 1-有远程巡检 |  |
| inspectName | string | N | 巡检名称 |  |

## 响应

### 返回数据

| 名称 | 类型 | 描述 | 示例 |
| --- | --- | --- | --- |
| meta | object | 服务响应信息 |  |
| -code | int | 错误码 |  |
| -message | string | 错误描述 |  |

### 返回示例

```
{
    "meta": {
        "code": 200,
        "message": "操作成功"
    }
}
```

### 错误码

| 状态码 | 错误码 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| 200 | 200 | 操作成功 |  |
| 10001 | 10001 | 参数错误 |  |
| 49999 | 49999 | 数据异常 |  |
| 50000 | 50000 | 服务器异常 | 可提交“[工单](https://open.ys7.com/console/work.html)”解决相关问题 |
| 404 | 404 | 资源不存在 |  |