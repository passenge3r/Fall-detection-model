# EZOpenSDK-iOS-回放-倍数回放.md

> EZOpenSDK-iOS-回放-倍数回放

> 更新时间: 2026-07-13T10:36:09.000+08:00

> 文档ID: 4088 | 来源树: SDK及示例

---

# 倍数回放

针对视频可以进行多种倍速播放。api如下

EZPlayer.h

```
/**
sd卡及云存储倍速回放接口（倍数后播放没有声音，这个是正常的，不是问题）
1.支持抽帧快放的设备最高支持16倍速快放（所有取流方式，包括P2P）
2.不支持抽帧快放的设备，仅支持内外网直连快放，最高支持8倍
3.HCNetSDK取流没有快放概念，全速推流，只改变播放库速率
4.注意区别：
   老SD卡回放以及HCNetSDK回放，设置完通过返回值返回成功还是失败，没有其他消息
   新协议的云存储回放以及支持seek、continue的设备的新SD卡回放，设置完通过返回值返回成功还是失败，如果成功，
   则后续还有一条EZVideoPlayerMessageStart异步消息表示成功再次取流
   返回其他错误码表示失败 (新协议云存储和新SD卡回放返回EZ_ERROR_NEED_RETRY 表示需要重试）

@param rate    回放速度，具体参考 EZ_PLAY_BACK_RATE
@param mode 回放时的抽帧控制，当前仅云存储支持。0： 4倍速全帧，8倍速以上抽帧   1：抽帧   2：全帧  （如设备回放当前不支持，传入0即可）
@return YES/NO
 */
- (BOOL)setPlaybackRate:(EZPlaybackRate) rate mode:(NSUInteger)mode;
```

## 云存储录像倍数回放

支持0.5/1/2/4/8/16/32倍速，选项固定。

## SD卡录像倍数回放

SD卡录像倍数回放跟设备能力集相关，倍速选项根据设备能力集动态渲染。

通过 `[EZBusinessTool getSDCardPlaybackRates:deviceInfo cameraInfo:cameraInfo streamFetchType:streamFetchType]` 获取设备实际支持的倍速列表，UI 仅展示设备支持的选项。返回 nil 表示不支持倍速回放。

> 注：`EZBusinessTool` 是 Demo 工程中的工具类，非 SDK 类，开发者需自行实现或复制该方法。

**获取倍速选项列表示例**：

```
- (void)showSDCardRateBottomMenu {
    int streamFetchType = [self.player getStreamFetchType];
    NSArray<NSNumber *> *rates = [EZBusinessTool getSDCardPlaybackRates:self.deviceInfo cameraInfo:self.cameraInfo streamFetchType:streamFetchType];
    NSArray<NSString *> *rateStrings = [EZBusinessTool getSDCardPlaybackRateStrings:self.deviceInfo cameraInfo:self.cameraInfo streamFetchType:streamFetchType];
    if (!rates || rates.count == 0) {
        [EZToast show:NSLocalizedString(@"device_playbackrate_not_support", @"该设备不支持回放倍率设置")];
        return;
    }
    // 展示倍速选择列表
    // ...
}
```

**设置倍速示例**：

```
- (void)setPlaybackRate:(EZPlaybackRate)rate {
    [_player setPlaybackRate:rate mode:0];
}
```

**EZBusinessTool.getSDCardPlaybackRates 方法**：

```
/**
 * 获取SD卡录像支持的倍数数组
 * 规则：
 * 1. 先判断设备是否支持倍数回放(isSupportPlaybackRate)
 *    1.1 如果支持，通过 isSupportPlaybackSmallSpeed 和 getPlaybackMaxSpeed 获取支持倍数
 *        1.1.1 isSupportPlaybackSmallSpeed = YES：支持0.5、2倍；= NO：不支持0.5、2倍
 *        1.1.2 getPlaybackMaxSpeed = -1：默认支持1、4、8、16倍；= 1：不支持倍数；= 4：支持1、4；= 8：支持1、4、8；= 16：支持1、4、8、16
 *    1.2 如果不支持，判断是否内网直连(streamFetchType==2) && 支持内网直连倍数(isSupportDirectInnerRelaySpeed)
 *        - 是：返回 1、4、8 倍数
 *        - 否：返回 nil，表示不支持倍数回放
 */
+ (NSArray<NSNumber *> *)getSDCardPlaybackRates:(EZDeviceInfo *)deviceInfo cameraInfo:(EZCameraInfo *)cameraInfo streamFetchType:(int)streamFetchType {
    BOOL isSupportPlaybackRate = [self isSupportPlaybackRate:deviceInfo cameraInfo:cameraInfo];
    
    if (isSupportPlaybackRate) {
        NSMutableArray *rates = [NSMutableArray array];
        BOOL supportSmallSpeed = [self isSupportPlaybackSmallSpeed:deviceInfo cameraInfo:cameraInfo];
        if (supportSmallSpeed) {
            [rates addObject:@(EZOPENSDK_PLAY_RATE_1_2)];
        }
        int maxSpeed = [self getPlaybackMaxSpeed:deviceInfo cameraInfo:cameraInfo];
        if (maxSpeed == 1) {
            [rates addObject:@(EZOPENSDK_PLAY_RATE_1)];
        } else if (maxSpeed == 0) {
            [rates addObject:@(EZOPENSDK_PLAY_RATE_1)];
            if (supportSmallSpeed) { [rates addObject:@(EZOPENSDK_PLAY_RATE_2)]; }
            [rates addObject:@(EZOPENSDK_PLAY_RATE_4)];
            [rates addObject:@(EZOPENSDK_PLAY_RATE_8)];
            [rates addObject:@(EZOPENSDK_PLAY_RATE_16)];
        } else {
            [rates addObject:@(EZOPENSDK_PLAY_RATE_1)];
            if (supportSmallSpeed) { [rates addObject:@(EZOPENSDK_PLAY_RATE_2)]; }
            if (maxSpeed >= 4) { [rates addObject:@(EZOPENSDK_PLAY_RATE_4)]; }
            if (maxSpeed >= 8) { [rates addObject:@(EZOPENSDK_PLAY_RATE_8)]; }
            if (maxSpeed >= 16) { [rates addObject:@(EZOPENSDK_PLAY_RATE_16)]; }
        }
        return [rates copy];
    } else {
        BOOL isSupportDirectInnerRelaySpeed = [self isSupportDirectInnerRelaySpeed:deviceInfo cameraInfo:cameraInfo];
        if (streamFetchType == 2 && isSupportDirectInnerRelaySpeed) {
            return @[@(EZOPENSDK_PLAY_RATE_1), @(EZOPENSDK_PLAY_RATE_4), @(EZOPENSDK_PLAY_RATE_8)];
        }
        return nil;
    }
}
```