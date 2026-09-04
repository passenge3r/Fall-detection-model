# EZOpenSDK-android-告警消息.md

> EZOpenSDK-android-告警消息

> 更新时间: 2026-06-02T14:03:42.000+08:00

> 文档ID: 4170 | 来源树: SDK及示例

---

# 告警消息

有人体感应事件时，设备会记录存储该事件发生的时间、告警图片等信息。

## 告警消息开关

EZOpenSDK.java

```
/**
  * 设备设置布防状态，兼容A1和IPC设备的布防
  * 该接口为耗时操作，必须在线程中调用
  *
  * @param deviceSerial 设备序列号
  * @param defence      布防状态, 摄像机布防状态只有0和1，告警器有0:睡眠 8:在家 16:外出
  * @return 设备设置布防状态是否成功
  * @throws BaseException
  */
public boolean setDefence(String deviceSerial, EZConstants.EZDefenceStatus defence) throws BaseException;
```

## 告警消息列表获取

EZOpenSDK.java

```
/**
 * 获取告警信息列表
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号，为null时查询整个账户下的告警信息列表
 * @param pageIndex    查询页index，从0开始
 * @param pageSize     每页数量（建议20以内）
 * @param beginTime    搜索时间范围开始时间，开始时间和结束时间可以同时为空
 * @param endTime      搜索时间范围结束时间
 * @return EZAlarmInfo对象列表
 * @throws BaseException
 */
public List<EZAlarmInfo> getAlarmList(String deviceSerial, int pageIndex, int pageSize, Calendar beginTime, Calendar endTime) throws BaseException;
```

## 告警图片加载

获取到告警消息列表后，列表中EZAlarmInfo对象中的alarmPicUrl属性为告警图片，可使用如下api进行解密加载。

EZOpenSDK.java

```
/**
 * 解密数据，设备加密，该接口可以用于解密告警图片
 *
 * @param inputData  解密前数据
 * @param verifyCode 密码，设备加密时通常为设备验证码，平台加密时为平台返回的checkSum
 */
public byte[] decryptData(byte[] inputData, String verifyCode);

/**
 * 解密数据，该接口可以用于解密告警图片
 *
 * @param inputData  解密前数据
 * @param verifyCode 密码，设备加密时通常为设备验证码，平台加密时为平台返回的checkSum
 * @param cryptType  加密类型 1-设备加密 2-平台加密
 */
public byte[] decryptData(byte[] inputData, String verifyCode, int cryptType);
```

  

- alarmPicUrl属性类型是String，api入参类型为byte[]，调用前需先进行类型转换，详见demo工程中EZUtils.java类中的loadImage方法实现。
- encryptType入参对应EZAlarmInfo对象中的crypt属性值

## 未读消息数获取

EZOpenSDK.java

```
/**
 * 获取未读消息数
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 需要获取的设备序列号，为空时返回账户下所有设备的未读消息数
 * @param messageType  消息类型：EZMessageTypeAlarm 告警消息，EZMessageTypeLeave 留言消息
 * @return 未读消息数
 * @throws BaseException
 */
public int getUnreadMessageCount(String deviceSerial, EZMessageType messageType) throws BaseException;
```

## 设置告警消息为已读

EZOpenSDK.java

```
/**
 * 设置告警为已读
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param alarmIdList 告警信息Id数组(设置单条告警为已读时，数组中可以只有一个Id)
 * @param alarmStatus 告警状态,目前只支持设为已读功能 EZMessageStatusRead
 * @return true 表示成功， false 表示失败
 * @throws BaseException
 */
public boolean setAlarmStatus(List<String> alarmIdList, EZAlarmStatus alarmStatus) throws BaseException;
```

## 删除告警消息

EZOpenSDK.java

```
/**
 * 批量删除告警
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param alarmIdList 告警ID list
 * @return true 表示成功， false 表示失败
 * @throws BaseException
 */
public boolean deleteAlarm(List<String> alarmIdList) throws BaseException;
```