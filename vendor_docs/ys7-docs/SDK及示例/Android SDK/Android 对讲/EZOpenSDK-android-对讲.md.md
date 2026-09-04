# EZOpenSDK-android-对讲.md

> EZOpenSDK-android-对讲

> 更新时间: 2026-06-02T14:03:41.000+08:00

> 文档ID: 4168 | 来源树: SDK及示例

---

# 对讲

分为全双工对讲和半双工对讲

- 对讲流程需要根据设备的对讲能力进行区分处理。EZDeviceInfo中的isSupportTalk可获取到设备的对讲能力，0-不支持对讲，1-支持全双工对讲，3-支持半双工对讲。
- 同一设备需要开启不同功能（直播/回放/对讲）的播放器时，需要分别对每个功能创建一个播放器。播放器的功能是单一的。

## 全双工对讲

全双工对讲，与半双工对讲对应，指的是通信系统中同时进行双向对讲的方式，它允许对讲的双方可以在同一时刻进行发送和接收语音，而不需要像半双工通信那样交替进行。

### 1. 第一步创建对讲播放器

可调用EZOpenSDK类中的 createPlayer 方法创建对讲播放器。

### 2. 第二步配置对讲播放器

对讲播放器创建完成后需要进行设置handler回调，验证码设置等配置。  
**注意**：v5.18之前对讲播放器需要配置验证码，v5.18起取消了验证码的校验，无须在配置验证码

### 3. 第三步开始对讲

- IPC设备调用startVoiceTalk(true)开启对讲。
- NVR设备调用startVoiceTalk(false)开启通道对讲

### 4. 第四步结束对讲

调用stopVoiceTalk结束对讲

### 5. 第五步释放对讲播放器

调用release释放对讲播放器

**示例代码**：

```
public class EZRealPlayActivity extends RootActivity implements SurfaceHolder.Callback,
        Handler.Callback, ... {

    private EZPlayer mEZPlayer = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // do something

        // 创建播放器，也可以直接使用EZPlayer类中的方法创建
        mEZPlayer = EzvizApplication.getOpenSDK().createPlayer(mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo());

        // 设置Handler, 该handler将被用于从播放器向handler传递消息
        mEZPlayer.setHandler(mHandler);

        // 设置播放器的显示Surface
        mEZPlayer.setSurfaceHold(mRealPlaySh);

        // 可选，设备开启了视频/图片加密功能后需设置，可根据EZDeviceInfo的isEncrypt属性判断
        mEZPlayer.setPlayVerifyCode(verifyCode);

        // 对讲开启前，关闭播放器的声音；否则画面码流和对讲码流中同时播放声音，导致回音
        // Turn off the sound of the player before starting the intercom; Otherwise,
        // playing sound simultaneously in both the picture stream and the intercom stream
        if (mEZPlayer != null) {
            mEZPlayer.closeSound();
        }
        // IPC设备发起对讲
        mEZPlayer.startVoiceTalk(true);

        // NVR设备发起对讲
        // mEZPlayer.startVoiceTalk(false);
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mEZPlayer != null) {
            // 页面退出或用户主动停止播放时调用stopVoiceTalk结束对讲
            mEZPlayer.stopVoiceTalk();
        }
        // do something
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mEZPlayer != null) {
            // 调用release释放播放器
            mEZPlayer.release();
        }
        // do something
    }

    @Override
    public boolean handleMessage(Message msg) {
        if (this.isFinishing()) {
            return false;
        }
        LogUtil.i(TAG, "handleMessage:" + msg.what);
        switch (msg.what) {
            case EZRealPlayConstants.MSG_REALPLAY_VOICETALK_SUCCESS:// 对讲成功
                // do something
                break;
            case EZRealPlayConstants.MSG_REALPLAY_VOICETALK_STOP:// 对讲停止成功
                // do something
                // 对讲结束后把player播放器的声音重新打开
                if (mStatus == RealPlayStatus.STATUS_PLAY) {
                    if (mEZPlayer != null) {
                        if (mLocalInfo.isSoundOpen()) {
                            mEZPlayer.openSound();
                        } else {
                            mEZPlayer.closeSound();
                        }
                    }
                }
                break;
            case EZRealPlayConstants.MSG_REALPLAY_VOICETALK_FAIL:// 对讲失败
                //播放失败,得到失败信息
                ErrorInfo errorinfo = (ErrorInfo) msg.obj;
                int errorCode = errorInfo.errorCode;
                // do something
                break;
        }
    }

}
```

## 半双工对讲

半双工对讲，指的是通信系统中交替进行发送和接收语音的模式，与对讲机类似，一方说话期间，其他用户只能接听，只有该用户停止讲话，其他用户才能开始讲话。

半双工设备对讲代码实现与全双工对讲一样。区别是发起成功后，默认模式为 **手机端听-设备端说**。可进行如下操作进行听说模式切换。

```
// 切换到 手机端说-设备端听 模式
mEZPlayer.setVoiceTalkStatus(true);

// 切换到 手机端听-设备端说 模式
mEZPlayer.setVoiceTalkStatus(false);
```