# EZOpenSDK-iOS-下载安装.md

> EZOpenSDK-iOS-下载安装

> 更新时间: 2026-06-02T14:03:45.000+08:00

> 文档ID: 4075 | 来源树: SDK及示例

---

# 下载安装

## 下载SDK静态库安装

### 1. [下载SDK](https://open.ys7.com/mobile/download.html?type=app)并解压缩

![iOS SDK下载图片](https://resource.eziot.com/group2/M00/00/FA/CtwQF2eSHieAOU2aAAB_uxWb8Is319.png)
  
  
解压缩后，目录如下：  
![iOS SDK解压后图片](https://resource.eziot.com/group2/M00/00/FA/CtwQFmeSII2AfFc7AABCXPK3Atc158.png)

**解压缩后，请务必先阅读【README(集成必读).txt】文件，可以帮助您更快地开始集成开发并避免集成过程中可能出现的各种问题。**

### 2. 在您的项目工程中，导入EZOpenSDK库

鼠标左键按住EZOpenSDK文件夹不放，拖动到项目根目录下，如图  
![iOS SDK集成图片](https://resource.eziot.com/group2/M00/00/FA/CtwQFmeSIuOAdaLNAAEBW1HL4wE779.png)

松开鼠标左键，如下勾选选项  
![iOS SDK集成图片](https://resource.eziot.com/group2/M00/00/FA/CtwQF2eSI96AfRGOAACFJgpglQM543.png)

点击右下角Finish按钮，完成后如下图  
![iOS SDK集成图片](https://resource.eziot.com/group2/M00/00/FA/CtwQF2eSJIaAQsCZAADjE26YruQ730.png)

### 3. 导入系统依赖库libsqlite3.0、CoreMedia、AudioToolbox、VideoToolbox、GLKit、OpenAL、MobileCoreServices、AVFoundation、CoreTelephony、SystemConfiguration、libc++、libiconv、libbz2、libz

**注意**：Xcode15移除了libiconv.2.4.0.tbd，所以SDK自v5.4起，更换为libiconv.tbd

![list of frameworks](https://resource.eziot.com/group2/M00/00/AB/CtwQFmTsBdOADXZlAACyHep9GR8377.png)

### 4. 添加Other Linker Flags **-ObjC**

**注意区分大小写。**  
![Other Linker Flags](https://img.ys7.com/group2/M00/3E/A7/CmGCBFepfsKAXzRyAAB-dHRcot4070.jpg)

### 5. 关闭目标target的bitcode功能

![关闭bitcode图片](https://resource.eziot.com/group2/M00/00/FA/CtwQFmeSGsOAfCbpAACg7_dboTs273.png)

### 6. 配置完成