# EZOpenSDK-android-回放-录像下载.md

> EZOpenSDK-android-回放-录像下载

> 更新时间: 2026-06-02T14:03:40.000+08:00

> 文档ID: 4162 | 来源树: SDK及示例

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
private void startDownloadCloudVideo(final EZCloudRecordFile cloudFile) {
    if (cloudFile == null) {
        return;
    }
    final String notificationTitle = "download video from cloud";
    final int notificationId = getUniqueNotificationId();
    showSimpleNotification(mContext, notificationId, notificationTitle, "downloading...click to cancel!", true);
    getTaskManager().submit(() -> {
        String strFileNameWithPath =
          DemoConfig.getRecordsFolder() + "/cloud_" + System.currentTimeMillis() + ".mp4";
        final File file = new File(strFileNameWithPath);
        if (!file.getParentFile().exists()) {
            file.getParentFile().mkdirs();
        }
        final EZCloudStreamDownload ezCloudStreamDownloader = new EZCloudStreamDownload(strFileNameWithPath,
                cloudFile);
        // 云存储录像支持下载进度回调，SD卡录像下载不支持
        ezCloudStreamDownloader.setStreamDownloadCallback(
                new EZStreamDownloadCallbackWithNotify(cloudFile, notificationId, notificationTitle));
        ezCloudStreamDownloader.setSecretKey(DataManager.getInstance().getDeviceSerialVerifyCode(mCameraInfo.getDeviceSerial()));
        ezCloudStreamDownloader.start();
        mDownloadTaskRecordListAbstract.add(new DownloadTaskRecordOfCloud(ezCloudStreamDownloader,
          notificationId));

        toast("started! And you can find download progress from notification bar.");
    });
}
```

## SD卡录像下载

不是所有的设备都支持SD卡录像下载，需要设备支持如下能力集

| 序号 | 字段 | 名称 | 能力集值说明 |
| --- | --- | --- | --- |
| 260 | support\_replay\_download | 是否支持SD卡录像下载 | 0-不支持，1-支持 |

开发时可使用如下api进行判断设备是否支持SD卡录像下载，支持的话再在录像下载页面显示下载图标。

EZBusinessTool.java

```
/**
  * 是否支持SD卡录像下载
  */
public static boolean isSupportSDRecordDownload(EZDeviceInfo deviceInfo, EZCameraInfo cameraInfo) {
    if (cameraInfo instanceof EZSubDeviceInfo) {
        EZSubDeviceInfo subDeviceInfo = (EZSubDeviceInfo) cameraInfo;
        return subDeviceInfo.isSupportSDRecordDownload();
    }
    return deviceInfo.isSupportSDRecordDownload();
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
private void startDownloadDeviceVideo(final EZDeviceRecordFile deviceFile) {
    if (deviceFile == null) {
        return;
    }
    final String notificationTitle = "download video from sdcard";
    final int notificationId = getUniqueNotificationId();
    showSimpleNotification(mContext, notificationId, notificationTitle, "downloading...click to cancel!", true);
    getTaskManager().submit(new Runnable() {
        @Override
        public void run() {
            String strRecordFilePath = DemoConfig.getRecordsFolder() + "/device_" + System.currentTimeMillis() + ".mp4";
            File file = new File(strRecordFilePath);
            if (!file.getParentFile().exists()) {
                file.getParentFile().mkdirs();
            }

            final EZDeviceStreamDownload ezDeviceStreamDownloader = new EZDeviceStreamDownload(strRecordFilePath,
                    mCameraInfo.getDeviceSerial(), mCameraInfo.getCameraNo(), deviceFile);
            ezDeviceStreamDownloader.setStreamDownloadCallback(new EZStreamDownloadCallbackWithNotify(notificationId, notificationTitle));
            ezDeviceStreamDownloader.setSecretKey(DataManager.getInstance().getDeviceSerialVerifyCode(mCameraInfo.getDeviceSerial()));
            ezDeviceStreamDownloader.start();
            mDownloadTaskRecordListAbstract.add(new DownloadTaskRecordOfDevice(ezDeviceStreamDownloader,
                    notificationId));
        }
    });
}
```

### 其他注意事项

1. SD卡本地录像不支持onDownloadingSize下载进度回调，只有云存储录像下载才支持。
2. 双目设备录像下载，均需设置downloader.setMultiChannelDevice(true); 详见demo工程代码。
3. 小权限TKToken模式，SD卡录像下载前必须通过downloader.setStreamToken(streamToken) 设置小权限tkToken。