# EZOpenSDK-harmony-回放-录像下载.md

> EZOpenSDK-harmony-回放-录像下载

> 更新时间: 2026-06-02T14:03:58.000+08:00

> 文档ID: 4202 | 来源树: SDK及示例

---

# 录像下载

可以将设备上SD卡中的录像片段 或 存储于云端的录像片段下载到手机终端。  
SDK只能将录像片段下载到应用沙盒中，下载的录像文件格式为MP4；如果需要将沙盒中的录像转存到相册中，需要开发者自行实现，可参考demo工程。

## 云存储录像下载

### 1. 第一步创建下载任务

创建EZCloudStreamDownload对象。

### 2. 第二步设置回调函数

setStreamDownloadCallback方法设置监听。

### 3. 第三步加入下载队列

start开始下载。

示例代码：

```
/**
 * 云存储录像下载 download video from ezviz cloud
 * @param cloudFile
 */
async startDownloadCloudVideo(cloudFile: EZCloudRecordFile) {
  if (!cloudFile) {
    EZLog.error(this.TAG, 'startDownloadCloudVideo error: deviceFile is null')
    return
  }
  if (!this.cameraInfo) {
    EZLog.error(this.TAG, 'startDownloadCloudVideo error: cameraInfo is null')
    return
  }
  const index = this.playbackRecords?.indexOf(cloudFile)
  let convertCloudFile = this.playbackConvertRecords![index!] as CloudRecordFile
  if (convertCloudFile.isRecordDownloading()) {
    EZToastUtil.showToast($r('app.string.playback_record_download_downloading'))
    return
  }
  // 录像文件下载路径
  const strRecordFilePath = `${Constants.PATH_CloudRecord}/cloud_${Date.now()}.mp4`
  // 获取文件的父目录路径
  const parentDirPath = strRecordFilePath.substring(0, strRecordFilePath.lastIndexOf('/'))
  // 父级文件夹创建
  if (!fs.accessSync(parentDirPath)) {
    await fs.mkdir(parentDirPath)
    EZLog.info(this.TAG, `startDownloadCloudVideo Directory created successfully(${parentDirPath})`)
  }
  // 1、创建下载器
  const ezCloudStreamDownload = new EZCloudStreamDownload()
  await ezCloudStreamDownload.prepareDownloadParams(strRecordFilePath, cloudFile)
  // 设置验证码
  let verifyCode = PreferenceUtil.getString(getContext(this), this.cameraInfo.deviceSerial) as string
  ezCloudStreamDownload.setSecretKey(verifyCode)
  // 2、设置下载监听
  ezCloudStreamDownload.setStreamDownloadCallback({
    onSuccess: async (filepath: string): Promise<void> => {
      // do something
    },
    onError: (error: EZStreamDownloadError): void => {
      // do something
    },
    onErrorCode: (code: number): void => {
      // do something
    },
    onDownloadingSize: (downloadSize: number): void => {
      // do something
    }
  })
  // 3、开始下载
  EZToastUtil.showToast($r('app.string.playback_record_download_start'))
  convertCloudFile.recordDownloadStatus = RecordDownloadStatus.Record_Download_Start
  await ezCloudStreamDownload.start()
}
```

## SD卡录像下载

不是所有的设备都支持SD卡录像下载，需要设备支持如下能力集

| 序号 | 字段 | 名称 | 能力集值说明 |
| --- | --- | --- | --- |
| 260 | support\_replay\_download | 是否支持SD卡录像下载 | 0-不支持，1-支持 |

开发时可使用如下api进行判断设备是否支持SD卡录像下载，支持的话再在录像下载页面显示下载图标。

EZBusinessTool.ets

```
/** 是否支持SD卡录像下载 */
static isSupportSDRecordDownload(deviceInfo: EZDeviceInfo | null, cameraInfo: EZCameraInfo | null) {
  if (!deviceInfo) {
    return false
  }
  return EzvizSupportKit.isSupportSDRecordDownload(deviceInfo.abilities)
}
```

  

确定设备支持SD卡录像下载后，创建下载任务并开始下载。

### 1. 第一步创建下载任务

创建EZDeviceStreamDownload对象。

### 2. 第二步设置回调函数

setStreamDownloadCallback方法设置监听。

### 3. 第三步加入下载队列

start开始下载。

示例代码：

```
/**
 * SD卡录像下载 download video from ezviz device
 * @param deviceFile
 */
async startDownloadDeviceVideo(deviceFile: EZDeviceRecordFile) {
  if (!deviceFile) {
    EZLog.error(this.TAG, 'startDownloadDeviceVideo error: deviceFile is null')
    return
  }
  if (!this.cameraInfo) {
    EZLog.error(this.TAG, 'startDownloadDeviceVideo error: cameraInfo is null')
    return
  }
  const index = this.playbackRecords?.indexOf(deviceFile)
  let convertDeviceFile = this.playbackConvertRecords![index!] as DeviceRecordFile
  if (convertDeviceFile.isRecordDownloading()) {
    EZToastUtil.showToast($r('app.string.playback_record_download_downloading'))
    return
  }
  // 录像文件下载路径
  const strRecordFilePath = `${Constants.PATH_DeviceRecord}/device_${Date.now()}.mp4`
  // 获取文件的父目录路径
  const parentDirPath = strRecordFilePath.substring(0, strRecordFilePath.lastIndexOf('/'))
  // 父级文件夹创建
  if (!fs.accessSync(parentDirPath)) {
    await fs.mkdir(parentDirPath)
    EZLog.info(this.TAG, `startDownloadDeviceVideo Directory created successfully(${parentDirPath})`)
  }
  // 1、创建下载器
  const ezDeviceStreamDownload = new EZDeviceStreamDownload()
  await ezDeviceStreamDownload.prepareDownloadParams(strRecordFilePath, this.cameraInfo.deviceSerial,
    this.cameraInfo.cameraNo, deviceFile)
  // 设置验证码
  let verifyCode = PreferenceUtil.getString(getContext(this), this.cameraInfo.deviceSerial) as string
  ezDeviceStreamDownload.setSecretKey(verifyCode)
  // 2、设置下载监听，SD卡录像下载不支持onDownloadingSize下载进度
  ezDeviceStreamDownload.setStreamDownloadCallback({
    onSuccess: async (filepath: string): Promise<void> => {
      // do something
    },
    onError: (error: EZStreamDownloadError): void => {
      // do something
    },
    onErrorCode: (code: number): void => {
      // do something
    }
  })
  // 3、开始下载
  EZToastUtil.showToast($r('app.string.playback_record_download_start'))
  convertDeviceFile.recordDownloadStatus = RecordDownloadStatus.Record_Download_Start
  await ezDeviceStreamDownload.start()
}
```

### 其他注意事项

1. SD卡本地录像不支持onDownloadingSize下载进度回调，只有云存储录像下载才支持。
2. 双目设备录像下载，均需设置downloader.setMultiChannelDevice(true); 详见demo工程代码。
3. 小权限TKToken模式，SD卡录像下载前必须通过downloader.setStreamToken(streamToken) 设置小权限tkToken。