# EZOpenSDK-iOS-告警消息.md

> EZOpenSDK-iOS-告警消息

> 更新时间: 2026-06-02T14:03:51.000+08:00

> 文档ID: 4095 | 来源树: SDK及示例

---

# 告警消息

有人体感应事件时，设备会记录存储该事件发生的时间、告警图片等信息。

## 告警消息开关

EZOpenSDK.h

```
/**
 *  设备设置布防状态，兼容A1和IPC设备的布防
 *
 *  @param defence      布防状态, IPC布防状态只有0和1，A1有0:睡眠 8:在家 16:外出
 *  @param deviceSerial 设备序列号
 *  @param completion   回调block，error为空表示设置成功
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)setDefence:(EZDefenceStatus)defence
                        deviceSerial:(NSString *)deviceSerial
                          completion:(void (^)(NSError * __nullable error))completion;
```

## 告警消息列表获取

EZOpenSDK.h

```
/**
 *  根据设备序列号获取告警信息列表，设备序列号为nil时查询整个账户下的告警信息列表
 *
 *  @param deviceSerial 设备序列号
 *  @param pageIndex    分页当前页码（从0开始）
 *  @param pageSize     分页每页数量（建议20以内）
 *  @param beginTime    搜索时间范围开始时间
 *  @param endTime      搜索时间范围结束时间
 *  @param completion   回调block，正常时返回EZAlarmInfo的对象数据和查询时间范围内的告警个数的总数，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getAlarmList:(NSString *)deviceSerial
                             pageIndex:(NSInteger)pageIndex
                              pageSize:(NSInteger)pageSize
                             beginTime:(NSDate *)beginTime
                               endTime:(NSDate *)endTime
                            completion:(void (^)(NSArray *alarmList, NSInteger totalCount, NSError * __nullable error))completion;
```

## 告警图片加载

获取到告警消息列表后，列表中EZAlarmInfo对象中的alarmPicUrl属性为告警图片，可使用如下api进行解密加载。

EZOpenSDK.h

```
/**
 *  告警图片解密方法，设备加密
 *
 *  @param data       需要解密的数据
 *  @param verifyCode 设备验证码
 *
 *  @return 解密的NSData对象，如果返回的数据是空的，请检查密码是否正确或者传入的数据是否正确。
 */
+ (NSData *)decryptData:(NSData *)data verifyCode:(NSString *)verifyCode;

/**
 *  告警图片解密方法，需指定设备加密 或 平台加密
 *
 *  @param data       需要解密的数据
 *  @param verifyCode 设备验证码
 *  @param type 1:设备加密；2：平台加密
 *
 *  @return 解密的NSData对象，如果返回的数据是空的，请检查密码是否正确或者传入的数据是否正确。
 */
+ (NSData *)decryptData:(NSData *)data verifyCode:(NSString *)verifyCode encryptType:(NSInteger)type;
```

  

- alarmPicUrl属性类型是NSString，api入参类型为NSData，调用前需先进行类型转换，详见demo工程中的MessageListCell.m类实现。
- encryptType入参对应EZAlarmInfo对象中的crypt属性值

## 未读消息数获取

EZOpenSDK.h

```
/**
 *  根据设备序列号获取未读消息数，设备序列号为空时获取所有设备的未读消息数
 *
 *  @param deviceSerial 需要获取的设备序列号，为空时返回账户下所有设备的未读消息数
 *  @param type         消息类型：EZMessageTypeAlarm 告警消息（1），EZMessageTypeLeave 留言消息（2）
 *  @param completion   回调block，正常时返回未读数量，错误时返回错误码
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)getUnreadMessageCount:(NSString *)deviceSerial
                                    messageType:(EZMessageType)type
                                     completion:(void (^)(NSInteger count, NSError * __nullable error))completion;
```

## 设置告警消息为已读

EZOpenSDK.h

```
/**
 *  设置告警信息为已读接口
 *
 *  @param alarmIds   告警信息Id数组(可以只有一个Id)，最多为10个id,否则会报错
 *  @param status     告警消息状态
 *  @param completion 回调block，error为空时表示设置成功
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)setAlarmStatus:(NSArray *)alarmIds
                             alarmStatus:(EZMessageStatus)status
                              completion:(void (^)(NSError * __nullable error))completion;
```

## 删除告警消息

EZOpenSDK.h

```
/**
 *  根据alarmId删除告警信息接口
 *
 *  @param alarmIds   告警信息Id数组(可以只有一个Id)，最多为10个Id，否则会报错
 *  @param completion 回调block，error为空时表示删除成功
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)deleteAlarm:(NSArray *)alarmIds
                           completion:(void (^)(NSError * __nullable error))completion;
```