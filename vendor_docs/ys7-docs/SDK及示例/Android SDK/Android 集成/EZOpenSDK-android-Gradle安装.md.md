# EZOpenSDK-android-Gradle安装.md

> EZOpenSDK-android-Gradle安装

> 更新时间: 2026-07-30T16:36:59.000+08:00

> 文档ID: 4149 | 来源树: SDK及示例

---

# Gradle 安装

## 使用Gradle依赖下载

### 1. 项目根目录下的build.gradle配置

```
buildscript {
    ...
    repositories {
        ...
        // 添加maven仓库
        mavenCentral()
    }

    dependencies {
        ...
    }
}
```

### 2. app下的build.gradle配置

```
android {
    ...
    sourceSets {
        main {
            jniLibs.srcDirs = ['libs'] // 指定so文件路径
        }
    }
    defaultConfig {
        ...
        ndk {
            abiFilters "armeabi-v7a", "arm64-v8a" // 支持64位架构
        }
        ...
    }
}

dependencies {
    /*萤石SDK核心模块，必须依赖*/
    implementation 'io.github.ezviz-open:ezviz-sdk:5.30'
    // 4.19.0版本之后需要自行依赖okhttp和gson库
    implementation 'com.squareup.okhttp3:okhttp:3.12.1'
    implementation 'com.google.code.gson:gson:2.8.5'

    ...
 }
```

### 3. 混淆文件配置

SDK在打包时不能混淆，需要在项目app下的proguard-rules.pro文件中添加以下内容

```
#*******************************************************************#
#**********         以下是SDK不能混淆的内容            *********#
#*******************************************************************#

#========SDK对外接口=======#
-keep class com.ezviz.opensdk.** { *;}

#========以下是hik二方库=======#
-dontwarn com.ezviz.**
-keep class com.ezviz.** { *;}

-dontwarn com.ez.**
-keep class com.ez.** { *;}

-dontwarn com.hc.CASClient.**
-keep class com.hc.CASClient.** { *;}

-dontwarn com.videogo.**
-keep class com.videogo.** { *;}

-dontwarn com.hik.TTSClient.**
-keep class com.hik.TTSClient.** { *;}

-dontwarn com.hik.stunclient.**
-keep class com.hik.stunclient.** { *;}

-dontwarn com.hik.streamclient.**
-keep class com.hik.streamclient.** { *;}

-dontwarn com.hikvision.sadp.**
-keep class com.hikvision.sadp.** { *;}

-dontwarn com.hikvision.netsdk.**
-keep class com.hikvision.netsdk.** { *;}

-dontwarn com.neutral.netsdk.**
-keep class com.neutral.netsdk.** { *;}

-dontwarn com.hikvision.audio.**
-keep class com.hikvision.audio.** { *;}

-dontwarn com.mediaplayer.audio.**
-keep class com.mediaplayer.audio.** { *;}

-dontwarn com.hikvision.wifi.**
-keep class com.hikvision.wifi.** { *;}

-dontwarn com.hikvision.keyprotect.**
-keep class com.hikvision.keyprotect.** { *;}

-dontwarn com.hikvision.audio.**
-keep class com.hikvision.audio.** { *;}

-dontwarn org.MediaPlayer.PlayM4.**
-keep class org.MediaPlayer.PlayM4.** { *;}
#========以上是hik二方库=======#

#========以下是第三方开源库=======#
# JNA
-dontwarn com.sun.jna.**
-keep class com.sun.jna.** { *;}

# Gson
-keepattributes *Annotation*
-keep class sun.misc.Unsafe { *; }
-keep class com.idea.fifaalarmclock.entity.***
-keep class com.google.gson.stream.** { *; }

# OkHttp
# JSR 305 annotations are for embedding nullability information.
-dontwarn javax.annotation.**
# A resource is loaded with a relative path so the package of this class must be preserved.
-keepnames class okhttp3.internal.publicsuffix.PublicSuffixDatabase
# Animal Sniffer compileOnly dependency to ensure APIs are compatible with older versions of Java.
-dontwarn org.codehaus.mojo.animal_sniffer.*
# OkHttp platform used only on JVM and when Conscrypt dependency is available.
-dontwarn okhttp3.internal.platform.ConscryptPlatform
# 必须额外加的，否则编译无法通过
-dontwarn okio.**


## Glide
-dontwarn com.bumptech.glide.**
-keep class com.bumptech.glide.**{*;}
-keep public class * implements com.bumptech.glide.module.GlideModule
-keep public class * extends com.bumptech.glide.AppGlideModule
-keep public enum com.bumptech.glide.load.resource.bitmap.ImageHeaderParser$** {
  **[] $VALUES;
  public *;
 }


#========以上是第三方开源库=======#
```