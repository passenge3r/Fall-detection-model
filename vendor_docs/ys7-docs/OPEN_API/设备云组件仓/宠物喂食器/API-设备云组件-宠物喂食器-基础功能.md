# API-设备云组件-宠物喂食器-基础功能

> API-设备云组件-宠物喂食器-基础功能

> 更新时间: 2026-05-25T16:39:40.000+08:00

> 文档ID: 1591 | 来源树: OPEN_API

---

## 宠物喂食器 基础功能

本文档仅适用于设备型号：CS-PH-FD402系列宠物喂食器，其余型号不保证可用。

| 产品名称 | 功能点 | 子功能点 | 接口名称 | 操作 |
| --- | --- | --- | --- | --- |
| 宠物喂食器 | 余量检测 |  | 【消息】余量不足事件（FoodNotEnough） | [查看详情](https://open.ys7.com/help/1559) |
|  |  |  | 查询余粮不足（LackFood） | [查看详情](https://open.ys7.com/help/1560) |
|  | WIFI网络情况 |  | 查询网络状态（NetStatus） | [查看详情](https://open.ys7.com/help/1561) |
|  | 电量监测 |  | 查询电接接入状态（BatterIn） | [查看详情](https://open.ys7.com/help/1562) |
|  |  |  | 查询电池电量（BatteryPercentage） | [查看详情](https://open.ys7.com/help/1563) |
|  |  |  | 【消息】电量不足（LowPower） | [查看详情](https://open.ys7.com/help/1564) |
|  | 喂食相关 | 喂食计划 | 查询喂食计划（MealPlan） | [查看详情](https://open.ys7.com/help/1565) |
|  |  |  | 设置喂食计划（MealPlan） | [查看详情](https://open.ys7.com/help/1566) |
|  |  | 下一餐喂食信息 | 查询下一餐信息（NextMealInfo） | [查看详情](https://open.ys7.com/help/1567) |
|  |  |  | 查询取消下一餐 （CancelNextMeal） | [查看详情](https://open.ys7.com/help/1568) |
|  |  |  | 设置取消下一餐（CancelNextMeal） | [查看详情](https://open.ys7.com/help/1569) |
|  |  | 手动喂食 | 手动喂食（ManualFeed） | [查看详情](https://open.ys7.com/help/1570) |
|  |  | 喂食消息 | 【消息】喂食计划记录（TimerFeedLog） | [查看详情](https://open.ys7.com/help/1571) |
|  |  |  | 【消息】设备喂食记录（DeviceFeedLog） | [查看详情](https://open.ys7.com/help/1572) |
|  |  |  | 【消息】喂食成功通知（FeedSuccessNotify） | [查看详情](https://open.ys7.com/help/1592) |
|  |  | 出粮异常检测 | 查询出粮检测开关（OutputSensorSwitch） | [查看详情](https://open.ys7.com/help/1574) |
|  |  |  | 设置出粮检测开关（OutputSensorSwitch） | [查看详情](https://open.ys7.com/help/1575) |
|  |  |  | 【消息】没有粮食流出（NoFoodOut） | [查看详情](https://open.ys7.com/help/1576) |
|  |  |  | 查询没有粮食流出状态（NoFoodOutStatus） | [查看详情](https://open.ys7.com/help/1577) |
|  |  | 堵食检测 | 查询智能感应堵食开关（BlockSensorSwitch） | [查看详情](https://open.ys7.com/help/1578) |
|  |  |  | 设置智能感应堵食开关（BlockSensorSwitch） | [查看详情](https://open.ys7.com/help/1579) |
|  |  |  | 【消息】设备卡死通知（DeviceJamAlert） | [查看详情](https://open.ys7.com/help/1580) |
|  |  |  | 查询设备卡死状态（DeviceJamStatus） | [查看详情](https://open.ys7.com/help/1581) |
|  |  | 设备喂食按键设置 | 查询按键锁状态（KeyLockStatus） | [查看详情](https://open.ys7.com/help/1582) |
|  |  |  | 设置按键锁状态（KeyLockStatus） | [查看详情](https://open.ys7.com/help/1583) |
|  | 夜间模式设置 |  | 查询夜间模式（NightMode） | [查看详情](https://open.ys7.com/help/1584) |
|  |  |  | 设置夜间模式（NightMode） | [查看详情](https://open.ys7.com/help/1585) |
|  | 干燥剂状态 |  | 查询干燥剂使用信息（Desiccant） | [查看详情](https://open.ys7.com/help/1586) |
|  |  |  | 干燥剂复位（DesiccantReset） | [查看详情](https://open.ys7.com/help/1587) |
|  |  |  | 【消息】干燥剂更换提醒（DesiccantReplaceNotice） | [查看详情](https://open.ys7.com/help/1588) |
|  | 其余功能 |  | 查询机器时间（RealTime） | [查看详情](https://open.ys7.com/help/1589) |