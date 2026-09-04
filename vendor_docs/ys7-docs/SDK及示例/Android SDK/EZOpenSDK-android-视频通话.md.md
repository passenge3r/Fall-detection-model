# EZOpenSDK-android-视频通话.md

> EZOpenSDK-android-视频通话

> 更新时间: 2026-06-16T12:17:07.000+08:00

> 文档ID: 4179 | 来源树: SDK及示例

---

# 视频通话

视频通话功能是萤石屏类设备（比如S10）产品中的一项重要功能，旨在为用户提供便捷的远程视频通话体验。用户可以通过手机或其他设备与摄像头进行实时的视频对话。

## 注意事项

- EZOpenSDK的视频通话能力是基于ERTC SDK来实现的，EZOpenSDK封装了ERTC SDK，用于实现S10等屏类设备视频通话的需求。
- EZOpenSDK v5.21起支持视频通话。如果您的应用需要同时实现 **IPC设备取流** 和 **视频会议** 功能，使用EZOpenSDK v5.21及以上版本即可，无需再集成ERTC SDK。如果EZOpenSDK v5.21以下版本 与 ERTC SDK一起集成，可能存在编译或运行问题，须将EZOpenSDK升级到v5.21或以上版本，并移除ERTC SDK。
- EZOpenSDK 中所有ERTC SDK的头文件 和 api都是暴露的，如需实现视频通话其他能力，相关功能实现请参考 [ERTC SDK文档](https://open.ys7.com/help/1830) 即可。

## 名词解释

| 名词 | 释义 |
| --- | --- |
| 项目ID | 即ERTC SDK中的AppId，**不是AppKey**，请前往[萤石开放平台控制台-实时音视频](https://open.ys7.com/console/rtc/projectManage.html)进行创建 |
| 资源token（ertcToken） | 资源token，用于客户端(手机端)入会权限校验，不是accessToken，由客户服务端管理生成并透传给App，参考Java SDK生成：[前往](https://open.ys7.com/help/1873) |
| 资源token（ertcHttpToken) | 也是资源token，服务端使用，用于邀请设备入会，不是accessToken，由客户服务端管理生成并透传给App，参考Java SDK生成：[前往](https://open.ys7.com/help/1873) |
| 房间ID | roomId/房间号/会议ID，视频通话房间号，由客户服务端管理生成并透传给App |
| 用户ID | userId/姓名，视频通话用户ID，由客户服务端管理生成并透传给App |

## ERTCEngine初始化

客户端呼叫设备端 或 客户端接听设备端呼叫 都需要先初始化ERTCEngine对象。示例代码如下：

EZJoinMeetingActivity.java

```
// ------------------------------ ERTC初始化 ------------------------------

private void initErtcEngine() {
    String appId = appIdEt.getText().toString();
    String ertcToken = ertcTokenEt.getText().toString();
    String ertcHttpToken = ertcHttpTokenEt.getText().toString();
    String roomId = roomIdEt.getText().toString();
    String userId = userIdEt.getText().toString();
    ErtcHelper.initERTCEngine(EZJoinMeetingActivity.this, appId, new ERTCEngine.OnInitListener() {
        @Override
        public void onInitialization(ERTCEngine engine) {
            LogUtil.d(TAG, "Init OK");
            ErtcHelper.ertcEngine = engine;

            RTCConstant.EnterParam localUserInfo = new RTCConstant.EnterParam();
            localUserInfo.roomId = roomId;
            localUserInfo.userId = userId;
            localUserInfo.token = ertcToken;
            localUserInfo.appId = appId;

            ErtcRoomActivity.launch(EZJoinMeetingActivity.this, localUserInfo, mCameraInfo, ertcHttpToken,
                    isClientCallDevice, true, true);
        }

        @Override
        public void onError(int code) {
            LogUtil.d(TAG, "Init failed error:" + code);
        }
    });
}
```

ErtcHelper.java

```
public static void initERTCEngine(Context context, String appId, ERTCEngine.OnInitListener onInitListener) {
    // 环境设置
    AppSpUtils.saveHost(context, LocalInfo.getInstance().getOriginalServAddr());
    // 初始化
    RTCConstant.RTCEngineConfig config = new RTCConstant.RTCEngineConfig();
    config.appId = appId;
    config.context = context.getApplicationContext();
    // 音频编码类型[必须，S10音频使用AAC]
    config.audioCodeType = RTCConstant.ErtcAudioCodeType.AAC;
    // 日志路径[非必须]
    config.logLevel = LogUtil.ERTC_LOG_LEVEL_DEBUG;
    config.logPath = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS).getPath();
    // 日志回调[非必须]
    LogUtil.setErtcLogCallback((logLevel, tag, content) -> {
        // TODO 日志回调，可以根据自己的需要打印或写入日志
        com.videogo.util.LogUtil.d(tag, content);
    });
    ERTCEngine.init(config, onInitListener);
}
```

## 客户端（手机端）进入房间

示例代码如下：

ErtcRoomActivity.java

```
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    // do something

    // 设置大码流视频参数
    RTCConstant.ERTCVideoEncParam videoParam = new RTCConstant.ERTCVideoEncParam();
    videoParam.videoResolution = RTCConstant.ERTCVideoResolution.ERTCVideoResolution_1280_720;
    videoParam.videoFps = 15;
    // Android端，videoBitrate单位是字节，需要 *1024；iOS端，videoBitrate单位是Kbps
    videoParam.videoBitrate = 500 * 1024;
    ErtcHelper.ertcEngine.setVideoEncoderParam(videoParam, true);

    // 开关本地视频
    ErtcHelper.ertcEngine.enableLocalVideo(true);

    // 使用硬件回音消除，必须
    ErtcHelper.ertcEngine.enableHardAec(true);

    // 码流保存，开发调试用，线上必须关闭
    // ErtcHelper.ertcEngine.setERTCDebugAudioLog(true);

    // 设置填充模式及本地预览
    vcsLocalTextureView.setRenderType(RTCConstant.ERTC_VIDEO_RENDER_MODE_FILL);
    ErtcHelper.ertcEngine.setLocalView(vcsLocalTextureView);

    // 设置事件监听
    setRTCListener();

    // 进入房间
    ErtcHelper.ertcEngine.enterRoom(localUserInfo, RTCConstant.Scene.VideoCall);
}
```

- 设备端呼叫客户端：设备端发起呼叫，开发者的服务端会接收到该设备的呼叫消息，服务端通过长链接将呼叫消息通知给客户端，客户端使用如上方法进入对应房间即可。**应用与服务端的长链接需要开发者自行开发实现。**
- 客户端呼叫设备端：客户端发起呼叫，客户端使用如上方法进入房间，再邀请设备入会。

### 邀请设备入会

如果是客户端（手机端）发起视频通话，客户端进入房间成功后，再邀请设备进入对应房间。

示例代码如下：

ErtcRoomActivity.java

```
private void setRTCListener() {
    ErtcHelper.ertcEngine.setRTCListener(new RTCListener() {

        /**
         * 用户加入房间成功，加入房间成功后将收到回调
         */
        @Override
        public void onEnterRoomSuccess() {
            super.onEnterRoomSuccess();
            // 进入房间成功
            LogUtil.d(TAG, "ErtcRoomEventListener onEnterRoomSuccess");
            // 客户端发起视频通话，邀请设备入会
            if (isClientCallDevice) {
                inviteDeviceEnterMeeting();
            }
        }

        ......
    });
}

private void inviteDeviceEnterMeeting() {
    // 客户端发起视频通话，邀请设备入会
    new Thread(() -> {
        try {
            EzvizApplication.getOpenSDK().inviteDeviceEnterMeeting(localUserInfo.appId, ertcHttpToken, localUserInfo.roomId,
                    mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(), localUserInfo.userId);
        } catch (BaseException e) {
            e.printStackTrace();
            toast("邀请设备入会失败");
            runOnUiThread(() -> {
                toggleHangUp();
            });
        }
    }).start();
}
```

### 取消邀请设备入会

如果是客户端（手机端）发起视频通话，客户端进入房间后，设备端一直未接听，需设置一个超时时间。超时后，取消邀请设备入会。

示例代码如下：

ErtcRoomActivity.java

```
// 启动计时器
private void startUpdateTimer() {
    stopUpdateTimer();
    // 开始录像计时
    mUpdateTimer = new Timer();
    mUpdateTimerTask = new TimerTask() {
        @Override
        public void run() {
            mVideoTalkSecond ++;
            runOnUiThread(() -> {
                String convToUIDuration = RemoteListUtil.convToUIDuration(mVideoTalkSecond);
                tvVideoTalkTime.setText(convToUIDuration);
                // 15秒后设备仍未进入会议的话，视频通话失败，退出房间
                if (mVideoTalkSecond > 15 && !isRemoteUserEnterRoom) {
                    showToast("设备端无人接听，视频通话结束");
                    stopUpdateTimer();
                    toggleHangUp();
                }
            });
        }
    };
    // 延时1000ms后执行，1000ms执行一次
    mUpdateTimer.schedule(mUpdateTimerTask, 0, 1000);
}

/**
 * 挂断
 */
private void toggleHangUp() {
    // 客户端呼叫设备 && 设备未接听，取消邀请设备入会
    if (isClientCallDevice && !isRemoteUserEnterRoom) {
        cancelInviteDeviceEnterMeeting();
    }
    releaseERTC("endMeeting 会议结束");
    finish();
}

private void cancelInviteDeviceEnterMeeting() {
    // 客户端发起视频通话，取消邀请设备入会
    new Thread(() -> {
        try {
            EzvizApplication.getOpenSDK().cancelInviteDeviceEnterMeeting(localUserInfo.appId, ertcHttpToken, localUserInfo.roomId,
                    mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(), localUserInfo.userId);
        } catch (BaseException e) {
            e.printStackTrace();
            toast("取消邀请设备入会失败");
        }
    }).start();
}
```

## 订阅设备端码流

ERTCEngine设置代理后，在-onUserVideoAvailable方法中订阅设备端的码流。

示例代码如下：

ErtcRoomActivity.java

```
private void setRTCListener() {
    ErtcHelper.ertcEngine.setRTCListener(new RTCListener() {

        /**
         * 用户加入房间成功，加入房间成功后将收到回调
         */
        @Override
        public void onEnterRoomSuccess() {
            super.onEnterRoomSuccess();
            // 进入房间成功
            LogUtil.d(TAG, "ErtcRoomEventListener onEnterRoomSuccess");
            // 客户端发起视频通话，邀请设备入会
            if (isClientCallDevice) {
                inviteDeviceEnterMeeting();
            }
        }

        /**
         * 用户退出房间，非主动退出房间才会收到该回调
         * @param reason 退出房间原因
         */
        @Override
        public void onExitRoom(int reason) {
            super.onExitRoom(reason);
            // 退出房间成功
            LogUtil.d(TAG, "ErtcRoomEventListener onExitRoom");
        }

        /**
         * 远端用户进入房间成功回调，进入房间时将会收到所有已在房间内用户加入房间的回调
         * @param userId 用户id
         */
        @Override
        public void onRemoteUserEnterRoom(String userId) {
            super.onRemoteUserEnterRoom(userId);
            LogUtil.d(TAG, "ErtcRoomEventListener onRemoteUserEnterRoom RemoteUser加入房间成功 userId:" + userId);
            runOnUiThread(() -> {
                isRemoteUserEnterRoom = true;
                vcsRemoteTextureView.setVisibility(View.VISIBLE);
            });
        }

        /**
         * 远端用户离开房间
         * @param userId 用户ID
         * @param reason 离开原因，0表示用户主动退出房间，1表示用户超时退出。
         */
        @Override
        public void onRemoteUserLeaveRoom(String userId, int reason) {
            super.onRemoteUserLeaveRoom(userId, reason);
            LogUtil.d(TAG, "ErtcRoomEventListener onRemoteUserLeaveRoom RemoteUser离开房间成功 userId:" + userId);
            runOnUiThread(() -> {
                showToast(R.string.ys_mt_room_toast_video_end);
                toggleHangUp();
            });
        }

        /**
         * 远端用户打开或关闭视频流的回调
         * @param userId 远端用户id
         * @param available true-视频可用 false-视频不可用
         * @param streamType 码流类型
         */
        @Override
        public void onUserVideoAvailable(String userId, boolean available, int streamType) {
            super.onUserVideoAvailable(userId, available, streamType);
            LogUtil.d(TAG, "ErtcRoomEventListener onUserVideoAvailable userId:" + userId + ", available:" + available);
            runOnUiThread(() -> {
                Boolean value = remoteUserMap.get(userId);
                if (value != null && value.booleanValue() == available) {
                    LogUtil.d(TAG, "ErtcRoomEventListener duplicate message, filtered");
                    return;
                }

                remoteUserMap.put(userId, available);
                if (available) {
                    vcsRemoteTextureView.setRenderType(RTCConstant.ERTC_VIDEO_RENDER_MODE_FIT);
                    ErtcHelper.ertcEngine.setRemoteView(userId, RTCConstant.ERTC_VIDEO_STREAM_TYPE_BIG,
                            vcsRemoteTextureView);
                } else {
                    ErtcHelper.ertcEngine.setRemoteView(userId, RTCConstant.ERTC_VIDEO_STREAM_TYPE_BIG,
                            null);
                }
            });
        }

        @Override
        public void onError(int errorCode) {
            super.onError(errorCode);
            // ERTC错误码文档：https://open.ys7.com/help/1825
            LogUtil.d(TAG, "ErtcRoomEventListener onError errorCode:" + errorCode);
            runOnUiThread(() -> {
                if (errorCode == BaseError.ERR_SERVICE_ACCESSTOKEN_INVALID) {
                    showToast("ertcToken异常，请更新token后重新入会。");
                } else {
                    showToast("errorCode:" + errorCode);
                }
                toggleHangUp();
            });
        }
    });
}
```

## 视频通话工具栏功能

### 麦克风开关

ERTCEngine.class

```
/// 开启本地音频模块并推流，调用成功后其它用户将收到 onUserAudioAvailable
/// @param enable true-开启 false-关闭
public abstract void enableLocalAudio(boolean enable);
```

### 扬声器/耳机

ERTCEngine.class

```
/// 打开扬声器，默认扬声器是开的
/// @param enable 打开扬声器
public abstract void setSpeakerPhoneOn(boolean enable);
```

### 挂断

示例代码：

```
public void releaseERTC(String cause) {
    LogUtil.i(TAG, "release===cause[" + cause + "]");
    final ERTCEngine ertcEngine = ErtcHelper.ertcEngine;
    if (ertcEngine != null) {
        ertcEngine.setLocalView(null);
        ertcEngine.setLocalViewChanged(null);
        ertcEngine.enableLocalVideo(false);
        ertcEngine.setRTCListener(null);
        ertcEngine.setRtcStatsListener(null);
        new Thread(() -> {
            ertcEngine.exitRoom();
            ERTCEngine.destroyEngine();
        }).start();
    }
}
```

### 前后摄像头切换

ERTCEngine.class

```
/// 切换前后置摄像头
public abstract void switchCamera();
```

### 摄像头禁用/取消禁用

ERTCEngine.class

```
/// 是否开启本地采集并推流。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 onUserVideoAvailable
/// @param enable true-开启推流 false-关闭推流
public abstract void enableLocalVideo(boolean enable);
```