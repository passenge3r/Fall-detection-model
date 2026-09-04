# EZOpenSDK-harmony-预览-云台.md

> EZOpenSDK-harmony-预览-云台

> 更新时间: 2026-06-02T14:03:55.000+08:00

> 文档ID: 4193 | 来源树: SDK及示例

---

# 云台

云台，也称PTZ，是指对摄像机进行操控，比如云台转动、物理缩放、变焦等操作。
可以根据需要自动或手动调整方向和焦距，确保关键区域始终处于监控范围内。
该能力需摄像头本身支持PTZ能力。

### 云台控制

请先确认设备是否具备云台能力，可通过EzvizSupportKit.isSupportPTZ(deviceInfo.abilities)方法判断。

如果设备支持云台能力，**基线（线上）客户**推荐使用如下方法来控制云台

EZOpenSDK

```
/**
 * PTZ 控制接口，http+p2p双通道，设备响应先到达的指令，响应更快（推荐）
 *
 * @param deviceSerial 设备序列号
 * @param cameraNo     通道号
 * @param command      ptz控制命令
 * @param action       控制启动/停止
 * @param newSpeed     速度（0-7）
 * @param callback     回调，当error为空时表示操作成功
 */
static controlPTZMix(deviceSerial: string, cameraNo: number, command: EZPTZCommand, action: EZPTZAction, newSpeed: number, callback: (error: EZError) => void);
```

**私有云客户**推荐使用如下方法来控制云台（使用基础能力，私有云服务可能未支持其他扩展功能）

```
/**
 * PTZ 控制接口，支持8档速率，更细化
 * @param deviceSerial  设备序列号
 * @param cameraNo      通道号
 * @param command       ptz控制命令
 * @param action        控制启动/停止
 * @param newSpeed      云台速度：分为0-7共8档，数值越大，转速越快
 * @param callback      回调，当error为空时表示操作成功
 */
static controlPTZEx(deviceSerial: string, cameraNo: number, command: EZPTZCommand, action: EZPTZAction, newSpeed: number, callback: (error: EZError) => void);
```

### 云台角度

播放器EZPlayer设置setPlayerAdditionalInfoCallback回调后，会回调云台角度数据

```
@State ptzAngeleInfo: EZDevicePtzAngleInfo | null = null
  
private playerAdditionalInfoCallback: EZPlayerAdditionalInfoCallback = {
  /*
  * 设备云台角度数据回调
  */
  devicePtzAngleInfo: (info: EZDevicePtzAngleInfo) => {
    this.ptzAngeleInfo = info
  }
}
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
![云台角度UI](https://resource.eziot.com/group2/M00/00/FF/CtwQFmfSN9mAAFOSAAGxVoKRWmQ057.png)