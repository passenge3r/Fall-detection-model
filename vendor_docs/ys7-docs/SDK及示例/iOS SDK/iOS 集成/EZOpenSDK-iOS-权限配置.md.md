# EZOpenSDK-iOS-权限配置.md

> EZOpenSDK-iOS-权限配置

> 更新时间: 2026-06-02T14:03:45.000+08:00

> 文档ID: 4076 | 来源树: SDK及示例

---

# 权限配置

权限配置是在工程的info.plist文件中进行配置。在Xcode工程的文件导航栏中找到该文件，右键选择Open As -> Source Code，在合适位置添加对应权限代码。

### 1. 相册权限

如果需要使用开放平台播放器录像和截图并保存到相册的功能，就需要配置相册权限。

```
<key>NSPhotoLibraryUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机相册</string>
<key>NSPhotoLibraryAddUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机相册</string>
```

### 2. 麦克风权限

如果需要使用设备对讲功能，就需要配置麦克风权限。务必在发起对讲前向iOS系统申请麦克风权限，否则将导致第一次对讲异常。

```
<key>NSMicrophoneUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机麦克风</string>
```

### 3. 摄像头权限

如果需要仿照demo工程实现扫码添加设备功能，就需要配置摄像头权限。

```
<key>NSCameraUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用手机照相机用于扫码</string>
```

### 4. 本地网络权限 & 定位权限

如果需要仿照demo工程实现AP配网功能，就需要配置本地网络权限。

```
<key>NSLocalNetworkUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用本地网络权限用于wifi配网</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用定位权限用于wifi配网</string>
<key>NSLocationAlwaysUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用定位权限用于wifi配网</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>$(PRODUCT_NAME)需要使用定位权限用于wifi配网</string>
```

### 5. Target-Signing & Capabilities配置

```
添加Access WiFi Information（获取手机连接的WiFi名，配网需要）  
添加Hotspot Configuation（连接指定WiFi，配网需要）  
添加multicast多播能力（局域网设备搜索需要，此能力还需要证书中包含多播能力，申请需要一周时间。如果不使用局域网设备搜索功能，不需要添加此能力）
```

添加完后可以在.entitlements文件中查看。如下  
![entitlements配置](https://resource.eziot.com/group1/M00/01/7A/CtwQE2elqtaANK2TAABZw9FjIJ0813.png)