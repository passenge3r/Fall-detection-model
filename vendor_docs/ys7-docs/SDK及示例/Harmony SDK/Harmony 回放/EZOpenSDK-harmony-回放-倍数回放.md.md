# EZOpenSDK-harmony-回放-倍数回放.md

> EZOpenSDK-harmony-回放-倍数回放

> 更新时间: 2026-07-13T10:36:15.000+08:00

> 文档ID: 4203 | 来源树: SDK及示例

---

# 倍数回放

针对视频可以进行多种倍速播放。api如下

EZPlayer

```
/**
 * 回放倍数播放（倍数后播放没有声音，这个是正常的，不是问题）
 sd卡及云存储倍速回放接口（不能在didReceivedMessage方法中调用此方法，因为setPlaybackRate也会触发player:didReceivedMessage:方法，会陷入死循环导致回放卡顿）
  1.支持抽帧快放的设备最高支持16倍速快放（所有取流方式，包括P2P）
  2.不支持抽帧快放的设备，仅支持内外网直连快放，最高支持8倍
  3.HCNetSDK取流没有快放概念，全速推流，只改变播放库速率
  4.注意区别：
  老SD卡回放以及HCNetSDK回放，设置完通过返回值返回成功还是失败，没有其他消息
  新协议的云存储回放以及支持seek、continue的设备d新SD卡回放，设置完通过返回值返回成功还是失败，如果成功，
  则后续还有一条EZVideoPlayerMessageStart异步消息表示成功再次取流
  返回其他错误码表示失败 (新协议云存储和新SD卡回放返回EZ_ERROR_NEED_RETRY 表示需要重试）

  * @param rate 回放速度，具体参考 EZ_PLAY_BACK_RATE
  * @param mode 回放时的抽帧控制，当前仅云存储支持。0： 4倍速全帧，8倍速以上抽帧   1：抽帧   2：全帧  （如设备回放当前不支持，传入0即可）
  * returns true/false
  */
async setPlaybackRate(rate: EZPlaybackRate, mode: number): Promise<boolean>;
```

## 云存储录像倍数回放

支持0.5/1/2/4/8/16/32倍速，选项固定。

## SD卡录像倍数回放

SD卡录像倍数回放跟设备能力集相关，倍速选项根据设备能力集动态渲染。

通过 `EZBusinessTool.getSDCardPlaybackRates(deviceInfo, cameraInfo, streamFetchType)` 获取设备实际支持的倍速列表，UI 仅展示设备支持的选项。返回 null 表示不支持倍速回放。

> 注：`EZBusinessTool` 是 Demo 工程中的工具类，非 SDK 类，开发者需自行实现或复制该方法。

**获取倍速选项列表示例**：

```
// 点击倍速按钮时，获取设备支持的倍速列表渲染 UI
let streamFetchType = await this.player?.getStreamFetchType() ?? -1
let rates = EZBusinessTool.getSDCardPlaybackRates(this.deviceInfo, this.cameraInfo, streamFetchType)
if (rates == null) {
  // 设备不支持倍速回放
  return
}
// 展示倍速选择面板，使用 rates 数组渲染选项
// ...
```

**设置倍速示例**：

```
// 用户选择倍速后调用
let ret = await this.player?.setPlaybackRate(playbackRate, 0)
if (ret) {
  // 切换成功，更新倍速按钮文本
} else {
  // 切换失败
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
 *        1.1.2 getPlaybackMaxSpeed = 0（原始值-1被转化为0）：默认支持1、4、8、16倍；= 1：不支持倍数；= 4：支持1、4；= 8：支持1、4、8；= 16：支持1、4、8、16
 *    1.2 如果不支持，判断是否内网直连(streamFetchType==2) && 支持内网直连倍数(isSupportDirectInnerRelaySpeed)
 *        - 是：返回 1、4、8 倍数
 *        - 否：返回 null，表示不支持倍数回放
 */
static getSDCardPlaybackRates(deviceInfo: EZDeviceInfo, cameraInfo: EZCameraInfo, streamFetchType: number): EZPlaybackRate[] | null {
  let isSupportRate = EZBusinessTool.isSupportPlaybackRate(deviceInfo, cameraInfo)

  if (isSupportRate) {
    let rates: EZPlaybackRate[] = []
    let supportSmallSpeed = EzvizSupportKit.isSupportPlaybackSmallSpeed(deviceInfo.abilities)
    if (supportSmallSpeed) {
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_1_2)
    }
    let maxSpeed = EzvizSupportKit.getPlaybackMaxSpeed(deviceInfo.abilities)
    if (maxSpeed == 1) {
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_1)
    } else if (maxSpeed == 0) {
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_1)
      if (supportSmallSpeed) { rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_2) }
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_4)
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_8)
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_16)
    } else {
      rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_1)
      if (supportSmallSpeed) { rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_2) }
      if (maxSpeed >= 4) { rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_4) }
      if (maxSpeed >= 8) { rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_8) }
      if (maxSpeed >= 16) { rates.push(EZPlaybackRate.EZOPENSDK_PLAY_RATE_16) }
    }
    return rates
  } else {
    let supportDirectInner = EZBusinessTool.isSupportDirectInnerRelaySpeed(deviceInfo, cameraInfo)
    if (streamFetchType == 2 && supportDirectInner) {
      return [EZPlaybackRate.EZOPENSDK_PLAY_RATE_1, EZPlaybackRate.EZOPENSDK_PLAY_RATE_4, EZPlaybackRate.EZOPENSDK_PLAY_RATE_8]
    }
    return null
  }
}
```