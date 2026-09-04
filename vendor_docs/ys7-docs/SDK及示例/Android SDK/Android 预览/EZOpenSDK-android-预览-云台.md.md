# EZOpenSDK-android-预览-云台.md

> EZOpenSDK-android-预览-云台

> 更新时间: 2026-06-02T14:03:37.000+08:00

> 文档ID: 4153 | 来源树: SDK及示例

---

# 云台

云台，也称PTZ，是指对摄像机进行操控，比如云台转动、物理缩放、变焦等操作。
可以根据需要自动或手动调整方向和焦距，确保关键区域始终处于监控范围内。
该能力需摄像头本身支持PTZ能力。

### 云台控制

请先确认设备是否具备云台能力，可通过EZDeviceInfo的isSupportPTZ方法判断。

如果设备支持云台能力，**基线（线上）客户**推荐使用如下方法来控制云台

EZOpenSDK

```
/**
* PTZ 通过p2p服务+http双通道控制云台，设备响应先到达的指令，响应更快（推荐）
* 该接口为耗时操作，必须在线程中调用
*
* @param deviceSerial 设备序列号
* @param cameraNo     通道号
* @param command      ptz控制命令
* @param action       控制启动/停止
* @param newSpeed     速度（0-7）
* @return 操作成功或者失败(返回失败错误码)
*/
public boolean controlPTZMix(final String deviceSerial, final int cameraNo, final EZPTZCommand command, final EZPTZAction action, final int newSpeed) throws BaseException;
```

**私有云客户**推荐使用如下方法来控制云台（使用基础能力，私有云服务可能未支持其他扩展功能）

```
/**
* PTZ 控制接口
* 该接口为耗时操作，必须在线程中调用
*
* @param deviceSerial 设备序列号
* @param cameraNo     通道号
* @param command      ptz控制命令
* @param action       控制启动/停止
* @param speed        速度（0-2）
* @return 操作成功或者失败(返回失败错误码)
*/
public boolean controlPTZ(String deviceSerial, int cameraNo, EZPTZCommand command, EZPTZAction action, int speed) throws BaseException;
```

### 云台角度

播放器EZPlayer设置handler通知回调后，会回调云台角度数据

```
@Override
public boolean handleMessage(Message msg) {
    switch (msg.what) {
        case EZRealPlayConstants.MSG_PTZ_GET_SUCCESS:// 云台角度获取成功
            handleDevicePtzAngleInfo(msg.obj);
            break;
    }
}

/**
 * 云台角度比例尺更新
 * @param obj
 */
private void handleDevicePtzAngleInfo (Object obj) {
    if (mPtzControlAngleViewHor.getVisibility() == View.VISIBLE || mPtzControlAngleViewVer.getVisibility() == View.VISIBLE) {
        EZDevicePtzAngleInfo info = (EZDevicePtzAngleInfo) obj;
        // do something
    }
}
```

  

EZDevicePtzAngleInfo对象属性如下

| 属性 | 释义 |
| --- | --- |
| horStartAng | 水平方向起点角度 |
| horEndAng | 水平方向终点角度 |
| horCurAng | 水平方向当前角度 |
| verStartAng | 垂直方向起点角度 |
| verEndAng | 垂直方向终点角度 |
| verCurAng | 垂直方向当前角度 |

根据如上属性，可以绘制云台角度比例尺，需自行实现，可参考demo工程。效果图如下  
![云台角度UI](https://resource.eziot.com/group1/M00/01/7B/CtwQE2em77iAPoQGAAKj38Mniss592.png)