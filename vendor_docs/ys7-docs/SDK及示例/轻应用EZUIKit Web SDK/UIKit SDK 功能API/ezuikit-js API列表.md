# ezuikit-js API列表

> ezuikit-js API列表

> 更新时间: 2026-05-25T16:44:29.000+08:00

> 文档ID: 4275 | 来源树: SDK及示例

---

# EZUIKit API 接口文档

> 本文档列出 EZUIKitPlayer 实例的全部公开 API。所有异步方法返回 Promise。
>
> 示例中 player 为 new EZUIKitPlayer({...}) 创建的实例。

## 播放控制

| 序号 | 功能 | API | 示例 | 入参（\*为必填） | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 播放 | play(options?) | player.play() | string | { url, accessToken?, token?, unSaveUrl?, showPoster? } | Promise<{ code: 0 | -1 }> | 可传入新的 ezopen 地址和 token 切换播放 |
| 2 | 停止 | stop() | player.stop() | / | Promise | 停止播放并断开取流连接，停止时自动停止录制 |
| 3 | 暂停 | pause() | player.pause() | / | Promise | 仅回放模式支持，暂停时自动停止录制 |
| 4 | 恢复播放 | resume() | player.resume() | / | Promise | 仅回放模式支持 |
| 5 | 切换播放地址 | changePlayUrl(options) | player.changePlayUrl({ url, accessToken }) | { url?, accessToken?, token?, validCode?, deviceSerial?, channelNo?, type?, begin?, end? } | Promise | 切换设备/通道/回放时间等，无需销毁重建 |
| 6 | 跳转 | seek(startTime, endTime?) | player.seek('143000', '235959') | \*startTime: 时间字符串（HHmmss），endTime: 可选 | Promise | 仅回放模式，需设备支持 seek 能力 |
| 7 | 倍速播放 | fast(speed?) | player.fast(2) | speed[number]: 目标倍速（不传则按 x2 递增） | Promise | 支持 0.5/1/2/4/8/16 倍速，其中 8 倍、16 倍只有云存储、云录制模式支持 |
| 8 | 减速播放 | slow(speed?) | player.slow(0.5) | speed[number]: 目标倍速（不传则按 ÷2 递减） | Promise | 与 fast 配对使用 |
| 9 | 获取播放速率 | getPlayRate() | player.getPlayRate() | / | { speed: number } |  |

## 音频控制

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | 开启声音 | openSound() | player.openSound() | / | Promise |  |
| 11 | 关闭声音 | closeSound() | player.closeSound() | / | Promise |  |

## 截图与录制

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | 截图 | capturePicture(name?, callback?, download?) | player.capturePicture('my-pic') | name[string]: 文件名（可选），callback: 回调（可选），download[boolean]: 是否下载 | Promise<{ fileName, fileUint8Array, base64 }> |  |
| 13 | 开始录制 | startSave(name?, secretCode?) | player.startSave('my-video') | name[string]: 文件名（可选），secretCode[string]: 加密验证码（可选） | Promise | 开启水印且非硬解模式下不允许录制 |
| 14 | 停止录制 | stopSave() | player.stopSave() | / | Promise | 停止后自动下载 MP4 文件 |

## 清晰度

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 切换清晰度 | changeVideoLevel(level) | player.changeVideoLevel(2) | \*level[number]: 清晰度等级 0-6 | Promise | 0:流畅 1:标清 2:高清 3:超清 4:极清 5:3K 6:4K，实际可用取决于设备能力 |
| 16 | 获取当前清晰度 | getVideoLevel() | player.getVideoLevel() | / | number |  |
| 17 | 获取支持的清晰度列表 | getVideoLevelList() | player.getVideoLevelList() | / | Array<{ level, name, streamTypeIn }> | 依赖设备报备的清晰度能力集 |

## 对讲

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 18 | 开启对讲 | startTalk() | player.startTalk() | / | / | 需设备支持（能力集 support\_talk 为 1 或 3），需浏览器麦克风权限，需播放器正在播放 |
| 19 | 关闭对讲 | stopTalk() | player.stopTalk() | / | / |  |
| 20 | 获取麦克风权限 | getMicrophonePermission() | player.getMicrophonePermission() | / | Promise<{ code, msg, res }> |  |
| 21 | 获取麦克风列表 | getMicrophonesList() | player.getMicrophonesList() | / | Promise<{ code, msg, res: MediaDeviceInfo[] }> |  |
| 22 | 切换麦克风 | talkSetProfile(options) | player.talkSetProfile({ microphoneId: 'xxx' }) | { microphoneId[string] } | / | 正在对讲时切换会自动重启对讲 |
| 23 | 设置音频增益 | setVolumeGain(volume) | player.setVolumeGain(5) | \*volume[number]: 0-10 | { code, msg } |  |

## 云广播

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | 查询语音列表 | queryVoiceList(params?) | player.queryVoiceList() | { voiceName?, pageStart?, pageSize? } | Promise |  |
| 25 | 下发临时语音 | sendVoiceOnce(data, channelNo?) | player.sendVoiceOnce(voiceFile) | 录音数据，通道号（可选） | Promise |  |
| 26 | 下发默认语音 | sendVoice(fileUrl, channelNo?) | player.sendVoice(url) | 语音文件 URL，通道号（可选） | Promise |  |

## 云台控制（PTZ）

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 27 | 开启云台 | openPtz() | player.openPtz() | / | { code: 0 | -1 } | 移动端非全屏状态不展示云台 |
| 28 | 关闭云台 | closePtz() | player.closePtz() | / | { code: 0 | -1 } |  |
| 29 | 获取云台状态 | getPtzStatus() | player.getPtzStatus() | / | boolean |  |

## 电子放大

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 30 | 开启电子放大 | enableZoom() | player.enableZoom() | / | / |  |
| 31 | 关闭电子放大 | closeZoom() | player.closeZoom() | / | / |  |
| 32 | 放大 | zoomAdd(scale?) | player.zoomAdd(1) | scale[number]: 倍数增量（默认 1） | / | 最大 8.0X |
| 33 | 缩小 | zoomSub(scale?) | player.zoomSub(1) | scale[number]: 倍数减量（默认 1） | / | 最小 1.0X |
| 34 | 切换 2D/3D 模式 | changeZoomType(flag) | player.changeZoomType(true) | \*flag[boolean]: true=3D, false=2D | / |  |
| 35 | 开启 3D 定位 | enable3DZoom() | player.enable3DZoom() | / | Promise | 需设备支持（能力集 support\_3d\_position === "1"），需初始化时 use3DZoom: true |
| 36 | 关闭 3D 定位 | close3DZoom() | player.close3DZoom() | / | Promise |  |

## 鱼眼矫正

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 37 | 设置鱼眼矫正类型 | setFECCorrectType(type, ids?) | player.setFECCorrectType({ place: 3, type: 1 }) | \*{ place, type }, ids: 分屏 canvas id（可选） | / | 壁装(place=1): 0不矫正/1全景/2四分屏/4广角；顶装(place=3): 0不矫正/1全景/4四分屏/5柱状 |
| 38 | 设置 3D 矫正视角 | setFEC3DViewParam(param) | player.setFEC3DViewParam({ port, upDateType, fValue }) | \*{ port, upDateType, fValue } | / |  |
| 39 | 获取 3D 矫正视角 | getFEC3DViewParam(param) | player.getFEC3DViewParam({ port, upDateType }) | \*{ port, upDateType } | / |  |

## 全屏

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 40 | 全屏 | fullscreen() | player.fullscreen() | / | Promise | PC 端浏览器原生全屏，移动端旋转 90° 充满屏幕 |
| 41 | 退出全屏 | exitFullscreen() | player.exitFullscreen() | / | Promise |  |

## 主题与 UI

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 42 | 切换主题 | changeTheme(themeData) | player.changeTheme({ footer: { btnList: [...] } }) | \*string | object: 模板名或 themeData 对象 | / | 切换主题会中断正在进行的录制、对讲、云台操作 |
| 43 | 重置主题 | resetTheme() | player.resetTheme() | / | / |  |

## 其他

| 序号 | 功能 | API | 示例 | 入参 | 返回值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| 44 | 销毁 | destroy() | player.destroy() | / | Promise | 释放所有资源（连接、解码、画布、定时器、事件），无需先调用 stop() |
| 45 | 调整尺寸 | reSize(width, height) | player.reSize(800, 600) | \*width, \*height: 数值或 CSS 字符串 | / | 8.2.0 起支持 CSS 字符串值（如 '100%'） |
| 46 | 获取 OSD 时间 | getOSDTime() | player.getOSDTime() | / | Promise<{ code, data }> | data 为时间戳 |
| 47 | 设置水印 | setWaterMarkFont(options) | 见下方示例 | \*见下方参数表（传 null 关闭水印） | / |  |
| 48 | 设置解密密钥 | setSecretKey(key) | player.setSecretKey('ABCDEF') | \*key[string]: 密钥 | / | 10 秒内调用直接解密，超过 10 秒会重新取流 |
| 49 | 设置全局基准时间 | setGlobalBaseTime(time) | player.setGlobalBaseTime({ year, month, day, hour, min, sec, ms }) | \*时间对象 | / |  |
| 50 | 设置抗锯齿 | setAntialias(flag) | player.setAntialias(2) | \*flag[number]: 0 关闭, 2 开启 | / |  |
| 51 | 设置画面缩放模式 | setScaleMode(mode) | player.setScaleMode(1) | \*mode: 0 铺满 / 1 等比缩放有黑边 / 2 等比裁剪无黑边 | / | 8.2.0+ |
| 52 | 镜像翻转 | setMirrorFlip(command) | player.setMirrorFlip(2) | \*command[number]: 0 上下 / 1 左右 / 2 中心 | / | 需设备支持 |
| 53 | 展示码流信息 | displayStreamInfo(flag) | player.displayStreamInfo(true) | \*flag[boolean]: true 展示 / false 隐藏 | / | 展示码流信息会消耗性能 |
| 54 | 设置日志选项 | setLoggerOptions(options) | player.setLoggerOptions({ level: 'DEBUG' }) | { name?, level?, showTime? } | / |  |
| 55 | 获取设备能力集 | getDeviceCapacity() | player.getDeviceCapacity() | / | Promise |  |
| 56 | 设置显示区域 | setDisplayRegion(left, right, top, bottom) | player.setDisplayRegion(0, 1, 0, 1) | \*left, \*right, \*top, \*bottom: 四个边界值（0-1） | / |  |

### 水印参数详细说明

```
player.setWaterMarkFont({
  fontString: ['EZVIZ', '2026-04-27'],  // *文本信息数组，元素间换行
  startPos: { fX: 0.1, fY: 0.1 },       // 位置，原点左上角，范围 0~1
  fontColor: { fR: 1, fG: 1, fB: 1, fA: 0.7 }, // 颜色，RGBA 范围 0~1
  fontSize: { nFontWidth: 48, nFontHeight: 48 }, // 字体大小
  fontRotate: { fRotateAngle: 45, fFillFullScreen: true }, // 旋转角度，是否平铺
  fontFamily: 'Arial',                   // 字体
  fontNumber: { nRowNumber: 4, nColNumber: 4 },  // 行列数（1-16）
  space: 2,                              // 行间距
});

// 关闭水印
player.setWaterMarkFont(null);
```

## 已废弃 API

以下 API 在历史版本中存在，当前版本已废弃或替换，请使用新 API：

| 旧 API | 替代 API | 废弃版本 | 说明 |
| --- | --- | --- | --- |
| fullScreen() | fullscreen() | 8.2.0 | 注意大小写变化 |
| cancelFullScreen() | exitFullscreen() | 8.2.0 |  |
| browserFullscreen() | fullscreen() | 8.2.0 | 统一为一个全屏 API |
| exitBrowserFullscreen() | exitFullscreen() | 8.2.0 |  |
| isBrowserFullscreen() | isCurrentBrowserFullscreen（属性） | 8.2.0 | 改为属性访问 |
| getDefinition() | getVideoLevel() | 8.0.5 | 清晰度体系重构 |
| setDefinition(type) | changeVideoLevel(level) | 8.0.5 | 参数从 'sd'/'hd' 改为数字 0-6 |
| setPoster(url) | 初始化参数 poster 或 themeData.poster | 9.x |  |
| Zoom.startZoom() | enableZoom() | 9.x | 不再通过 Zoom 子对象调用 |
| Zoom.stopZoom() | closeZoom() | 9.x |  |
| setProfile(options) | talkSetProfile(options) | 9.x | 方法名更明确 |
| theme.changeTheme() | changeTheme() | 8.2.0 | 不再通过 theme 子对象调用 |