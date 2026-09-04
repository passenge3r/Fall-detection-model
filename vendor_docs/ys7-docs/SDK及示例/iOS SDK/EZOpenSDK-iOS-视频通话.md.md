# EZOpenSDK-iOS-视频通话.md

> EZOpenSDK-iOS-视频通话

> 更新时间: 2026-06-16T12:15:22.000+08:00

> 文档ID: 4105 | 来源树: SDK及示例

---

# 视频通话

视频通话功能是萤石屏类设备（比如S10）产品中的一项重要功能，旨在为用户提供便捷的远程视频通话体验。用户可以通过手机或其他设备与摄像头进行实时的视频对话。

## 注意事项

- EZOpenSDK的视频通话能力是基于ERTC SDK来实现的，EZOpenSDK封装了ERTC SDK，用于实现S10等屏类设备视频通话的需求。
- EZOpenSDK v5.21起支持视频通话。如果您的应用需要同时实现 **IPC设备取流** 和 **视频会议** 功能，使用EZOpenSDK v5.21及以上版本即可，无需再集成ERTC SDK。如果EZOpenSDK v5.21以下版本 与 ERTC SDK一起集成，可能存在编译或运行问题，须将EZOpenSDK升级到v5.21或以上版本，并移除ERTC SDK。
- EZOpenSDK 中所有ERTC SDK的头文件 和 api都是暴露的，如需实现视频通话其他能力，相关功能实现请参考 [ERTC SDK文档](https://open.ys7.com/help/1824) 即可。

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

EZJoinMeetingViewController.m

```
#pragma mark - ERTC初始化

/**
 * ERTC初始化
 * @param isClientCallDevice 是否是客户端呼叫设备端
 */
- (void)initErtcEngine:(BOOL)isClientCallDevice {
    NSString *appId = [self.appIdTextField.text trim];
    NSString *ertcToken = [self.ertcTokenTextField.text trim];
    NSString *ertcHttpToken = [self.ertcHttpTokenTextField.text trim];
    NSString *roomId = [self.roomIdTextField.text trim];
    NSString *userId = [self.userIdTextField.text trim];
    
    [[ErtcHelper sharedInstance] initERTCEngine:appId initBlock:^(ERTCEngine * _Nullable instance, NSError * _Nullable error) {
        if (!error) {
            NSLog(@"ERTCEngine init OK");
            [ErtcHelper sharedInstance].ertcEngine = instance;
            
            ERTCParam *ertcParam = [[ERTCParam alloc] init];
            ertcParam.roomId = roomId;
            ertcParam.userId = userId;
            ertcParam.token = ertcToken;
            ertcParam.appID = appId;
            ertcParam.apiUrl = [kUserDefaults objectForKey:UserApiUrl];
            ErtcRoomViewController *ertcRoomVC = [[ErtcRoomViewController alloc] init];
            ertcRoomVC.ertcParam = ertcParam;
            ertcRoomVC.ertcHttpToken = ertcHttpToken;
            ertcRoomVC.cameraInfo = self.cameraInfo;
            ertcRoomVC.isClientCallDevice = isClientCallDevice;
            [self.navigationController pushViewController:ertcRoomVC animated:YES];
        } else {
            NSLog(@"ERTCEngine init failed--->%@", error);
        }
    }];
}
```

ErtcHelper.m

```
+ (void)initERTCEngine:(NSString *)appId initBlock:(InstanceBlock)initBlock {
    [[ERTCLog sharedInstance] enableFileLog];// 打开文件log
    [[ERTCLog sharedInstance] enableConsoleLog];// 打开控制台log
    ERTCEngineConfig *config = [[ERTCEngineConfig alloc] init];
    config.apiUrl = [kUserDefaults objectForKey:UserApiUrl];// 指定域名
    config.appID = appId;
    
    [ERTCEngine createWithConfig:config instanceBlock:initBlock];
}
```

## 客户端（手机端）进入房间

示例代码如下：

ErtcRoomViewController.m

```
- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    // 设置大码流视频参数
    ERTCVideoEncParam *videoParam = [[ERTCVideoEncParam alloc] init];
    videoParam.videoResolution = ERTCVideoResolution_1280_720;
    videoParam.videoFps = ERTCVideoFPS_15;
    // iOS端，videoBitrate单位是Kbps；Android端，videoBitrate单位是字节，需要 *1024
    videoParam.videoBitrate = 500;
    videoParam.resMode = ERTCVideoResolutionModePortrait;
    [[ErtcHelper sharedInstance].ertcEngine setVideoEncoderParam:videoParam];
    
    // 开关本地视频
    [[ErtcHelper sharedInstance].ertcEngine enableLocalVideo:YES];
    
    // 音频编码类型[必须，S10音频使用AAC]
    [[ErtcHelper sharedInstance].ertcEngine setAudioEncoderType:ERTCAudioEncodeType_AAC];
    
    // 设置填充模式及本地预览
    self.vcsLocalPlayView.fillMode = ERTCVideoFillMode_Fill;
    [[ErtcHelper sharedInstance].ertcEngine setLocalPreview:self.vcsLocalPlayView withRegionID:0];
    
    // 设置事件代理
    [ErtcHelper sharedInstance].ertcEngine.delegate = self;
    
    // 进入房间
    [[ErtcHelper sharedInstance].ertcEngine enterRoom:self.ertcParam withScene:ERTCAppScene_VideoCall];
}
```

- 设备端呼叫客户端：设备端发起呼叫，开发者的服务端会接收到该设备的呼叫消息，服务端通过长链接将呼叫消息通知给客户端，客户端使用如上方法进入对应房间即可。**应用与服务端的长链接需要开发者自行开发实现。**
- 客户端呼叫设备端：客户端发起呼叫，客户端使用如上方法进入房间，再邀请设备入会。

### 邀请设备入会

如果是客户端（手机端）发起视频通话，客户端进入房间成功后，再邀请设备进入对应房间。

示例代码如下：

ErtcRoomViewController.m

```
#pragma mark - ERTC代理 事件回调

/// 用户加入房间成功，加入房间成功后将收到回调
/// @param result 加入房间耗时
- (void)onEnterRoomSuccess:(NSInteger)result {
    NSLog(@"ERTCDelegate onEnterRoomSuccess result: %ld", (long)result);
    // 客户端发起视频通话，邀请设备入会
    if (self.isClientCallDevice) {
        [self inviteDeviceEnterMeeting];
    }
}

......

/** 邀请设备入会 */
- (void)inviteDeviceEnterMeeting {
    [EZOpenSDK inviteDeviceEnterMeeting:self.ertcParam.appID ertcToken:self.ertcHttpToken roomId:self.ertcParam.roomId deviceSerial:self.cameraInfo.deviceSerial cameraNo:self.cameraInfo.cameraNo account:self.ertcParam.userId completion:^(NSError * _Nonnull error) {
        if (error) {
            NSLog(@"inviteDeviceEnterMeeting error:%@", error);
            [EZToast show:@"邀请设备入会失败"];
            [self hangUpAction];// 挂断，退出房间
        }
    }];
}
```

### 取消邀请设备入会

如果是客户端（手机端）发起视频通话，客户端进入房间后，设备端一直未接听，需设置一个超时时间。超时后，取消邀请设备入会。

示例代码如下：

ErtcRoomViewController.m

```
/** 启动计时器 */
- (void)startUpdateTimer {
    if (!_videoTalkTimer) {
        _videoTalkTimer = [NSTimer scheduledTimerWithTimeInterval:1.0 target:self selector:@selector(timerStart:) userInfo:nil repeats:YES];
    }
}

- (void)timerStart:(NSTimer *)timer {
    NSInteger currentTime = ++self.videoTalkSecond;
    self.videoTalkTimeLabel.text = [NSString stringWithFormat:@"%02d:%02d", (int)currentTime/60, (int)currentTime % 60];
    // 15秒后设备仍未进入会议的话，视频通话失败，退出房间
    if (self.videoTalkSecond > 15 && !self.isRemoteUserEnterRoom) {
        [EZToast show:@"设备端无人接听，视频通话结束"];
        [self stopUpdateTimer];
        [self hangUpAction];
    }
}

/**
 * 挂断
 */
- (void)hangUpAction {
    // 客户端呼叫设备 && 设备未接听，取消邀请设备入会
    if (self.isClientCallDevice && !self.isRemoteUserEnterRoom) {
        [self cancelInviteDeviceEnterMeeting];
    }
    [self releaseERTC];
    [self.navigationController popViewControllerAnimated:YES];
}

/** 取消邀请设备入会 */
- (void)cancelInviteDeviceEnterMeeting {
    [EZOpenSDK cancelInviteDeviceEnterMeeting:self.ertcParam.appID ertcToken:self.ertcHttpToken roomId:self.ertcParam.roomId deviceSerial:self.cameraInfo.deviceSerial cameraNo:self.cameraInfo.cameraNo account:self.ertcParam.userId completion:^(NSError * _Nonnull error) {
        if (error) {
            NSLog(@"inviteDeviceEnterMeeting error:%@", error);
            [EZToast show:@"取消邀请设备入会失败"];
        }
    }];
}
```

## 订阅设备端码流

ERTCEngine设置代理后，在-onUserVideoAvailable:available:方法中订阅设备端的码流。

示例代码如下：

ErtcRoomViewController.m

```
#pragma mark - ERTC代理 事件回调

/// 用户加入房间成功，加入房间成功后将收到回调
/// @param result 加入房间耗时
- (void)onEnterRoomSuccess:(NSInteger)result {
    NSLog(@"ERTCDelegate onEnterRoomSuccess result: %ld", (long)result);
    // 客户端发起视频通话，邀请设备入会
    if (self.isClientCallDevice) {
        [self inviteDeviceEnterMeeting];
    }
}

/// 用户退出房间，非主动退出房间才会收到该回调
/// @param reason 退出房间原因
- (void)onExitRoom:(ERTCSelfExitReason)reason {
    NSLog(@"ERTCDelegate onEnterRoomSuccess reason: %lu", (unsigned long)reason);
}

/// 远端用户进入房间成功回调，进入房间时将会收到所有已在房间内用户加入房间的回调
/// @param userId 用户id
- (void)onRemoteUserEnterRoom:(NSString *)userId {
    NSLog(@"ERTCDelegate onRemoteUserEnterRoom RemoteUser加入房间成功 userId:%@", userId);
    self.isRemoteUserEnterRoom = YES;
    self.vcsRemotePlayView.hidden = NO;
}

/// 远端用户离开房间
/// @param userId 用户ID
/// @param reason 离开原因，0表示用户主动退出房间，1表示用户超时退出。
- (void)onRemoteUserLeaveRoom:(NSString *)userId reason:(NSInteger)reason {
    NSLog(@"ERTCDelegate onRemoteUserLeaveRoom RemoteUser离开房间成功 userId:%@", userId);
    [EZToast show:@"设备端已挂断，视频通话结束"];
    [self hangUpAction];
}

/// 远端用户打开或关闭视频流的回调
/// @param userId 远端用户id
/// @param available true-视频可用 false-视频不可用
- (void)onUserVideoAvailable:(NSString *)userId available:(BOOL)available {
    NSLog(@"ERTCDelegate onUserVideoAvailable RemoteUser userId:%@, available:%@", userId, available ? @"YES" : @"NO");
    BOOL value = [[self.remoteUserDict objectForKey:userId] boolValue];
    if (value == available) {
        NSLog(@"ERTCDelegate duplicate message, filtered");
        return;
    }
    
    [self.remoteUserDict setValue:[NSNumber numberWithBool:available] forKey:userId];
    if (available) {
        // 订阅远端视频
        self.vcsRemotePlayView.fillMode = ERTCVideoFillMode_Fit;
        [[ErtcHelper sharedInstance].ertcEngine subscribe:YES forUser:userId withStream:ERTCVideoStreamTypeBig];
        [[ErtcHelper sharedInstance].ertcEngine setRemoteView:self.vcsRemotePlayView forUser:userId withRegionID:0];
    } else {
        [[ErtcHelper sharedInstance].ertcEngine subscribe:NO forUser:userId withStream:ERTCVideoStreamTypeBig];
        [[ErtcHelper sharedInstance].ertcEngine setRemoteView:nil forUser:userId withRegionID:0];
    }
}

- (void)onError:(NSInteger)errCode {
    // ERTC错误码文档：https://open.ys7.com/help/1822
    NSLog(@"ERTCDelegate onError: %ld", (long)errCode);
    if (errCode == ERTC_ERR_SERVICE_AccesstokenInvalid) {
        [EZToast show:@"ertcToken异常，请更新token后重新入会。"];
    } else {
        [EZToast show:[NSString stringWithFormat:@"errorCode:%ld", (long)errCode]];
    }
    [self hangUpAction];
}
```

## 视频通话工具栏功能

### 麦克风开关

ERTCEngine.h

```
/// 开启本地音频模块并推流，调用成功后其它用户将收到 onUserAudioAvailable
/// @param enable YES-开启 NO-关闭
- (void)enableLocalAudio:(BOOL)enable;
```

### 扬声器/耳机

ERTCEngine.h

```
/// 打开扬声器，默认扬声器是开的
/// @param enableSpeaker 打开扬声器
- (void)setEnableSpeakerphone:(BOOL)enableSpeaker;
```

### 挂断

示例代码：

```
if ([ErtcHelper sharedInstance].ertcEngine) {
        [[ErtcHelper sharedInstance].ertcEngine exitRoom];
        [ErtcHelper sharedInstance].ertcEngine.delegate = nil;
        [ErtcHelper sharedInstance].ertcEngine = nil;
        [ERTCEngine destroySharedIntance];
    }
```

### 前后摄像头切换

ERTCEngine.h

```
/// 切换前后置摄像头
- (void)switchCamera;
```

### 摄像头禁用/取消禁用

ERTCEngine.h

```
/// 是否开启本地采集并推流。加入房间前调用则加入后自动推流，加入房间后调用则直接推流. 调用后其它用户将收到 onUserVideoAvailable
/// @param enable YES-开启推流 NO-关闭推流
- (void)enableLocalVideo:(BOOL)enable;
```