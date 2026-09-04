# ERTC SDK集成说明- iOS.md

>  接入文档

> 更新时间: 2026-05-25T16:36:32.000+08:00

> 文档ID: 1824 | 来源树: 音视频

---

# ERTC SDK接入文档

#### Updated Time 2023/09/01

# 接入必读

- 本SDK只包含真机调试的功能，不支持任何模拟器的调试。
- SDK支持的最低系统版本为iOS 12。

# 名词解释

| 名词 | 注解 |
| --- | --- |
| appID | appID的申请可以参阅: [官网](https://open.ys7.com/console/application.html) |
| token | 资源 token，由server返回给client用于认证 |
| apiUrl | 平台地址，接入方设置 |

# 隐私声明

## 1、权限说明

| 功能模块 | 权限名称 | 使用目的 |
| --- | --- | --- |
| 视频通话 | Camera 相机 | 用于本地视频采集 |
| 语音通话 | Microphone 麦克风 | 用于语音通话功能，采集音频 |

# 安装SDK

SDK安装目前只支持手动集成。

## 下载安装

1. 下载SDK并解压缩
2. 导入SDK库到主工程中（如图所示）;  
   ![file tree](https://resource.eziot.com/group1/M00/00/E0/CtwQEmTwKXuAPADJAABLU_69jM0051.png)
3. 添加资源文件com.hri.hpc.mobile.ios.player.metallib到主工程中

**注意**：资源文件可以从ERTC.framework中添加

![list of frameworks](https://resource.eziot.com/group1/M00/00/E0/CtwQE2TwKYGAG5zaAADVYcqS-88928.png)

4. 添加Other Linker Flags **-ObjC**  
   **注意区分大小写。**  
   ![Other Linker Flags](https://img.ys7.com/group2/M00/3E/A7/CmGCBFepfsKAXzRyAAB-dHRcot4070.jpg)
5. 关闭目标target的bitcode功能
   Build Settings->Enable Bitcode设置为NO
6. 配置完成

# 权限配置

权限配置是在工程的info.plist文件中进行配置。在Xcode工程的文件导航栏中找到该文件，右键选择Open As -> Source Code,在合适位置添加对应权限代码。

1. 麦克风权限：
   如果需要使用语音通话功能，就需要配置麦克风权限。务必在发起音视频通话前向iOS系统申请麦克风权限，否则将导致第一次语音通话异常。

```
<key>NSMicrophoneUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机麦克风</string>
```

2. 摄像头权限：
   如果使用视频通话功能，就需要套配置摄像头权限。

```
<key>NSCameraUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机摄像头用与视频通话</string>
```

# 实现音视频通话

## 1 初始化

```
   ERTCEngineConfig *config = [ERTCEngineConfig new];
   [ERTCEngine createWithConfig:config instanceBlock:^(ERTCEngine * _Nullable instance, NSError * _Nullable error) {
        self.engine = instance;
   }];
```

## 2 加入房间

```
    ERTCParam *param = [ERTCParam new];
    param.roomId = "房间号";
    param.userId = "用户ID";
    param.token = "资源 token";
    param.apiUrl = "开放平台地址";
    param.appID = "应用标识/应用 ID";
    [self.engine enterRoom:param withScene:ERTCAppScene_VideoCall];
```

## 3 开启麦克风

```
[self.engine enableLocalAudio:YES];
```

## 4 开启摄像头

```
[self.engine enableLocalVideo:YES];
[self.engine setLocalPreview:localView withRegionID:0]
```

## 5 开启屏幕共享

```
[self.engine startScreenShareWithName:@"ys_mt_meeting_screenShare".lc_T withResultBlock:^(NSInteger ret) {
       
    } andEndedBlock:^{
       
    }];
```

## 6 订阅远端视频

```
[self.engine subscribe:YES forUser:_playInfoModel.account.id_p withStream:ERTCVideoStreamTypeBig];//订阅码流
 [self.engine setRemoteView:self.playerView forUser:_playInfoModel.account.id_p withRegionID:0];//设置窗口
```

## 7 订阅远端屏幕共享

```
 [self.engine subscribe:YES forUser:@"" withStream:ERTCVideoStreamTypeSub];//订阅码流
 [self.engine setRemoteView:self.remoteShareView.playView forUser:@"" withRegionID:0];//设置窗口
```