# EZOpenSDK-harmony-回放-SD卡录像封面.md

> EZOpenSDK-harmony-回放-SD卡录像封面

> 更新时间: 2026-06-02T14:03:58.000+08:00

> 文档ID: 4207 | 来源树: SDK及示例

---

# SD卡录像封面

自动抽取画面中的某一帧作为录像的封面图，需要设备能力集支持。

### 1. 第一步SD卡录像封面管理器初始化

传入设备序列号、通道号，初始化SD卡录像封面管理器；设备代理并实现代理方法，示例代码如下：

```
@Entry
@Component
struct EZPlaybackPage {

  aboutToAppear() {
    // do something
    // 3.SD卡本地录像获取初始化
    // 国内支持SD卡录像封面获取，海外不支持
    // 与设备建立链接，获取SD卡录像封面（页面退出的时候必须断开链接，释放资源，见-dealloc方法）
    EZRecordCoverFetcherManager.getInstance().initFetcher(this.cameraInfo.deviceSerial, this.cameraInfo.cameraNo, {
      onFetcherInitSuccess: (): void => {
        EZLog.debug(this.TAG, 'EZRecordCoverFetcherManager onFetcherInitSuccess')
      },
      onFetcherInitFailed: (): void => {
        EZLog.error(this.TAG, 'EZRecordCoverFetcherManager onFetcherInitFailed')
      }
    })

    // do something
  }

}
```

### 2. 第二步请求录像封面

获取到SD卡录像列表后请求录像封面，示例代码如下：

```
/**
 * 请求录像封面
 */
async requestDeviceRecordCover() {
  if (!this.playbackRecords) {
    return
  }
  for (let i = 0; i < this.playbackRecords.length; i++) {
    let recordFile = this.playbackRecords[i] as EZDeviceRecordFile
    recordFile.seq = i // 设置索引，封面回调的时候知道对应哪一个录像
  }
  // 去获取SD卡视频封面
  let isSupportSdCover = EZBusinessTool.isSupportSdCover(this.deviceInfo, this.cameraInfo)
  if (isSupportSdCover) {
    await EZRecordCoverFetcherManager.getInstance()
      .requestRecordCover(this.playbackRecords as Array<EZDeviceRecordFile>, {
        onGetCoverSuccess: async (seq: number, data: Uint8Array): Promise<void> => {
          /**
           * 注意：图片是设备一张一张传回来的，接收到一张就需要局部刷新UI。
           */
          let recordFile = this.playbackConvertRecords![seq] as DeviceRecordFile
          recordFile.pixelMap = await EZBusinessTool.convertToPixelMap(data)
        },
        onGetCoverFailed: (errorCode: number): void => {
          EZLog.error(this.TAG, 'onGetCoverFailed')
        }
      })
  }
}
```

### 3. 页面退出时录像封面管理器释放资源

```
async aboutToDisappear() {
  // do something
  EZRecordCoverFetcherManager.getInstance().stopFetcher()
}
```