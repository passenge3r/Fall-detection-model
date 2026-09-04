# EZOpenSDK-iOS-预览-清晰度自适应.md

> EZOpenSDK-iOS-预览-清晰度自适应

> 更新时间: 2026-06-04T10:22:08.000+08:00

> 文档ID: 4083 | 来源树: SDK及示例

---

# 清晰度自适应

当设备支持该能力时，开发者可以在自己应用中的该设备清晰度选择列表中加入【自动】选项；  
当用户选择【自动】时，SDK会监测网络状况，通知升档降档消息给应用层，开发者再调用SDK中的指定api来切换设备清晰度，整个过程预览不断流。

## 一、判断设备是否支持 自动清晰度

EZDeviceInfo.h

```
/// 是否支持自动清晰度
@property (nonatomic) BOOL isSupportDeviceAutoVideolevel;
```

**注意：该属性为计算型属性，需调用后再查看该属性值；调试模式下查看EZDeviceInfo对象的该属性值是不准确的**

## 二、加入【自动】选项、开启网络检测开关

开发者可以在支持该能力集的清晰度列表选项中加入【自动】选项，

![自动清晰度UI](https://resource.eziot.com/group1/M00/01/82/CtwQE2fFTMeAdGDtAAN-WkSK2j4383.png)

**当终端用户选择【自动】后，再开启网络检测开关并重新开始取流，并将该设备的自动清晰度开启状态缓存于本地，下次对设备进行取流时，EZPlayer初始化的时候须打开网络检测开关**，api如下  
  
EZPlayer.h

```
/**
 * 是否开启自动清晰度网络检测开关，startRealPlay之前调用；此api未调用时，不会回调以下消息 
 * EZPlayer - EZMessageCode - PLAYER_VIDEO_LEVEL_AUTO_IMPROVE  网络好，会回调此消息，建议切换高一级清晰度
 * EZPlayer - EZMessageCode - PLAYER_VIDEO_LEVEL_AUTO_REDUCE   网络差，会回调此消息，建议切换低一级清晰度
 */
- (void)enableDeviceAutoVideoLevel;
```

示例代码如下：

```
// 本地缓存设备当前状态是否是"自动清晰度"，不支持的不用管理状态
if (isSupportDeviceAutoVideolevel) {
    [kUserDefaults setBool:_isQulityModeAuto forKey:[NSString stringWithFormat:@"QualityAuto_%@", self.deviceInfo.deviceSerial]];
    [kUserDefaults synchronize];
}
// 选择"自动"，重新取流，接收到通知消息后再切换清晰度；
[self.player stopRealPlay];
[self.player enableDeviceAutoVideoLevel];
[self.player startRealPlay];
```

## 三、清晰度升档降档通知回调

EZPlayer代理方法player:didReceivedMessage:会接收到升档:PLAYER\_VIDEO\_LEVEL\_AUTO\_IMPROVE 或 降档:PLAYER\_VIDEO\_LEVEL\_AUTO\_REDUCE 消息回调后，调用如下api来切换清晰度

```
/**
 *  设置设备通道的清晰度(非强制，两个及以上客户端同时在取流时无法设置，会返回失败)
 *  录制过程中不能调用此接口，否则会导致录制视频异常
 *
 *  @param deviceSerial 设备序列号
 *  @param cameraNo     通道号
 *  @param videoLevel   通道清晰度，0-流畅，1-均衡，2-高清，3-超清，4-极清，5-3K，6-4K
 *  @param completion   回调block，无error表示设置成功
 *  @see 如果是正在播放时调用该接口，设置清晰度成功以后必须让EZPlayer调用stopRealPlay再调用startRealPlay重新取流才成完成画面清晰度的切换。
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)setVideoLevelAuto:(NSString *)deviceSerial
                                   cameraNo:(NSInteger)cameraNo
                                 videoLevel:(EZVideoLevelType)videoLevel
                                 completion:(void (^)(NSError * __nullable error))completion;
```

- 当接收到升档:PLAYER\_VIDEO\_LEVEL\_AUTO\_IMPROVE消息时，调用如上api设置高一级的清晰度
- 当接收到降档:PLAYER\_VIDEO\_LEVEL\_AUTO\_REDUCE消息时，调用如上api设置低一级的清晰度

**注意事项：见如上api方法注释**

示例代码：

```
/** 播放器播放成功消息回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    NSLog(@"player: %@, didReceivedMessage: %d", player, (int)messageCode);
    if (messageCode == PLAYER_REALPLAY_START) {

    } else if (messageCode == PLAYER_VIDEO_LEVEL_AUTO_IMPROVE) {// 清晰度升档，EZPlayer.enableDeviceAutoVideolevel开关打开后才会有此回调
        if (_isQulityModeAuto && !self.localRecordButton.selected) {// 录制的时候不能切换，涉及到分辨率的变化，会影响转码
            NSInteger higherVideoLevel = [EZBusinessTool getHigherVideoLevel:self.cameraInfo.videoLevel deviceDetailPublicInfo:self.deviceDetailPublicInfo];
            if (higherVideoLevel > self.cameraInfo.videoLevel) {
                [self qualityAutoAction:[EZVideoQualityInfo initWithVideoQualityName:[EZBusinessTool getDeviceQualityTitle:higherVideoLevel] videoLevel:higherVideoLevel]];
            }
        }
        
    } else if (messageCode == PLAYER_VIDEO_LEVEL_AUTO_REDUCE) {// 清晰度降档，EZPlayer.enableDeviceAutoVideolevel开关打开后才会有此回调
        if (_isQulityModeAuto && !self.localRecordButton.selected) {
            NSInteger lowerVideoLevel = [EZBusinessTool getLowerVideoLevel:self.cameraInfo.videoLevel deviceDetailPublicInfo:self.deviceDetailPublicInfo];
            if (lowerVideoLevel < self.cameraInfo.videoLevel) {
                [self qualityAutoAction:[EZVideoQualityInfo initWithVideoQualityName:[EZBusinessTool getDeviceQualityTitle:lowerVideoLevel] videoLevel:lowerVideoLevel]];
            }
        }
    }

/** 自动清晰度切换Action */
- (void)qualityAutoAction:(EZVideoQualityInfo *)videoQualityInfo {
    [EZOPENSDK setVideoLevelAuto:_cameraInfo.deviceSerial
                        cameraNo:_cameraInfo.cameraNo
                      videoLevel:(EZVideoLevelType)videoQualityInfo.videoLevel
                      completion:^(NSError *error) {
        if (error) {
            // 失败不用处理
            return;
        }
        
        _cameraInfo.videoLevel = videoQualityInfo.videoLevel;
        [self.qualityButton setTitle:videoQualityInfo.videoQualityName forState:UIControlStateNormal];
    }];
}
```