# EZOpenSDK-harmony-录制.md

> EZOpenSDK-harmony-录制

> 更新时间: 2026-07-09T15:28:20.000+08:00

> 文档ID: 4200 | 来源树: SDK及示例

---

# 录制

提供录像能力，集成后可以对当前`预览或回放`画面进行录像，一般是某一段时长录像，并提供保存。

## 开始录制

EZPlayer.ets

```
/**
  * 预览/回放时开始本地录像录制功能
  * 注意：录制的MP4视频时长 和 应用层录制时长 对比是没有意义的。因为应用层计时器一直在走，但是网络异常导致画面卡住 或 设备码流异常（比如帧丢失、跳帧等情况）都会影响录制的时长
  * 验证标准如下：
  * 1、录制的MP4视频播放开始画面中的时间戳 与 实际开始录制时画面中的时间戳是否相近。
  * 2、录制的MP4视频播放结束画面中的时间戳 与 实际结束录制时画面中的时间戳是否相近。
  * @param path  文件存储路径
  * @returns true/false
  */
async startLocalRecordWithPathExt(path: string): Promise<boolean>;
```

**注意**：预览或回放取流过程中才能开始录制功能。

示例代码：

```
/** 开始本地录像Action */
async startLocalRecordAction() {
  // 文件目录、文件创建
  let dirPath = Constants.PATH_LocalRecord
  if (!fs.accessSync(dirPath)) {
    await fs.mkdir(dirPath)
  }
  let fileName = EZTimeUtil.dateFormat(new Date(), 'yyyyMMddHHmmss')
  this.localRecordFilePath = `${dirPath}/${fileName}.mp4`
  await fs.open(this.localRecordFilePath, fs.OpenMode.CREATE)

  // do something 定时器开启

  // 开始录像
  await this.player?.startLocalRecordWithPathExt(this.localRecordFilePath)
}
```

## 结束录制

EZPlayer.ets

```
/**
 * 结束预览/回放录像录制，并生成mp4录制文件
 * @param callback  操作是否成功 true/false
 */
async stopLocalRecordExt(callback: (ret: boolean) => void);
```

示例代码：

```
/** 结束本地录像Action */
async stopLocalRecordAction() {
  await this.player?.stopLocalRecordExt(async (result) => {
    if (result) {
      await EZMediaFileUtil.saveMediaToAlbum(this.localRecordFilePath, photoAccessHelper.PhotoType.VIDEO)
      await fs.unlink(this.localRecordFilePath)
    }
  })
}
```

**注意**：如果用户没有主动调用停止录制，页面退出的时候，开发者需要在onPageHide函数中停止录制。