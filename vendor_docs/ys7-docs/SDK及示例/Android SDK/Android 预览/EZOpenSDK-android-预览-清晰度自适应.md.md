# EZOpenSDK-android-预览-清晰度自适应.md

> EZOpenSDK-android-预览-清晰度自适应

> 更新时间: 2026-06-04T10:22:06.000+08:00

> 文档ID: 4157 | 来源树: SDK及示例

---

# 清晰度自适应

当设备支持该能力时，开发者可以在自己应用中的该设备清晰度选择列表中加入【自动】选项；  
当用户选择【自动】时，SDK会监测网络状况，通知升档降档消息给应用层，开发者再调用SDK中的指定api来切换设备清晰度，整个过程预览不断流。

## 一、判断设备是否支持 自动清晰度

EZDeviceInfo

```
/**
 * 是否支持自动清晰度
 */
public boolean isSupportDeviceAutoVideolevel();
```

## 二、加入【自动】选项、开启网络检测开关

开发者可以在支持该能力集的清晰度列表选项中加入【自动】选项，

![自动清晰度UI](https://resource.eziot.com/group1/M00/01/82/CtwQE2fFTMeAdGDtAAN-WkSK2j4383.png)

**当终端用户选择【自动】后，再开启网络检测开关并重新开始取流，并将该设备的自动清晰度开启状态缓存于本地，下次对设备进行取流时，EZPlayer初始化的时候须打开网络检测开关**，api如下  
  
EZPlayer

```
/**
 * 是否开启自动清晰度网络检测开关，startRealPlay之前调用；此api未调用时，不会回调以下消息
 * @see EZConstants.EZRealPlayConstants#MSG_VIDEO_LEVEL_AUTO_IMPROVE  网络好，会回调此消息，建议切换高一级清晰度
 * @see EZConstants.EZRealPlayConstants#MSG_VIDEO_LEVEL_AUTO_REDUCE   网络差，会回调此消息，建议切换低一级清晰度
 */
public void enableDeviceAutoVideoLevel();
```

示例代码如下：

```
// 本地缓存设备当前状态是否是"自动清晰度"，不支持的不用管理状态
if (isSupportDeviceAutoVideolevel) {
    SpTool.storeBooleanValue(ValueKeys.QUALITY_AUTO + "_" + mCameraInfo.getDeviceSerial(), isQulityModeAuto);
}
// 停止播放 Stop play
stopRealPlay();
SystemClock.sleep(500);
mEZPlayer.enableDeviceAutoVideoLevel();
// 开始播放 Start play
startRealPlay();
```

## 三、清晰度升档降档通知回调

EZPlayer的handler回调方法会接收到升档:EZRealPlayConstants.MSG\_VIDEO\_LEVEL\_AUTO\_IMPROVE 或 降档:EZRealPlayConstants.MSG\_VIDEO\_LEVEL\_AUTO\_REDUCE 消息回调后，调用如下api来切换清晰度

```
/**
 * 设置指定监控点视频清晰度(非强制，两个及以上客户端同时在取流时无法设置，会返回失败)
 * 录制过程中不能调用此接口，否则会导致录制视频异常
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @param cameraNo     设备通道号，默认为1
 * @param videoLevel   清晰度 0-流畅，1-均衡，2-高清，3-超清，4-极清，5-3K，6-4K
 * @return
 * @throws BaseException
 */
public boolean setVideoLevelAuto(String deviceSerial, int cameraNo, int videoLevel) throws BaseException;
```

- 当接收到升档:EZRealPlayConstants.MSG\_VIDEO\_LEVEL\_AUTO\_IMPROVE消息时，调用如上api设置高一级的清晰度
- 当接收到降档:EZRealPlayConstants.MSG\_VIDEO\_LEVEL\_AUTO\_REDUCE消息时，调用如上api设置低一级的清晰度

**注意事项：见如上api方法注释**

示例代码：

```
@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_VIDEO_LEVEL_AUTO_IMPROVE:// 清晰度升档，EZPlayer.enableDeviceAutoVideolevel开关打开后才会有此回调
            if (isQulityModeAuto && !isRecording) {// 录制的时候不能切换，涉及到分辨率的变化，会影响转码
                EZVideoLevel higherVideoLevel = EZBusinessTool.getHigherVideoLevel(mCurrentQulityMode, mDeviceDetailPublicInfo);
                if (higherVideoLevel.getVideoLevel() > mCurrentQulityMode.getVideoLevel()) {
                    setQualityModeAuto(higherVideoLevel);
                }
            }
            break;
        case EZRealPlayConstants.MSG_VIDEO_LEVEL_AUTO_REDUCE:// 清晰度降档，EZPlayer.enableDeviceAutoVideolevel开关打开后才会有此回调
            if (isQulityModeAuto && !isRecording) {
                EZVideoLevel lowerVideoLevel = EZBusinessTool.getLowerVideoLevel(mCurrentQulityMode, mDeviceDetailPublicInfo);
                if (lowerVideoLevel.getVideoLevel() < mCurrentQulityMode.getVideoLevel()) {
                    setQualityModeAuto(lowerVideoLevel);
                }
            }
            break;
        case EZRealPlayConstants.MSG_SET_VEDIOMODE_AUTO_SUCCESS:// 设置自动清晰度成功
            // do something
            setVideoLevel();
            break;
    }
}

/**
 * 设置自动清晰度请求
 * @param mode
 */
private void setQualityModeAuto(final EZVideoLevel mode) {
    if (mEZPlayer != null) {
        Thread thr = new Thread(() -> {
            try {
                EzvizApplication.getOpenSDK().setVideoLevelAuto(mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(), mode.getVideoLevel());
                mCurrentQulityMode = mode;
                Message msg = Message.obtain();
                msg.what = EZRealPlayConstants.MSG_SET_VEDIOMODE_AUTO_SUCCESS;
                mHandler.sendMessage(msg);
                LogUtil.i(TAG, "setQualityModeAuto success");
            } catch (BaseException e) {
                e.printStackTrace();
                LogUtil.i(TAG, "setQualityModeAuto fail");
                // 失败不用处理
            }

        });
        thr.start();
    }
}
```