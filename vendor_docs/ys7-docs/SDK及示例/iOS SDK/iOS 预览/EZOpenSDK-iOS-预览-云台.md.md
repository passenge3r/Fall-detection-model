# EZOpenSDK-iOS-预览-云台.md

> EZOpenSDK-iOS-预览-云台

> 更新时间: 2026-06-02T14:03:46.000+08:00

> 文档ID: 4079 | 来源树: SDK及示例

---

# 云台

云台，也称PTZ，是指对摄像机进行操控，比如云台转动、物理缩放、变焦等操作。
可以根据需要自动或手动调整方向和焦距，确保关键区域始终处于监控范围内。
该能力需摄像头本身支持PTZ能力。

### 云台控制

请先确认设备是否具备云台能力，可通过EZDeviceInfo的isSupportPTZ属性判断。

如果设备支持云台能力，**基线（线上）客户**推荐使用如下方法来控制云台

EZOpenSDK.h

```
/**
 *  PTZ 控制接口，http+p2p双通道，设备响应先到达的指令，响应更快（推荐）
 *
 *  @param deviceSerial 设备序列号
 *  @param cameraNo     通道号
 *  @param command      ptz控制命令
 *  @param action       控制启动/停止
 *  @param newSpeed     云台速度：分为0-7共8档，数值越大，转速越快
 *  @param resultBlock  回调block，当error为空时表示操作成功
 */
+ (NSURLSessionDataTask *)controlPTZMix:(NSString *)deviceSerial
                               cameraNo:(NSInteger)cameraNo
                                command:(EZPTZCommand)command
                                 action:(EZPTZAction)action
                               newSpeed:(NSInteger)newSpeed
                                 result:(void (^)(NSError *error))resultBlock;
```

**私有云客户**推荐使用如下方法来控制云台（使用基础能力，私有云服务可能未支持其他扩展功能）

```
/**
 *  PTZ 控制接口
 *
 *  @param deviceSerial 设备序列号
 *  @param cameraNo     通道号
 *  @param command      ptz控制命令
 *  @param action       控制启动/停止
 *  @param speed        云台速度：0-慢，1-适中，2-快
 *  @param resultBlock  回调block，当error为空时表示操作成功
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)controlPTZ:(NSString *)deviceSerial
                            cameraNo:(NSInteger)cameraNo
                             command:(EZPTZCommand)command
                              action:(EZPTZAction)action
                               speed:(NSInteger)speed
                              result:(void (^)(NSError * __nullable error))resultBlock;
```

### 云台角度

播放器EZPlayer设置代理后，会回调云台角度数据

```
/**
 * 设备云台角度数据回调
 *
 * @param player 播放器对象
 * @param info 私有数据
 */
- (void)player:(EZPlayer *)player didReceivedDevicePtzAngleInfo:(EZDevicePtzAngleInfo *)info;
```

  

EZDevicePtzAngleInfo对象属性如下

| 属性 | 释义 |
| --- | --- |
| horizontalStartAngle | 水平方向起点角度 |
| horizontalEndAngle | 水平方向终点角度 |
| horizontalCurrentAngle | 水平方向当前角度 |
| verticalStartAngle | 垂直方向起点角度 |
| verticalEndAngle | 垂直方向终点角度 |
| verticalCurrentAngle | 垂直方向当前角度 |

根据如上属性，可以绘制云台角度比例尺，需自行实现，可参考demo工程。效果图如下  
![云台角度UI](https://resource.eziot.com/group1/M00/01/7B/CtwQE2em77iAPoQGAAKj38Mniss592.png)