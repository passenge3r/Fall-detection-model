# EZOpenSDK-iOS-回放-录像下载.md

> EZOpenSDK-iOS-回放-录像下载

> 更新时间: 2026-06-02T14:03:50.000+08:00

> 文档ID: 4087 | 来源树: SDK及示例

---

# 录像下载

可以将设备上SD卡中的录像片段 或 存储于云端的录像片段下载到手机终端。  
SDK只能将录像片段下载到应用沙盒中，下载的录像文件格式为MP4；如果需要将沙盒中的录像转存到相册中，需要开发者自行实现，可参考demo工程。

## 云存储录像下载

### 1. 第一步创建下载任务

可调用EZCloudRecordDownloadTask的initTaskWithID:cloudRecordFile:verifyCode:savePath方法创建下载任务。

### 2. 第二步设置回调函数

setDownloadCallBackWithFinshed:failed:方法设置回调。

### 3. 第三步加入下载队列

addDownloadTask:方法加入下载队列后开始下载。

示例代码：

```
- (void)startCloudRecordDownload:(NSString *)path cloudFile:(EZCloudRecordFile *)cloudFile {
    EZCloudRecordDownloadTask *task = [[EZCloudRecordDownloadTask alloc] initTaskWithID:_selectedIndexPath.row cloudRecordFile:cloudFile verifyCode:self.verifyCode savePath:path];
    // 设置回调函数
    __weak typeof(task) weakTask = task;
    [task setDownloadCallBackWithFinshed:^(EZRecordDownloaderStatus statusCode) {
        __strong typeof(weakTask) strongTask = weakTask;
        NSLog(@"statuCode:%ld", (long)statusCode);
        
        switch (statusCode) {
            case EZRecordDownloaderStatusFinish:
            {
                // do something
            }
                break;
            case EZRecordDownloaderStatusMoreToken:
                // do something
                break;
            default:
                break;
        }
        [[EZRecordDownloader shareInstane] stopDownloadTask:strongTask];
        
    } failed:^(NSError * _Nonnull error) {
        NSLog(@"EZDeviceRecordDownloader error:%@", error);
        __strong typeof(weakTask) strongTask = weakTask;
        // do something
        [[EZRecordDownloader shareInstane] stopDownloadTask:strongTask];
    }];
    
    if (task) {
        // 加入下载队列下载
        int ret = [[EZRecordDownloader shareInstane] addDownloadTask:task];
    }
}
```

## SD卡录像下载

不是所有的设备都支持SD卡录像下载，需要设备支持如下能力集

| 序号 | 字段 | 名称 | 能力集值说明 |
| --- | --- | --- | --- |
| 260 | support\_replay\_download | 是否支持SD卡录像下载 | 0-不支持，1-支持 |

开发时可使用如下api进行判断设备是否支持SD卡录像下载，支持的话再在录像下载页面显示下载图标。

EZBusinessTool.m

```
/** 是否支持SD卡录像下载 */
+ (BOOL)isSupportSDRecordDownload:(EZDeviceInfo *)deviceInfo cameraInfo:(EZCameraInfo *)cameraInfo {
    if ([cameraInfo isKindOfClass:[EZSubDeviceInfo class]]) {
        EZSubDeviceInfo *subDeviceInfo = (EZSubDeviceInfo *)cameraInfo;
        return subDeviceInfo.isSupportSDRecordDownload;
    }
    return deviceInfo.isSupportSDRecordDownload;
}
```

  

确定设备支持SD卡录像下载后，创建下载任务并开始下载。

### 1. 第一步创建下载任务

可调用EZDeviceRecordDownloadTask的initTaskWithID:DeviceRecordFileInfo:verifyCode:savePath:completion:方法创建下载任务。

### 2. 第二步设置回调函数

setDownloadCallBackWithFinshed:failed:方法设置回调。

### 3. 第三步加入下载队列

addDownloadTask:方法加入下载队列后开始下载。

示例代码：

```
- (void)startDeviceRecordDownload:(NSString *)path deviceFile:(EZDeviceRecordFile *)deviceFile {
    // 创建下载任务
    [[EZDeviceRecordDownloadTask alloc] initTaskWithID:_selectedIndexPath.row
                                  DeviceRecordFileInfo:deviceFile
                                          deviceSerial:_cameraInfo.deviceSerial
                                              cameraNo:self.cameraInfo.cameraNo
                                            verifyCode:self.verifyCode
                                              savePath:path
                                            completion:^(EZDeviceRecordDownloadTask * _Nonnull task) {
        // 设置回调函数
        __weak typeof(task) weakTask = task;
        [task setDownloadCallBackWithFinshed:^(EZRecordDownloaderStatus statusCode) {
            __strong typeof(weakTask) strongTask = weakTask;
            NSLog(@"statuCode:%ld", (long)statusCode);
            
            switch (statusCode) {
                case EZRecordDownloaderStatusFinish:
                {
                    // do something
                }
                    break;
                case EZRecordDownloaderStatusMoreToken:
                    // do something
                    break;
                default:
                    
                    break;
            }
            [[EZRecordDownloader shareInstane] stopDownloadTask:strongTask];
        } failed:^(NSError * _Nonnull error) {
            NSLog(@"EZDeviceRecordDownloader error:%@", error);
            __strong typeof(weakTask) strongTask = weakTask;
            
            if (error.code == 395416 || error.code == 380045) {
                [EZToast show:[NSString stringWithFormat:@"SDD Task:%lu-下载限制，达到最大连接数", (long)strongTask.taskID]];
            } else {
                [EZToast show:[NSString stringWithFormat:@"SDD Task:%lu-下载失败", (long)strongTask.taskID]];
            }
            [[EZRecordDownloader shareInstane] stopDownloadTask:strongTask];
        }];
        if (task) {
            // 加入下载队列下载
            int ret = [[EZRecordDownloader shareInstane] addDownloadTask:task];
        }
    }];
}
```

### 其他注意事项

1. SD卡本地录像不支持setDownloadCallBackWithDownloadSize下载进度回调，只有云存储录像下载才支持。
2. 双目设备录像下载，均需设置[task setMultiChannelDevice:YES]; 详见demo工程代码。
3. 小权限TKToken模式，SD卡录像下载前必须通过[task setStreamToken:streamToken] 设置小权限tkToken。