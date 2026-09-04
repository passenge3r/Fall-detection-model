# EZOpenSDK-iOS-预览-直播.md

> EZOpenSDK-iOS-预览-直播

> 更新时间: 2026-06-02T14:03:46.000+08:00

> 文档ID: 4078 | 来源树: SDK及示例

---

# 直播

## 预览

对摄像机实时取流，查看当前摄像机的实时直播画面。

### 1. 第一步创建播放器

可调用EZOpenSDK.h头文件中的 createPlayerWithDeviceSerial:cameraNo: 方法创建播放器。

### 2. 第二步配置播放器

播放器创建完成后需要进行设置代理，设置播放视图，验证码设置等配置。

### 3. 第三步开始播放

调用startRealPlay开启直播

### 4. 第四步结束播放

调用stopRealPlay结束直播

### 5.第五步释放播放器

调用release释放播放器

  

#### 完整示例代码如下：

```
@interface EZRealPlayViewController ()<EZPlayerDelegate, UIScrollViewDelegate> {
}
@property (nonatomic, strong) EZPlayer *player;///< 预览播放器要定义成属性，定义成变量会无法播放

@end

@implementation EZRealPlayViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // 创建播放器，也可以直接使用EZPlayer类中的方法创建
    _player = [EZOpenSDK createPlayerWithDeviceSerial:deviceSerial cameraNo:cameraNo];

    // 可选，建议设置，设置后才可以处理代理方法
    _player.delegate = self;

    // 可选，设备开启了视频/图片加密功能后需设置，可根据EZDeviceInfo的isEncrypt属性判断
    [_player setPlayVerifyCode:verifyCode];

    // 设置用以展示直播画面的视图
    [_player setPlayerView:playerView];

    // 开始直播
    [_player startRealPlay];
}

- (void)viewDidDisappear:(BOOL)animated {
    NSLog(@"viewDidDisappear");
    [super viewDidDisappear:animated];
    // do something
    // 页面退出或用户主动停止播放时调用stopRealPlay结束直播
    if (_isPlaying) {
        [_player stopRealPlay];
    }
}

- (void)dealloc {
    NSLog(@"%@ dealloc", self.class);
    // 调用release释放播放器
    [EZOpenSDK releasePlayer:_player];
}

#pragma mark - PlayerDelegate Methods 播放器消息回调

/** 播放器播放失败消息回调 */
- (void)player:(EZPlayer *)player didPlayFailed:(NSError *)error {
    NSLog(@"player: %@, didPlayFailed: %@", player, error);
    // 如果是需要验证码或者是验证码错误
    if (error.code == EZ_SDK_NEED_VALIDATECODE) {
        // do something
    } else if (error.code == EZ_SDK_VALIDATECODE_NOT_MATCH) {
        // do something
    } else {
        // do something
    }
    // do something
}

/** 播放器播放成功消息回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    NSLog(@"player: %@, didReceivedMessage: %d", player, (int)messageCode);
    if (messageCode == PLAYER_REALPLAY_START) {// 预览播放开始
        // do something
    }
}

/** 播放器尺寸变化 */
- (void)player:(EZPlayer *)player didDecodedData:(NSData *)data width:(NSInteger)width height:(NSInteger)height {

}

@end
```

  

### 说明

1. 可调用EZOpenSDK.setVideoLevel:cameraNo:videoLevel:completion:接口设置视频清晰度，此调节可以在视频播放前设置也可以在视频播放成功后设置。视频播放成功后设置了清晰度，需要先停止播放stopRealPlay，然后重新开启播放startRealPlay才能生效。
2. 开始播放之后在didReceivedMessageCode:中会收到播放开始的消息；失败会在didPlayFailed:收到错误码，如果是错误码EZ\_SDK\_NEED\_VALIDATECODE = 400035(需要设备验证码)或者EZ\_SDK\_VALIDATECODE\_NOT\_MATCH = 400036（设备验证码不匹配），需要开发者自己处理让用户输入验证密码，然后调用EZPlayer.setPlayVerifyCode:设置密码，然后重新启动播放。
3. 同一设备需要开启不同功能（直播/回放/对讲）的播放器时，需要分别对每个功能创建一个播放器。播放器的功能是单一的。
4. 电池设备取流1分钟后会进入休眠，导致取流链路断开。如需继续预览，需调用平台接口来唤醒设备，保持设备不休眠。具体实现方案如下：
   - 判断是否是电池设备。可通过EZDeviceInfo.getSupportInt(322)获取，(0)不使用电池 (1)一块电池 (2)两块电池
   - 如果是电池设备，创建一个定时器，每隔50秒调用[平台接口-唤醒设备](https://open.ys7.com/help/1529)来唤醒设备。

## 播放器窗口大小设置

播放器窗口大小设置有多种方法，任选其一即可。

### 方法一

IPC摄像头的画面尺寸通常采用16:9的固定宽高比，因此可以直接将窗口的显示比例设定为16:9。Demo工程采用此方案。

### 方法二

实现EZPlayer播放器代理，获取画面宽高，宽高相除得到宽高比，取流成功后才会回调。

EZPlayer.h

```
/**
 *  收到的画面长宽值
 *
 *  @param player 播放器对象
 *  @param height 高度
 *  @param width  宽度
 */
- (void)player:(EZPlayer *)player didReceivedDisplayHeight:(NSInteger)height displayWidth:(NSInteger)width;
```

### 方法三

调用EZPlayer类中的getDeviceDetailInfo方法获取画面宽高，宽高相除得到宽高比，取流成功后调用有效。

EZRealPlayViewController.m

```
/** 播放器播放成功消息回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    [player getDeviceDetailInfo:^(EZDeviceDetailPublicInfo *info) {
        NSInteger videoWidth = info.videoWidth;
        NSInteger videoHeight = info.videoHeight;
    }];
}
```

### 方法四

调用EZDeviceInfo类中的getSupportValue方法获取设备能力集，传入位数16 获取画面宽高比，设备信息获取后即可调用，不需要等到取流成功之后。

EZDeviceInfo.h

```
 * 根据位数获取设备能力集
 * @param index 位数，必须大于0
 *
 * @return 能力值
 */
- (NSString *)getSupportValue:(int)index;
```

代码示例：

```
NSString *videoRatio = [deviceInfo getSupportValue:16];// 获取的值为16-9，代表16:9
```