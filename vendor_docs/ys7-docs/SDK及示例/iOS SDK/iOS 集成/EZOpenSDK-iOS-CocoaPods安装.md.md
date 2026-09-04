# EZOpenSDK-iOS-CocoaPods安装.md

> EZOpenSDK-iOS-CocoaPods安装

> 更新时间: 2026-07-30T16:36:53.000+08:00

> 文档ID: 4074 | 来源树: SDK及示例

---

# CocoaPods 安装（推荐）

## 一、CocoaPods（如已安装请跳过第一步）

### 1. 设置 ruby 的软件源

由于默认的 ruby 的软件源(https://rubygems.org/)被墙阻拦导致CocoaPods安装失败，因此需要更新一下 ruby 的源。依次执行如下命令：

```
gem sources -l # (查看当前ruby的源)
gem sources --remove https://rubygems.org/ # (移除当前ruby的源)
gem sources -a https://gems.ruby-china.com
gem sources -l # (再次查看当前ruby的源)

# 显示如下文字表示更新成功。
# *** CURRENT SOURCES ***
# https://gems.ruby-china.com
```

### 2. 升级gem

gem 版本较低也可能导致安装或者升级失败，所以需要升级 gem。使用以下命令：

```
sudo gem update --system
```

### 3. 安装 CocoaPods

检查一下您的 OS X 的版本，若您的 OS X 版本小于等于 10.11，执行下面的命令安装 CocoaPods：

```
sudo gem install cocoapods
```

大于 10.11，使用如下命令安装：

```
sudo gem install -n /usr/local/bin cocoapods
pod setup
```

**注意：安装过程可能会耗时比较长，也有可能受网络状况影响造成失败，需要多次尝试直到成功。**

## 二、使用CocoaPods 安装 SDK

在您项目工程（.xcodeproj）文件同目录下创建一个名为 Podfile 文件。如果您尚未创建 Xcode 项目，请立即创建一个并将其保存到您的本地计算机。

### 1. 创建并编辑Podfile内容如下

```
source 'https://github.com/CocoaPods/Specs.git'

platform :ios, '11.0' #手机的系统
target 'YourProjectTarget' do
  pod 'EZOpenSDK', '~> 5.30'
end
```

### 2. 执行安装命令

```
pod install
```

安装成功以后，会出现如下记录：  
![pod install成功图片](https://resource.eziot.com/group2/M00/00/FA/CtwQF2eSGCaAIUuqAACqzmEm1Ro815.png)

### 3. 导入成功，启动工程

命令执行成功后，会生成 .xcworkspace 文件，恭喜你已成功导入EZOpenSDK iOS SDK。打开.xcworkspace 文件以启动工程（注意：此时不能同时开启.xcodeproj文件），如下图所示。  
![pod installc成功后项目目录](https://resource.eziot.com/group2/M00/00/FA/CtwQF2eSGgWAMzniAABis0EOukA018.png)

### 4. 关闭目标target的bitcode功能

![关闭bitcode图片](https://resource.eziot.com/group2/M00/00/FA/CtwQFmeSGsOAfCbpAACg7_dboTs273.png)

### 5. 安装完成

## CocoaPods相关问题

- **无法更新到最新版本**

  若已经安装了EZOpenSDK SDK，想要更新到最新版本，在Podfile文件的目录下使用以下命令：

```
pod repo update #用于保证本地EZOpenSDK为最新版 pod update
```

- **pod search无法搜索到类库的解决办法（找不到类库）**

  依次执行如下命令：

```
pod setup
rm ~/Library/Caches/CocoaPods/search_index.json
pod search EZOpenSDK
```

- **头文件导包问题**

  导包方式：

```
#import <EZOpenSDKFramework/EZOpenSDKFramework.h>
```

EZOpenSDKFramework.h头文件中已包含了SDK所有的头文件，也可以视情况按需引用。