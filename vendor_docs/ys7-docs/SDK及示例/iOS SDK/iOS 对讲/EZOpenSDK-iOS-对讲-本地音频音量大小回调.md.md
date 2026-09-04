# EZOpenSDK-iOS-对讲-本地音频音量大小回调.md

> EZOpenSDK-iOS-对讲-本地音频音量大小回调

> 更新时间: 2026-06-02T14:03:51.000+08:00

> 文档ID: 4106 | 来源树: SDK及示例

---

# 本地音频音量大小回调

对讲时，将手机本地采集到的音频音量大小回调给应用层。开发者可根据对讲音量值做对讲音柱效果的展示，提升用户体验。

### 1. 第一步设置对讲本地音频音量大小监听

EZPlayer.h

```
/**
 * 设置对讲本地采集音量大小回调时间间隔；默认为0，响度不回调；单位：秒
 * 在调用startVoiceTalk前生效
 * 设置后会通过`-player:didReceivedVoiceTalkLoudness:`代理方法进行回调
 *
 * @param interval 回调时间间隔
 */
- (void)setVoiceTalkLoudnessInterval:(float)interval;
```

示例代码：

```
@interface EZRealPlayViewController ()<EZPlayerDelegate, UIScrollViewDelegate> {
}
@property (nonatomic, strong) EZPlayer * talkPlayer;///< talkPlayer要定义成属性

@end

@implementation EZRealPlayViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    ...
    // 创建对讲播放器，也可以直接使用EZPlayer类中的方法创建
    _talkPlayer = [EZOpenSDK createPlayerWithDeviceSerial:deviceSerial cameraNo:cameraNo];

    // 设置后才可以处理音频音量回调代理方法
    _talkPlayer.delegate = self;
    // 设置对讲本地采集音量大小回调时间间隔
    [_talkPlayer setVoiceTalkLoudnessInterval:0.15f];

    // IPC设备发起对讲
    [_talkPlayer startVoiceTalk];
    ...
}

@end
```

### 2.第二步实现代理方法

EZPlayer.h

```
/**
 * 对讲时采集时的音频大小，必须调用`EZPlayer.setVoiceTalkLoudnessInterval`设置回调时间间隔后才会有回调
 * 注意：回调的音量单位为分贝，均为负数。在数字音频处理中，音量通常以dBFS（分贝满刻度）为单位来表示。
 * 0dBFS表示信号的最大可能幅度，即满量程刻度。由于有效的信号数值通常小于这个最大值，取对数后得到的值通常是负数。
 * 建议：(-90, -40)音量显示1格，[-40, -35)音量显示2格，[-35, -30)音量显示3格，[-30, -20)音量显示4格，[-20, 0)音量显示5格
 * 如需其他层级的音量显示效果，需开发者自行调试
 *
 * @param player 播放器对象
 * @param loudness 音频大小 [-90 ，0]
 */
- (void)player:(EZPlayer *)player didReceivedVoiceTalkLoudness:(float)loudness;
```

示例代码：

```
- (void)player:(EZPlayer *)player didReceivedVoiceTalkLoudness:(float)loudness {
    NSLog(@"didReceivedVoiceTalkLoudness--->%f", loudness);
    self.localLoudnessLabel.text = [NSString stringWithFormat:@"本地音频音量：%0.2f分贝", loudness];
}
```