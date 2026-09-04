# EZOpenSDK-android-回放-倍数回放.md

> EZOpenSDK-android-回放-倍数回放

> 更新时间: 2026-07-13T10:36:03.000+08:00

> 文档ID: 4163 | 来源树: SDK及示例

---

# 倍数回放

针对视频可以进行多种倍速播放。api如下

EZPlayer

```
/**
 * 设置sdcard录像和云存储录像回放速度（倍数后播放没有声音，这个是正常的，不是问题）
 * 此接口为耗时操作，需要在子线程中调用
 * 1.支持抽帧快放的设备最高支持16倍速快放（所有取流方式，包括P2P）
 * 2.不支持抽帧快放的设备，仅支持内外网直连快放，最高支持8倍
 * 3.HCNetSDK取流没有快放概念，全速推流，只改变播放库速率
 *
 * @param rate
 *             EZ_PLAYBACK_RATE_2_1,           // 1/2倍速
 *             EZ_PLAYBACK_RATE_1,             // 1倍速
 *             EZ_PLAYBACK_RATE_2,             // 2倍速
 *             EZ_PLAYBACK_RATE_4,             // 4倍速
 *             EZ_PLAYBACK_RATE_8,             // 8倍速
 *             EZ_PLAYBACK_RATE_16,            // 16倍速
 *             EZ_PLAYBACK_RATE_32;            // 32倍速      云存储回放专用
 * @return 成功返回true, 否则false并恢复成正常速度播放
 * @since V1.8.2
 */
public boolean setPlaybackRate(EZConstants.EZPlaybackRate rate);
```

## 云存储录像倍数回放

支持0.5/1/2/4/8/16/32倍速，选项固定。

## SD卡录像倍数回放

SD卡录像倍数回放跟设备能力集相关，倍速选项根据设备能力集动态渲染。

通过 `EZBusinessTool.getSDCardPlaybackRates(deviceInfo, cameraInfo, streamFetchType)` 获取设备实际支持的倍速列表，UI 仅展示设备支持的选项。返回 null 表示不支持倍速回放。

> 注：`EZBusinessTool` 是 Demo 工程中的工具类，非 SDK 类，开发者需自行实现或复制该方法。

**获取倍速选项列表示例**：

```
private void showSDCardRateBottomMenu(View view) {
    int streamFetchType = mPlaybackPlayer.getStreamFetchType();
    List<EZConstants.EZPlaybackRate> rates = EZBusinessTool.getSDCardPlaybackRates(mDeviceInfo, mCameraInfo, streamFetchType);
    List<String> rateStrings = EZBusinessTool.getSDCardPlaybackRateStrings(mDeviceInfo, mCameraInfo, streamFetchType);
    if (rates == null || rates.isEmpty()) {
        showToast(R.string.device_playbackrate_not_support);
        return;
    }
    // 展示倍速选择列表
    // ...
}
```

**设置倍速示例**：

```
private void setPlaybackRate(EZConstants.EZPlaybackRate targetRateEnum, String targetRateWithX) {
    // 倍数设置为耗时任务，需要在子线程中执行
    new Thread(() -> {
        if (!mPlaybackPlayer.setPlaybackRate(targetRateEnum)) {
            showToast("failed to change to " + targetRateWithX);
        }
    }).start();
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
public static List<EZConstants.EZPlaybackRate> getSDCardPlaybackRates(EZDeviceInfo deviceInfo, EZCameraInfo cameraInfo, int streamFetchType) {
    boolean supportPlaybackRate = isSupportPlaybackRate(deviceInfo, cameraInfo);

    if (supportPlaybackRate) {
        List<EZConstants.EZPlaybackRate> rates = new ArrayList<>();
        boolean supportSmallSpeed = isSupportPlaybackSmallSpeed(deviceInfo, cameraInfo);
        if (supportSmallSpeed) {
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_2_1);
        }
        int maxSpeed = getPlaybackMaxSpeed(deviceInfo, cameraInfo);
        if (maxSpeed == 1) {
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_1);
        } else if (maxSpeed == 0) {
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_1);
            if (supportSmallSpeed) {
                rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_2);
            }
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_4);
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_8);
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_16);
        } else {
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_1);
            if (supportSmallSpeed) {
                rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_2);
            }
            if (maxSpeed >= 4) rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_4);
            if (maxSpeed >= 8) rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_8);
            if (maxSpeed >= 16) rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_16);
        }
        return rates;
    } else {
        boolean supportDirectInner = isSupportDirectInnerRelaySpeed(deviceInfo, cameraInfo);
        if (streamFetchType == 2 && supportDirectInner) {
            List<EZConstants.EZPlaybackRate> rates = new ArrayList<>();
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_1);
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_4);
            rates.add(EZConstants.EZPlaybackRate.EZ_PLAYBACK_RATE_8);
            return rates;
        }
        return null;
    }
}
```