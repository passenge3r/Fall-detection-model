# EZOpenSDK-iOS-预览-清晰度切换.md

> EZOpenSDK-iOS-预览-清晰度切换

> 更新时间: 2026-06-02T14:03:47.000+08:00

> 文档ID: 4082 | 来源树: SDK及示例

---

# 清晰度切换

一般摄像头支持多种视频清晰度，比如：标清、高清、超清、极清等清晰度，可以让设备端推送不同清晰度的流进行清晰度切换；
由于设备端一般只会推送同一个清晰度的流，因此当多人同时观看，如果有单个客户端切换清晰度，所有客户端的观看清晰度都会同时变化。

## 设备支持的清晰度数据

取流成功后，SDK会通过代理方法player:didReceivedMessage: 回调，当messageCode = PLAYER\_REALPLAY\_START时，调用如下api可获取设备详情EZDeviceDetailPublicInfo对象，该对象中包含 清晰度数据列表 字段videoQualityInfos  
  
EZPlayer.h

```
/**
 * 获取设备部分详情信息（出画面后才有回调）
 *
 * @param complete  设备对象回调
 */
- (void)getDeviceDetailInfo:(void (^)(EZDeviceDetailPublicInfo *info))complete;
```

示例代码：

```
/** 播放器播放成功消息回调 */
- (void)player:(EZPlayer *)player didReceivedMessage:(NSInteger)messageCode {
    NSLog(@"player: %@, didReceivedMessage: %d", player, (int)messageCode);
    if (messageCode == PLAYER_REALPLAY_START) {
        EZWeak(self);
        [_player getDeviceDetailInfo:^(EZDeviceDetailPublicInfo *info) {
            EZStrong(self);
            strongself.deviceDetailPublicInfo = info;
        }];
    }
}
```

**注意：**
EZOpenSDK.h类中的 getDeviceList:pageSize:completion: 和 getDeviceInfo:completion: 等api中获取到的videoQualityInfos值不一定准确，不建议使用。

## 清晰度设置

```
/**
 *  设置设备通道的清晰度
 *
 *  @param deviceSerial 设备序列号
 *  @param cameraNo     通道号
 *  @param videoLevel   通道清晰度，0-流畅，1-均衡，2-高清，3-超清，4-极清，5-3K，6-4K
 *  @param completion   回调block，无error表示设置成功
 *  @see 如果是正在播放时调用该接口，设置清晰度成功以后必须让EZPlayer调用stopRealPlay再调用startRealPlay重新取流才成完成画面清晰度的切换。
 *
 *  @return operation
 */
+ (NSURLSessionDataTask *)setVideoLevel:(NSString *)deviceSerial
                               cameraNo:(NSInteger)cameraNo
                             videoLevel:(EZVideoLevelType)videoLevel
                             completion:(void (^)(NSError * __nullable error))completion;
```

示例代码：

```
    [MBProgressHUD showHUDAddedTo:self.view animated:YES];
    // 如果是正在播放时调用该接口，设置清晰度成功以后必须让EZPlayer调用stopRealPlay再调用startRealPlay重新取流才成完成画面清晰度的切换
    [EZOpenSDK setVideoLevel:_cameraInfo.deviceSerial
                    cameraNo:_cameraInfo.cameraNo
                  videoLevel:(EZVideoLevelType)videoQualityInfo.videoLevel
                  completion:^(NSError *error) {
        [MBProgressHUD hideHUDForView:self.view animated:YES];
        if (error) {
            [self.view makeToast:[NSString stringWithFormat:@"%@", error.description]];
            return;
        }
        [self playerStopRealPlay];
        
        // 本地数据保存 需要更新之前获取到的设备列表信息，开发者自己设置
        _cameraInfo.videoLevel = videoQualityInfo.videoLevel;
        [self.qualityButton setTitle:videoQualityInfo.videoQualityName forState:UIControlStateNormal];
        
        [self playerStartRealPlay];
    }];
```