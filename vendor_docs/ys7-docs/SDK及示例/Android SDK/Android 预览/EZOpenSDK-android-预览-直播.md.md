# EZOpenSDK-android-预览-直播.md

> EZOpenSDK-android-预览-直播

> 更新时间: 2026-06-02T14:03:36.000+08:00

> 文档ID: 4152 | 来源树: SDK及示例

---

# 直播

## 预览

对摄像机实时取流，查看当前摄像机的实时直播画面。

### 1. 第一步创建播放器

可调用EZOpenSDK类中的 createPlayer 方法创建播放器。

### 2. 第二步配置播放器

播放器创建完成后需要进行设置handler回调、显示区域、SurfaceHold、验证码设置等配置。

### 3. 第三步开始播放

调用startRealPlay开启直播

### 4. 第四步结束播放

调用stopRealPlay结束直播

### 5.第五步释放播放器

调用release释放播放器

### 6.第六步SurfaceHold窗口解绑

预览结束后，需重写surfaceDestroyed方法，将SurfaceHolder与EZPlayer解绑。

如未解绑，可能导致下一次取流失败，相关错误码如下

| 错误码 | 释义 | 原因 |
| --- | --- | --- |
| 321022/322008 | 窗口已经被占用 | A设备播放器创建时，取流页面的surfaceHolder通过setSurfaceHold绑定给了playerA， A设备取流结束时需要解绑surfaceHolder，即playerA.setSurfaceHold(null);  如果不解绑，直接将surfaceHolder再次绑定给设备B的播放器playerB，就会出现此错误码。 |

  

#### 完整示例代码如下：

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

        // 开始直播
        mEZPlayer.startRealPlay();
    }

    @Override
    protected void onStop() {
        super.onStop();
        if (mEZPlayer != null) {
            // 页面退出或用户主动停止播放时调用stopRealPlay结束直播
            mEZPlayer.stopRealPlay();
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
            case MSG_VIDEO_SIZE_CHANGED:// 播放器尺寸变化
                // do something
                break;
            case EZRealPlayConstants.MSG_REALPLAY_PLAY_SUCCESS:// 播放成功消息
                // do something
                break;
            case EZRealPlayConstants.MSG_REALPLAY_PLAY_FAIL:// 播放失败消息
                //播放失败,得到失败信息
                ErrorInfo errorinfo = (ErrorInfo) msg.obj;
                int errorCode = errorInfo.errorCode;
                // 如果是需要验证码或者是验证码错误
                if (errorCode == ErrorCode.ERROR_INNER_VERIFYCODE_NEED || errorCode == ErrorCode.ERROR_INNER_VERIFYCODE_ERROR) {
                    // do something
                } else {
                    // do something
                }
                
                break;
        }
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
        if (mEZPlayer != null) {
            mEZPlayer.setSurfaceHold(holder);
        }
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        if (mEZPlayer != null) {
            mEZPlayer.setSurfaceHold(holder);
        }
        if (mStatus == RealPlayStatus.STATUS_INIT) {
            // 开始播放
            startRealPlay();
        }
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        if (mEZPlayer != null) {
            mEZPlayer.setSurfaceHold(null);
        }
        mRealPlaySh = null;
    }

}
```

  

### 说明

1. 可调用EZOpenSDK.setVideoLevel(String deviceSerial, int cameraNo, int videoLevel)接口设置视频清晰度，此调节可以在视频播放前设置也可以在视频播放成功后设置。视频播放成功后设置了清晰度，需要先停止播放stopRealPlay，然后重新开启播放startRealPlay才能生效。
2. 开始播放之后在handleMessage回调中会收到通知消息，播放成功消息为EZRealPlayConstants.MSG\_REALPLAY\_PLAY\_SUCCESS，播放失败消息为EZRealPlayConstants.MSG\_REALPLAY\_PLAY\_FAIL；如果是错误码ERROR\_INNER\_VERIFYCODE\_NEED = 400035(需要设备验证码)或者ERROR\_INNER\_VERIFYCODE\_ERROR = 400036（设备验证码不匹配），需要开发者自己处理让用户输入验证密码，然后调用EZPlayer.setPlayVerifyCode(String verifyCode)设置密码，然后重新启动播放。
3. 电池设备取流1分钟后会进入休眠，导致取流链路断开。如需继续预览，需调用平台接口来唤醒设备，保持设备不休眠。具体实现方案如下：
   - 判断是否是电池设备。可通过EZDeviceInfo.getSupportInt(322)获取，(0)不使用电池 (1)一块电池 (2)两块电池
   - 如果是电池设备，创建一个定时器，每隔50秒调用[平台接口-唤醒设备](https://open.ys7.com/help/1529)来唤醒设备。

## 播放器窗口大小设置

播放器窗口大小设置有多种方法，任选其一即可。

### 方法一

IPC摄像头的画面尺寸通常采用16:9的固定宽高比，因此可以直接将窗口的显示比例设定为16:9。Demo工程采用此方案。

### 方法二

监听EZPlayer播放器消息通知，获取画面宽高，宽高相除得到宽高比，取流成功后才会回调。

EZRealPlayActivity.java

```
@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_REALPLAY_PLAY_SUCCESS:// 播放成功
            // do something
            break;
        // 其他消息监听

        case EZConstants.MSG_VIDEO_SIZE_CHANGED:// 播放器尺寸变化
            try {
                String temp = (String) msg.obj;
                String[] strings = temp.split(":");
                Integer mVideoWidth = Integer.parseInt(strings[0]);
                Integer mVideoHeight = Integer.parseInt(strings[1]);
            } catch (Exception e) {
                e.printStackTrace();
            }
            break;
        
    }
    return false;
}
```

### 方法三

调用EZPlayer类中的getDeviceDetailInfo方法获取画面宽高，宽高相除得到宽高比，取流成功后调用有效。

EZRealPlayActivity.java

```
@Override
public boolean handleMessage(Message msg) {
    if (this.isFinishing()) {
        return false;
    }
    LogUtil.i(TAG, "handleMessage:" + msg.what);
    switch (msg.what) {
        case EZRealPlayConstants.MSG_REALPLAY_PLAY_SUCCESS:// 播放成功
            EZDeviceDetailPublicInfo mDeviceDetailPublicInfo = mEZPlayer.getDeviceDetailInfo();
            Integer mVideoWidth = mDeviceDetailPublicInfo.videoWidth;
            Integer mVideoHeight = mDeviceDetailPublicInfo.videoHeight;
            break;
        // 其他消息监听
        
    }
    return false;
}
```

### 方法四

调用EZDeviceInfo类中的getSupportString方法获取设备能力集，传入位数16 获取画面宽高比，设备信息获取后即可调用，不需要等到取流成功之后。

EZDeviceInfo.java

```
 * 根据位数获取设备能力集
 * @param index 位数，必须大于0
 *
 * @return 能力值
 */
public String getSupportValue(int index);
```

代码示例：

```
String videoRadio = deviceInfo.getSupportValue(16);// 获取的值为16-9，代表16:9
```