# EZOpenSDK-android-权限配置.md

> EZOpenSDK-android-权限配置

> 更新时间: 2026-06-02T14:03:35.000+08:00

> 文档ID: 4150 | 来源树: SDK及示例

---

# 权限配置

权限配置是在工程的AndroidManifest.xml文件中进行配置。

## Activity注册

添加如下activity定义，用于EZOpenSDK中间页显示，包含登录、开通云存储等。

```
<activity
    android:name="com.videogo.main.EzvizWebViewActivity"
    android:screenOrientation="portrait"
    android:configChanges="orientation|keyboardHidden">
</activity>
```

## 权限配置

```
<!-- 以下是sdk所需权限 -->
<!-- 基础功能所需权限 -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<!-- 配网所需权限 -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CHANGE_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE" />
<!-- 对讲所需权限 -->
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- 以上是sdk所需权限 -->

<!-- 以下是demo所需权限 -->
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
<uses-permission
android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS"
tools:ignore="ProtectedPermissions" />
<uses-permission
android:name="android.permission.READ_LOGS"
tools:ignore="ProtectedPermissions" />
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<!-- 以上是demo所需权限 -->
```