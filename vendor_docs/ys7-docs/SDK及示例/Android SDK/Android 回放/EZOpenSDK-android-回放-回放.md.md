# EZOpenSDK-android-回放-回放.md

> EZOpenSDK-android-回放-回放

> 更新时间: 2026-06-02T14:03:39.000+08:00

> 文档ID: 4161 | 来源树: SDK及示例

---

# 回放

对摄像机存储于SD卡、云端的录像进行取流，查看当前摄像机的历史回放画面。

## 录像片段播放

### 1. 第一步创建播放器

可调用EZOpenSDK中的 createPlayer 方法创建播放器。

### 2. 第二步配置播放器

播放器创建完成后需要进行设置代理，设置播放视图，验证码设置等配置。

### 3. 第三步开始播放

调用startPlayback(EZCloudRecordFile cloudFile) 或 startPlayback(EZDeviceRecordFile deviceFile) 开始回放

### 4. 第四步结束播放

调用stopPlayback结束回放

### 5.第五步释放播放器

调用release释放播放器

完整示例代码如下：

```
public class EZPlayBackListActivity extends RootActivity implements TextureView.SurfaceTextureListener, Handler.Callback, ... {
  private EZPlayer mPlaybackPlayer = null;

  /**
   * 点击录像片段后调用
   */
  private void initEZPlayer() {
    if (mPlaybackPlayer != null) {
        // do something
        // 停止播放
        mPlaybackPlayer.stopPlayback();
    } else {
        // 创建播放器，也可以直接使用EZPlayer类中的方法创建
        mPlaybackPlayer = getOpenSDK().createPlayer(mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo());

        // 设置Handler, 该handler将被用于从播放器向handler传递消息
        mPlaybackPlayer.setHandler(playBackHandler);

        // 设置播放器的显示Surface
        mPlaybackPlayer.setSurfaceEx(mTextureView.getSurfaceTexture());

        // 可选，设备开启了视频/图片加密功能后需设置，可根据EZDeviceInfo的isEncrypt属性判断
        mPlaybackPlayer.setPlayVerifyCode(verifyCode);

        // 回放云端存储的视频，cloudFile由EZOpenSDK.searchRecordFileFromCloud接口获取
        mPlaybackPlayer.startPlayback(cloudFile);

        // 或者
        // 回放设备上存储的视频，deviceFile由EZOpenSDK.searchRecordFileFromDevice接口获取
        mPlaybackPlayer.startPlayback(deviceFile);
    }
  }

  @Override
    protected void onStop() {
        super.onStop();
        if (mPlaybackPlayer != null) {
            // 页面退出或用户主动停止播放时调用stopPlayback结束回放
            mPlaybackPlayer.stopPlayback();
        }
        // do something
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mPlaybackPlayer != null) {
            // 调用release释放播放器
            mPlaybackPlayer.release();
        }
        // do something
    }

  @Override
  public void handleMessage(Message msg) {
      super.handleMessage(msg);
      switch (msg.what) {
          // 画面显示第一帧
          case EZPlaybackConstants.MSG_REMOTEPLAYBACK_PLAY_SUCCUSS:// 录像回放成功
              // do something
              break;
          case EZPlaybackConstants.MSG_REMOTEPLAYBACK_PLAY_START:// 播放开始|seek成功
              // do something
              break;
          case EZPlaybackConstants.MSG_REMOTEPLAYBACK_STOP_SUCCESS:// 录像回放停止
              // do something
              break;
          case EZPlaybackConstants.MSG_REMOTEPLAYBACK_PLAY_FINISH:// 录像回放完成
              // do something
              break;
          case EZPlaybackConstants.MSG_REMOTEPLAYBACK_PLAY_FAIL:// 录像回放失败
              ErrorInfo errorInfo = (ErrorInfo) msg.obj;
              int errorCode = errorInfo.errorCode;
              // 如果是需要验证码或者是验证码错误
              if (errorCode == ErrorCode.ERROR_INNER_VERIFYCODE_NEED || errorCode == ErrorCode.ERROR_INNER_VERIFYCODE_ERROR) {
                  // do something
              } else {
                  // do something
              }
              break;
          default:
              break;
      }
  }

}
```

  

### 说明

1. 回放需先获取到视频信息，searchRecordFileFromCloud方法和searchRecordFileFromDevice方法分别是获取云端视频列表和设备存储视频列表的两个方法。
2. 开始播放之后在handleMessage回调中会收到通知消息，播放成功消息为EZPlaybackConstants.MSG\_REMOTEPLAYBACK\_PLAY\_SUCCUSS， 播放失败消息为EZPlaybackConstants.MSG\_REMOTEPLAYBACK\_PLAY\_FAIL，如果是错误码ErrorCode.ERROR\_INNER\_VERIFYCODE\_NEED = 400035(需要设备验证码)或者ErrorCode.ERROR\_INNER\_VERIFYCODE\_ERROR = 400036（设备验证码不匹配），需要开发者自己处理让用户输入验证密码，然后调用EZPlayer.setPlayVerifyCode设置密码，重新启动播放。

**注意**：实际录像回放结束时间可能与录像片段的结束时间有偏差，如果时间点相近则认为回放结束，此为正常现象。

## 多个录像片段连续播放

萤石Demo中演示的录像播放都为单个录像片段的播放。如需实现多个录像片段连续播放，可以将录像片段进行合并。

### SD卡录像

SD卡录像对象为EZDeviceRecordFile

例：如有三个**已按时间先后顺序排列**的SD卡录像片段recordFileA、recordFileB、recordFileC。只需要将recordFileA的结束时间设置为recordFileC的结束时间，再调用mPlaybackPlayer.startPlayback(recordFileA);即可实现三个录像片段连续播放。

### 云存储

云存储录像对象为EZCloudRecordFile

例：如有三个**已按时间先后顺序排列**的云存储录像片段recordFileA、recordFileB、recordFileC。

当三个对象的**encryption、istorageVersion、cloudType**字段值都一致时，将recordFileA的结束时间设置为recordFileC的结束时间，再调用mPlaybackPlayer.startPlayback(recordFileA);即可实现三个录像片段连续播放；

**否则**，需要先调用mPlaybackPlayer.startPlayback(recordFileA);开始回放，待接收到recordFileA回放完成通知后，再调用mPlaybackPlayer.startPlayback(recordFileB);开始回放，依此类推。

通常情况下，istorageVersion、cloudType字段值都是一致的，encryption字段值看用户有没有更改取流密码。

| 字段 | 释义 |
| --- | --- |
| encryption | 录像加密密码 |
| istorageVersion | 云存储类别 |
| cloudType | 云存储供应商 |

**Q：连续播放时，如何将当前画面所属的录像片段设置为选中状态？**

**A**：播放时，创建一个定时器（每秒刷新播放进度、更新UI等）。通过mPlaybackPlayer.getOSDTime()获取当前播放画面的时间戳，遍历录像列表并判断该时间戳位于哪个录像片段，将所属片段设置为选中状态。