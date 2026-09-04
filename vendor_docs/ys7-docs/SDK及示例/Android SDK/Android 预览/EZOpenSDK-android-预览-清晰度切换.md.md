# EZOpenSDK-android-预览-清晰度切换.md

> EZOpenSDK-android-预览-清晰度切换

> 更新时间: 2026-06-02T14:03:37.000+08:00

> 文档ID: 4156 | 来源树: SDK及示例

---

# 清晰度切换

一般摄像头支持多种视频清晰度，比如：标清、高清、超清、极清等清晰度，可以让设备端推送不同清晰度的流进行清晰度切换；
由于设备端一般只会推送同一个清晰度的流，因此当多人同时观看，如果有单个客户端切换清晰度，所有客户端的观看清晰度都会同时变化。

### 设备支持的清晰度数据

取流成功后，SDK会通过handler回调方法通知，当msg.what = EZRealPlayConstants.MSG\_REALPLAY\_PLAY\_SUCCESS时，调用如下api可获取设备详情EZDeviceDetailPublicInfo对象，该对象中包含 清晰度数据列表 字段videoQualityInfos  
  
EZPlayer

```
/**
 * 获取设备部分详情信息（出画面后才有回调）
 * @return
 */
public EZDeviceDetailPublicInfo getDeviceDetailInfo();
```

示例代码：

```
private EZDeviceDetailPublicInfo mDeviceDetailPublicInfo;// 取流详情数据

@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_REALPLAY_PLAY_SUCCESS:// 播放成功消息
            // do something
            mDeviceDetailPublicInfo = this.mEZPlayer.getDeviceDetailInfo();
            break;
        }
    }
```

**注意：**
EZOpenSDK类中的 getDeviceList 和 getDeviceInfo 等api中获取到的videoQualityInfos值不一定准确，不建议使用。

### 清晰度设置

```
/**
 * 设置指定监控点视频清晰度
 * 该接口为耗时操作，必须在线程中调用
 *
 * @param deviceSerial 设备序列号
 * @param cameraNo     设备通道号，默认为1
 * @param videoLevel   清晰度 0-流畅，1-均衡，2-高清，3-超清，4-极清，5-3K，6-4K
 * @return
 * @throws BaseException
 * @since 4.2
 */
public boolean setVideoLevel(String deviceSerial, int cameraNo, int videoLevel) throws BaseException;
```

示例代码：

```
/**
 * 设置清晰度请求
 * @param mode
 */
private void setQualityMode(final EZVideoLevel mode) {
    // do something
    if (mEZPlayer != null) {
        mWaitDialog.setWaitText(this.getString(R.string.setting_video_level));
        mWaitDialog.show();
        Thread thr = new Thread(() -> {
            try {
                EzvizApplication.getOpenSDK().setVideoLevel(mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(), mode.getVideoLevel());
                mCurrentQulityMode = mode;
                Message msg = Message.obtain();
                msg.what = EZRealPlayConstants.MSG_SET_VEDIOMODE_SUCCESS;
                mHandler.sendMessage(msg);
                LogUtil.i(TAG, "setQualityMode success");
            } catch (BaseException e) {
                e.printStackTrace();
                Message msg = Message.obtain();
                msg.what = EZRealPlayConstants.MSG_SET_VEDIOMODE_FAIL;
                mHandler.sendMessage(msg);
                LogUtil.i(TAG, "setQualityMode fail");
            }

        });
        thr.start();
    }
}

@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_SET_VEDIOMODE_SUCCESS:// 设置清晰度成功
            handleSetVedioModeSuccess();
            break;
        case EZRealPlayConstants.MSG_SET_VEDIOMODE_FAIL:// 设置清晰度失败
            handleSetVedioModeFail(msg.arg1);
            break;
    }
}

private void handleSetVedioModeSuccess() {
    setVideoLevel();
    try {
        mWaitDialog.setWaitText(null);
        mWaitDialog.dismiss();
    } catch (Exception e) {
        e.printStackTrace();
    }
    // 停止播放 Stop play
    stopRealPlay();
    SystemClock.sleep(500);
    // 开始播放 Start play
    startRealPlay();
}

private void handleSetVedioModeFail(int errorCode) {
    setVideoLevel();
    try {
        mWaitDialog.setWaitText(null);
        mWaitDialog.dismiss();
    } catch (Exception e) {
        e.printStackTrace();
    }
    Utils.showToast(EZRealPlayActivity.this, R.string.realplay_set_vediomode_fail, errorCode);
}

/**
 * 设置视频清晰度UI
 */
private void setVideoLevel() {
    if (mCameraInfo == null || mEZPlayer == null || mDeviceInfo == null) {
        return;
    }
    mRealPlayQualityBtn.setEnabled(mDeviceInfo.getStatus() == 1);
    // 本地数据保存 需要更新之前获取到的设备列表信息，开发者自己设置
    mCameraInfo.setVideoLevel(mCurrentQulityMode.getVideoLevel());
    mRealPlayQualityBtn.setText(EZBusinessTool.getDeviceQualityTitle(this, mCurrentQulityMode.getVideoLevel()));
}
```