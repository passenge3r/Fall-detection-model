# EZOpenSDK-iOS-回放-回放.md

> EZOpenSDK-iOS-回放-回放

> 更新时间: 2026-06-02T14:03:49.000+08:00

> 文档ID: 4086 | 来源树: SDK及示例

---

# 回放

对摄像机存储于SD卡、云端的录像进行取流，查看当前摄像机的历史回放画面。

## 录像片段播放

### 1. 第一步创建播放器

可调用EZOpenSDK.h头文件中的 createPlayerWithDeviceSerial:cameraNo: 方法创建播放器。

### 2. 第二步配置播放器

播放器创建完成后需要进行设置代理，设置播放视图，验证码设置等配置。

### 3. 第三步开始播放

调用startPlaybackFromCloud: 或 startPlaybackFromDevice: 开始回放

### 4. 第四步结束播放

调用stopPlayback结束回放

### 5. 第五步释放播放器

调用release释放播放器

完整示例代码如下：

```
@interface EZPlaybackViewController ()<EZPlayerDelegate, UIScrollViewDelegate> {
}
@property (nonatomic, strong) EZPlayer *player;///< 预览播放器要定义成属性，定义成变量会无法播放

@end

@implementation EZPlaybackViewController

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

    // 回放云端存储的视频，cloudFile由searchRecordFileFromCloud:cameraNo:beginTime:endTime:completion:接口获取
    [_player startPlaybackFromCloud:cloudFile];

    // 或者
    // 回放设备上存储的视频，deviceFile由searchRecordFileFromDevice:cameraNo:beginTime:endTime:completion:接口获取
    [_player startPlaybackFromDevice:deviceFile];
}

- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    // do something
    [_player stopPlayback];
}

- (void)dealloc {
    NSLog(@"%@ dealloc", self.class);
    [EZOpenSDK releasePlayer:_player];
    // do something
}

#pragma mark - PlayerDelegate Methods 播放器消息回调

/** 播放失败回调 */
- (void)player:(EZPlayer *)player didPlayFailed:(NSError *)error {
    NSLog(@"player: %@ didPlayFailed: %@", player, error);
    ...
    if (error.code == EZ_SDK_NEED_VALIDATECODE) {// 需要验证码
        // do something
    } else if (error.code == EZ_SDK_VALIDATECODE_NOT_MATCH) {// 验证码错误
        // do something
    } else {
        // do something
    }
}

/** 播放成功回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    NSLog(@"player: %@ didReceivedMessage: %d", player, (int)messageCode);
    if (messageCode == PLAYER_PLAYBACK_START) {
        // do something
    } else if (messageCode == PLAYER_PLAYBACK_STOP) {
        // do something
    }
}

@end
```

  

### 说明

1. 回放需先获取到视频信息，searchRecordFileFromCloud:cameraNo:beginTime:endTime:completion:方法和searchRecordFileFromDevice:cameraNo:beginTime:endTime:completion:方法分别是获取云端视频列表和设备存储视频列表的两个方法。
2. 开始播放之后在didReceivedMessageCode:中会收到播放开始的消息；失败会在didPlayFailed:收到错误码，如果是错误码EZ\_SDK\_NEED\_VALIDATECODE = 400035(需要设备验证码)或者EZ\_SDK\_VALIDATECODE\_NOT\_MATCH = 400036（设备验证码不匹配），需要开发者自己处理让用户输入验证密码，然后调用setPlayVerifyCode:设置密码，重新启动播放。
3. 同一设备需要开启不同功能（直播/回放/对讲）的播放器时，需要分别对每个功能创建一个播放器。播放器的功能是单一的。

**注意**：实际录像回放结束时间可能与录像片段的结束时间有偏差，如果时间点相近则认为回放结束，此为正常现象。

## 多个录像片段连续播放

萤石Demo中演示的录像播放都为单个录像片段的播放。如需实现多个录像片段连续播放，可以将录像片段进行合并。

### SD卡录像

SD卡录像对象为EZDeviceRecordFile

例：如有三个**已按时间先后顺序排列**的SD卡录像片段recordFileA、recordFileB、recordFileC。只需要将recordFileA的结束时间设置为recordFileC的结束时间，再调用[\_player startPlaybackFromDevice:recordFileA];即可实现三个录像片段连续播放。

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

**A**：播放时，创建一个定时器（每秒刷新播放进度、更新UI等）。通过[\_player getOSDTime]获取当前播放画面的时间戳，遍历录像列表并判断该时间戳位于哪个录像片段，将所属片段设置为选中状态。