# EZOpenSDK-harmony-预览-清晰度切换.md

> EZOpenSDK-harmony-预览-清晰度切换

> 更新时间: 2026-06-02T14:03:56.000+08:00

> 文档ID: 4196 | 来源树: SDK及示例

---

# 清晰度切换

一般摄像头支持多种视频清晰度，比如：标清、高清、超清、极清等清晰度，可以让设备端推送不同清晰度的流进行清晰度切换；
由于设备端一般只会推送同一个清晰度的流，因此当多人同时观看，如果有单个客户端切换清晰度，所有客户端的观看清晰度都会同时变化。

### 设备支持的清晰度数据

取流成功后，SDK会通过EZPlayerCallback的didReceivedMessage回调方法通知，当messageCode = EZMessageCode.PLAYER\_REALPLAY\_START时，调用如下api可获取设备详情EZDeviceDetailPublicInfo对象，该对象中包含 清晰度数据列表 字段videoQualityInfos  
  
EZPlayer

```
/**
 * 获取设备部分详情信息（出画面后才有回调）
 * @param callback
 */
getDeviceDetailInfo(callback: (info: EZDeviceDetailPublicInfo | null) => void);
```

示例代码：

```
// 取流详情数据
deviceDetailPublicInfo: EZDeviceDetailPublicInfo | null = null

private playerCallback: EZPlayerCallback = {
  /*
    * 播放器播放成功消息回调
    */
  didReceivedMessage: async (messageCode: number) => {
    EZLog.debug(this.TAG, `player didReceivedMessage messageCode: ${messageCode}`)
    if (messageCode == EZMessageCode.PLAYER_REALPLAY_START) {
      // do something
      this.player?.getDeviceDetailInfo((info) => {
        this.deviceDetailPublicInfo = info
      })
    }
  },
  /*
    * 播放器播放失败消息回调
    */
  didPlayFailed: async (error: EZError) => {
    // do something
  }
}
```

**注意：**
EZOpenSDK类中的 getDeviceList 和 getDeviceInfo 等api中获取到的videoQualityInfos值不一定准确，不建议使用。

### 清晰度设置

```
/**
 * 设置设备通道的清晰度
 * @param deviceSerial  设备序列号
 * @param cameraNo      通道号
 * @param videoLevel    通道清晰度，0-流畅，1-均衡，2-高清，3-超清
 * @param callback      回调，无error表示设置成功
 */
static setVideoLevel(deviceSerial: string, cameraNo: number, videoLevel: EZVideoLevelType,
  callback: (error: EZError) => void);
```

示例代码：

```
// 如果是正在播放时调用该接口，设置清晰度成功以后必须让EZPlayer调用stopRealPlay再调用startRealPlay重新取流才成完成画面清晰度的切换
EZOpenSDK.setVideoLevel(this.cameraInfo!.deviceSerial, this.cameraInfo!.cameraNo, videoLevelType, async (error) => {
  if (error) {
    EZToastUtil.showToast(`${error.message}`)
    return
  }
  await this.player?.stopRealPlay()

  // 刷新缓存数据
  this.cameraInfo!.videoLevel = videoLevelType
  emitter.emit({ eventId: EmitterEvents.EZDeviceListPageRefresh })
  this.currentQualityTitle = EZBusinessTool.getDeviceQualityTitle(videoLevelType)

  await this.player?.startRealPlay()
})
```