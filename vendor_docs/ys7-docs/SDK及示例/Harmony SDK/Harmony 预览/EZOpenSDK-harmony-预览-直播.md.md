# EZOpenSDK-harmony-预览-直播.md

> EZOpenSDK-harmony-预览-直播

> 更新时间: 2026-06-02T14:03:55.000+08:00

> 文档ID: 4192 | 来源树: SDK及示例

---

# 直播

## 预览

对摄像机实时取流，查看当前摄像机的实时直播画面。

### 1. 第一步创建播放器

可调用EZOpenSDK.ets头文件中的 createPlayer 方法创建播放器。

### 2. 第二步配置播放器

播放器创建完成后需要进行设置回调，设置播放视图，验证码设置等配置。

### 3. 第三步开始播放

调用startRealPlay开启直播

### 4. 第四步结束播放

调用stopRealPlay结束直播

### 5.第五步释放播放器

调用release释放播放器

  

#### 完整示例代码如下：

```
@Entry
@Component
struct EZRealPlayPage {
  // 预览播放器
  player: EZPlayer | null = null
  previewPlayerComponentID: string = 'PreviewPlayerComponentID'

  aboutToAppear() {
    // do something
    // 创建播放器，也可以直接使用EZPlayer类中的方法创建
    this.player = EZOpenSDK.createPlayer(this.cameraInfo.deviceSerial, this.cameraInfo.cameraNo)

    // 可选，建议设置，设置后才可以处理代理方法
    this.player.setPlayerCallback(this.playerCallback)

    // 可选，设备开启了视频/图片加密功能后需设置，可根据EZDeviceInfo的isEncrypt属性判断
    this.player.setPlayVerifyCode(verifyCode)

    // 设置用以展示直播画面的视图
    this.player?.setPlayerView(this.previewPlayerComponentID)

    // 开始直播
    await this.player?.startRealPlay()
  }

  async onPageHide(): Promise<void> {
    // 退到后台或者跳转到其他页面后，停止取流
    await this.player?.stopRealPlay()
    // do something
  }

  async aboutToDisappear(): Promise<void> {
    await EZOpenSDK.releasePlayer(this.player)
  }

  // ------------------------ 播放器回调函数 player callback ------------------------

  private playerCallback: EZPlayerCallback = {
    /*
    * 播放器播放成功消息回调
    */
    didReceivedMessage: async (messageCode: number) => {
      EZLog.debug(this.TAG, `player didReceivedMessage messageCode: ${messageCode}`)
      if (messageCode == EZMessageCode.PLAYER_REALPLAY_START) {// 预览播放开始
        // do something
      }
    },
    /*
    * 播放器播放失败消息回调
    */
    didPlayFailed: async (error: EZError) => {
      // do something
      // 如果是需要验证码或者是验证码错误
      if (error.code == EZErrorCode.EZ_SDK_NEED_VALIDATECODE) {
        // do something
      } else if (error.code == EZErrorCode.EZ_SDK_VALIDATECODE_NOT_MATCH) {
        // do something
      } else {
        EZToastUtil.showToast(`error code is ${error.code}`)
        this.errorMessage = $r('app.string.device_play_fail', `${error.code}`)
        this.isErrorMessageShow = true
        this.isPlaying = false
      }
    }
  }

}
```

  

### 说明

1. 可调用EZOpenSDK.setVideoLevel接口设置视频清晰度，此调节可以在视频播放前设置也可以在视频播放成功后设置。视频播放成功后设置了清晰度，需要先停止播放stopRealPlay，然后重新开启播放startRealPlay才能生效。
2. 开始播放之后在didReceivedMessage中会收到播放开始的消息；失败会在didPlayFailed收到错误码，如果是错误码EZErrorCode.EZ\_SDK\_NEED\_VALIDATECODE = 400035(需要设备验证码)或者EZErrorCode.EZ\_SDK\_VALIDATECODE\_NOT\_MATCH = 400036（设备验证码不匹配），需要开发者自己处理让用户输入验证密码，然后调用EZPlayer.setPlayVerifyCode设置密码，然后重新启动播放。
3. 同一设备需要开启不同功能（直播/回放/对讲）的播放器时，需要分别对每个功能创建一个播放器。播放器的功能是单一的。
4. 电池设备取流1分钟后会进入休眠，导致取流链路断开。如需继续预览，需调用平台接口来唤醒设备，保持设备不休眠。具体实现方案如下：
   - 判断是否是电池设备。可通过EZDeviceInfo.getSupportInt(322)获取，(0)不使用电池 (1)一块电池 (2)两块电池
   - 如果是电池设备，创建一个定时器，每隔50秒调用[平台接口-唤醒设备](https://open.ys7.com/help/1529)来唤醒设备。

## 播放器窗口大小设置

播放器窗口大小设置有多种方法，任选其一即可。

### 方法一

IPC摄像头的画面尺寸通常采用16:9的固定宽高比，因此可以直接将窗口的显示比例设定为16:9。Demo工程采用此方案。

### 方法二

监听EZPlayer播放器消息通知，获取画面宽高，宽高相除得到宽高比，取流成功后才会回调。

EZRealPlayPage.ets

```
  // ------------------------ 播放器回调函数 player callback ------------------------

  private playerCallback: EZPlayerCallback = {
    /*
     * 播放器播放成功消息回调
     */
    didReceivedMessage: async (messageCode: number) => {
      EZLog.debug(this.TAG, `player didReceivedMessage messageCode: ${messageCode}`)
      if (messageCode == EZMessageCode.PLAYER_REALPLAY_START) {
        // do something
      } else if (messageCode == EZMessageCode.PLAYER_VIDEO_SIZE_CHANGED) {
        // 获取画面宽高，电子放大的时候需要用
        let mVideoWidth = await this.player?.getVideoWidth() ?? 0
        let mVideoHeight = await this.player?.getVideoHeight() ?? 0
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

### 方法三

调用EZPlayer类中的getDeviceDetailInfo方法获取画面宽高，宽高相除得到宽高比，取流成功后调用有效。

EZRealPlayPage.ets

```
  // ------------------------ 播放器回调函数 player callback ------------------------

  private playerCallback: EZPlayerCallback = {
    /*
     * 播放器播放成功消息回调
     */
    didReceivedMessage: async (messageCode: number) => {
      EZLog.debug(this.TAG, `player didReceivedMessage messageCode: ${messageCode}`)
      if (messageCode == EZMessageCode.PLAYER_REALPLAY_START) {
         this.player?.getDeviceDetailInfo((info) => {
          let mVideoWidth = info.videoWidth
          let mVideoHeight = info.videoHeight
        })
      } 
      // do something
    },
    /*
     * 播放器播放失败消息回调
     */
    didPlayFailed: async (error: EZError) => {
      // do something
    }
  }
```

### 方法四

调用EzvizSupportKit类中的getSupportValue方法获取设备能力集，传入位数16 获取画面宽高比，设备信息获取后即可调用，不需要等到取流成功之后。

EzvizSupportKit.ts

```
static getSupportValue(index: number, abilityArray: Array<string>): string;
```

代码示例：

```
let videoRatio = EzvizSupportKit.getSupportValue(16, deviceInfo.abilities)// 获取的值为16-9，代表16:9
```