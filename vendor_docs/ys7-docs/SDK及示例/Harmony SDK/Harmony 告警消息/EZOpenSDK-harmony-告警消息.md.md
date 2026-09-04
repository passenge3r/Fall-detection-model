# EZOpenSDK-harmony-告警消息.md

> EZOpenSDK-harmony-告警消息

> 更新时间: 2026-06-02T14:03:59.000+08:00

> 文档ID: 4210 | 来源树: SDK及示例

---

# 告警消息

有人体感应事件时，设备会记录存储该事件发生的时间、告警图片等信息。

## 告警消息开关

EZOpenSDK.ets

```
/**
 * 布撤防接口
 * @param isDefence    布撤防状态
 * @param deviceSerial 设备序列号
 * @param callback     回调，无error表示设置成功
 */
static setDefence(isDefence: boolean, deviceSerial: string, callback: (error: EZError) => void);
```

## 告警消息列表获取

EZOpenSDK.ets

```
/**
 * 根据设备序列号获取告警信息列表，设备序列号为nil时查询整个账户下的告警信息列表
 * @param deviceSerial 设备序列号
 * @param pageIndex    分页当前页码（从0开始）
 * @param pageSize     分页每页数量（建议20以内）
 * @param beginTime    搜索时间范围开始时间（可以为空，nil代表为空）
 * @param endTime      搜索时间范围结束时间（可以为空，nil代表为空）
 * @param callback     回调，正常时返回EZAlarmInfo的对象数据和查询时间范围内的告警个数的总数，错误时返回错误码
 */
static getAlarmList(deviceSerial: string, pageIndex: number, pageSize: number, beginTime: Date, endTime: Date,
  callback: (alarmList: Array<EZAlarmInfo>, totalCount: number, error: EZError) => void);
```

## 告警图片加载

获取到告警消息列表后，列表中EZAlarmInfo对象中的alarmPicUrl属性为告警图片，可使用如下api进行解密加载。

EZOpenSDK.ets

```
/**
 * 解密图片
 * @param imageUrl     需要解密的图片url
 * @param verifyCode  设备验证码
 * @param cryptType   1:设备加密；2：平台加密
 * @param callback    回调解密的PixelMap对象，如果返回的数据是空的，请检查密码是否正确或者传入的数据是否正确。
 */
static async decryptData(imageUrl: string, verifyCode: string, cryptType: number,
  callback: (image: image.PixelMap | null, error: EZError | null) => void);
```

  

- 详见demo工程中MessageListCell.ets类实现。
- encryptType入参对应EZAlarmInfo对象中的crypt属性值

## 未读消息数获取

EZOpenSDK.ets

```
/**
 * 根据设备序列号获取未读消息数，设备序列号为空时获取所有设备的未读消息数
 * @param alarmIds    告警信息Id数组(可以只有一个Id)，最多为10个id,否则会报错
 * @param messageType 消息类型：EZMessageTypeAlarm 告警消息（1），EZMessageTypeLeave 留言消息（2）
 * @param callback    回调，error为空时表示设置成功
 */
static getUnreadMessageCount(deviceSerial: string, messageType: number,
  callback: (count: number, error: EZError) => void);
```

## 设置告警消息为已读

EZOpenSDK.ets

```
/**
 * 设置告警信息为已读接口
 * @param alarmIds   告警信息Id数组(可以只有一个Id)，最多为10个id,否则会报错
 * @param status     告警消息状态
 * @param callback   回调，error为空时表示设置成功
 */
static setAlarmStatus(alarmIds: Array<string>, alarmStatus: number, callback: (error: EZError) => void);
```

## 删除告警消息

EZOpenSDK.ets

```
/**
 * 根据alarmId删除告警信息接口
 * @param alarmIds   告警信息Id数组(可以只有一个Id)，最多为10个id,否则会报错
 * @param callback   回调，error为空时表示设置成功
 */
static deleteAlarm(alarmIds: Array<string>, callback: (error: EZError) => void);
```