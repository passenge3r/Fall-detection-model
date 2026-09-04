# EZOpenSDK-harmony-下载安装.md

> EZOpenSDK-harmony-下载安装

> 更新时间: 2026-07-30T17:43:47.000+08:00

> 文档ID: 4189 | 来源树: SDK及示例

---

# 下载安装

## 下载SDK

### 1. [下载SDK](https://open.ys7.com/mobile/download.html?type=app)并解压缩

![harmony SDK下载图片](https://resource.eziot.com/group1/M00/01/85/CtwQEmfRdJmAdbzoAADDUMlEnXM996.png)
  
  
解压缩后，目录如下：  
![harmony SDK解压后图片](https://resource.eziot.com/group1/M00/01/85/CtwQE2fRdSiAGQJsAABBgmwLGZo203.png)

**解压缩后，请务必先阅读【README(集成必读).txt】文件，可以帮助您更快地开始集成开发并避免集成过程中可能出现的各种问题。**

### 2. 在您的项目工程中，导入EZOpenSDK库

在自己工程的entry下创建一个libs文件夹，然后将EZOpenSDK.har复制到该文件夹下（如图所示）;  
![file tree](https://resource.eziot.com/group2/M00/00/EE/CtwQF2b9_1SAGPwmAACj7sE8Xsw307.png)

### 3. entry下的oh-package.json5下配置EZOpenSDK依赖

```
"dependencies": {
    "@ezviz/ezopensdk": "file:./libs/EZOpenSDK.har",
    ...
  }
```

### 4. entry下的build-profile.json5下配置

```
"buildOption": {
    "nativeLib": {
      "filter": {
        "enableOverride": true,
      }
    }
  },
```

### 5. 工程下的build-profile.json5下配置

```
{
  "app": {
    "products": [
      {
        ......

        "buildOption": {
          "strictMode": {
            "useNormalizedOHMUrl": true
          }
        }
      }
    ],
    ......
  }
}
```

### 6. 配置完成