# EZOpenSDK-harmony-对讲.md

> EZOpenSDK-harmony-对讲

> 更新时间: 2026-06-02T14:03:59.000+08:00

> 文档ID: 4208 | 来源树: SDK及示例

---

# 对讲

分为全双工对讲和半双工对讲

- 对讲流程需要根据设备的对讲能力进行区分处理。EzvizSupportKit中的isSupportTalk可获取到设备的对讲能力，0-不支持对讲，1-支持全双工对讲，3-支持半双工对讲。
- 同一设备需要开启不同功能（直播/回放/对讲）的播放器时，需要分别对每个功能创建一个播放器。播放器的功能是单一的。

## 全双工对讲

全双工对讲，与半双工对讲对应，指的是通信系统中同时进行双向对讲的方式，它允许对讲的双方可以在同一时刻进行发送和接收语音，而不需要像半双工通信那样交替进行。

### 1. 第一步创建对讲播放器

可调用EZOpenSDK类中的 createPlayer 方法创建对讲播放器。

### 2. 第二步配置对讲播放器

对讲播放器创建完成后需要进行设置handler回调，验证码设置等配置。  
**注意**：v1.1之前对讲播放器需要配置验证码，v1.1起取消了验证码的校验，无须在配置验证码

### 3. 第三步开始对讲

- IPC设备调用startVoiceTalk()开启对讲。
- NVR设备调用startVoiceTalkNeedVoiceChannel(true)开启通道对讲

### 4. 第四步结束对讲

调用stopVoiceTalk结束对讲

### 5. 第五步释放对讲播放器

调用release释放对讲播放器

**示例代码**：

```
@Entry
@Component
struct EZRealPlayPage {
  // 对讲播放器
  talkPlayer: EZPlayer | null = null

  aboutToAppear() {
    // do something

    // 创建播放器，也可以直接使用EZPlayer类中的方法创建
    this.talkPlayer = EZOpenSDK.createPlayer(this.cameraInfo.deviceSerial, this.cameraInfo.cameraNo)

    // 可选，建议设置，设置后才可以处理回调方法
    this.talkPlayer.setPlayerCallback(this.talkPlayerCallback)

    // IPC设备发起对讲
    await this.talkPlayer?.startVoiceTalk()

    // NVR设备发起对讲
    await this.talkPlayer?.startVoiceTalkNeedVoiceChannel(true)

    // do something
  }

  async onPageHide(): Promise<void> {
    // do something
    // 退到后台或者跳转到其他页面后，停止对讲
    await this.talkPlayer?.stopVoiceTalk()
  }

  async aboutToDisappear(): Promise<void> {
    // do something
    await EZOpenSDK.releasePlayer(this.talkPlayer)
  }

  private talkPlayerCallback: EZPlayerCallback = {
    /*
     * 对讲成功消息回调
     */
    didReceivedMessage: async (messageCode: number) => {
      EZLog.debug(this.TAG, `talkPlayer didReceivedMessage messageCode: ${messageCode}`)
      if (messageCode == EZMessageCode.PLAYER_VOICE_TALK_START) {
        // do something
        /**
         非国标设备需要关闭播放器player的声音，设备和手机对讲都是通过talkPlayer来传输音频数据的，所以需要关闭player播放器的声音，避免干扰(萤石设备都是萤石协议，属于非国标设备)
         国标设备不能关闭。国标设备taklPlayer只负责采集手机端的声音，设备端的声音是通过player来播放的 */
        if (this.deviceInfo?.devProtoEnum == 0) {
          await this.talkPlayer?.closeSound()
        }
      } else if (messageCode == EZMessageCode.PLAYER_VOICE_TALK_END) {
        // 对讲结束后把player播放器的声音开回来
        if (this.isOpenSound) {
          await this.player?.openSound()
        }
      } else {
        EZToastUtil.showToast(`didReceivedMessage messageCode：${messageCode}`)
      }
    },
    /*
     * 对讲失败消息回调
     */
    didPlayFailed: (error: EZError) => {
      // do something
      if (error.code == EZErrorCode.EZ_SDK_NOT_SUPPORT_TALK) {
        let msg = getContext().resourceManager.getStringSync($r('app.string.not_support_talk'))
        EZToastUtil.showToast(`${msg}(${error.code})`)
      } else {
        // do something
      }
    }
  }

}
```

## 半双工对讲

半双工对讲，指的是通信系统中交替进行发送和接收语音的模式，与对讲机类似，一方说话期间，其他用户只能接听，只有该用户停止讲话，其他用户才能开始讲话。

半双工设备对讲代码实现与全双工对讲一样。区别是发起成功后，默认模式为 **手机端听-设备端说**。可进行如下操作进行听说模式切换。

```
// 切换到 手机端说-设备端听 模式
this.talkPlayer?.audioTalkPressed(true)

// 切换到 手机端听-设备端说 模式
this.talkPlayer?.audioTalkPressed(false)
```