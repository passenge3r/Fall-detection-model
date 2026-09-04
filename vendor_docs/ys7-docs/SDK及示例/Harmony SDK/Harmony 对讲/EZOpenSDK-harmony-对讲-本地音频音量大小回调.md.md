# EZOpenSDK-harmony-对讲-本地音频音量大小回调.md

> EZOpenSDK-harmony-对讲-本地音频音量大小回调

> 更新时间: 2026-06-02T14:03:59.000+08:00

> 文档ID: 4219 | 来源树: SDK及示例

---

# 本地音频音量大小回调

对讲时，将手机本地采集到的音频音量大小回调给应用层。开发者可根据对讲音量值做对讲音柱效果的展示，提升用户体验。

EZPlayer.ets

```
/**
  * 设置对讲本地采集音量大小回调
  * 在调用startVoiceTalk前生效
  * 注意：回调的音量单位为分贝，均为负数。在数字音频处理中，音量通常以dBFS（分贝满刻度）为单位来表示。
  * 0dBFS表示信号的最大可能幅度，即满量程刻度。由于有效的信号数值通常小于这个最大值，取对数后得到的值通常是负数。
  * 建议：[-90, -40)音量显示1格，[-40, -35)音量显示2格，[-35, -30)音量显示3格，[-30, -20)音量显示4格，[-20, 0]音量显示5格
  * 如需其他层级的音量显示效果，需开发者自行调试
  * @param onLoudnessListener 本地采集音量大小回调
  * @param interval           回调间隔，单位秒，最小值、最大值与采样率有关，若过大或过小，则将自动限制在范围之内
  */
setVoiceTalkLoudnessCallback(onLoudnessListener: OnLoudnessListener, interval: number);
```

示例代码：

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

    // 其他设置
    ......

    // 设置对讲本地采集音量大小回调
    this.talkPlayer.setVoiceTalkLoudnessCallback(this.talkPlayerVoiceTalkLoudnessCallback, 0.15)

    // NVR设备发起对讲
    await this.talkPlayer?.startVoiceTalkNeedVoiceChannel(true)

    // do something
  }

  private talkPlayerVoiceTalkLoudnessCallback: OnLoudnessListener = {
    onReportLoudness: (loudness: number): void => {
      EZLog.info(this.TAG, `VoiceTalkLoudness--->${loudness}`)
      this.voiceTalkLoudness = loudness
    }
  }

}
```