# 可编程设备最佳实践-app端使用.md

> 可编程设备最佳实践-app端使用

> 更新时间: 2025-08-20T13:45:19.000+08:00

> 文档ID: 4493 | 来源树: 云接入

---

# 7. APP端使用

## 7.1 开发者测试

### 1. 前端环境准备

1）下载nvm安装包（https://github.com/coreybutler/nvm-windows/releases）
![](https://resource.eziot.com/group2/M00/01/08/CtwQFmiVmUyAJSkQAAG4cwyjabM551.png)

测试demo下载链接：https://izhstatic.ys7.com/vasp-openweb/1754896229562\_demo源码.zip

2）安装nvm，双击下载的nvm-setup.exe

a)安装路径避免包含空格（如C:\nvm）

b)安装完成后重启终端(win+r，打开cmd)，输入nvm -v验证是否成功

![](https://resource.eziot.com/group2/M00/01/07/CtwQF2iVmeCAHMZIAAAImMNixlw955.png)

3）下载nodejs

a)终端执行命令nvm install 16.19.0下载nodejs

b)下载后执行命令nvm list查看是否下载成功

c)执行命令node -v，查看nodejs是否正常

![](https://resource.eziot.com/group2/M00/01/08/CtwQFmiVmg6Ad8KeAABC025E95E553.png)

### 2. 执行代码

1）终端进入项目文件夹，执行命令npm install下载依赖（demo参考：）

2）执行命令npm run start运行代码

3） 浏览器访问地址http://localhost:3000? deviceSerial=（设备序列号）&appKey=（被授权方appKey）

注意：括号内需要手动填写

### 3. 在页面测试功能响应

## 7.2 用户使用前置准备

- 设备开发界面内，选择设备管理，申请授权code

![](https://resource.eziot.com/group2/M00/01/08/CtwQFmiVmvmAGAEfAABeZjnHkPU889.jpg)

## 7.3 App端使用流程

登录萤石app-选择可编程设备-进入设备设置页面-点击设备软件包-点击设备授权Code-输入授权码-点击“确定更换”进行软件包安装
![](https://resource.eziot.com/group2/M00/01/07/CtwQF2iVm1WAS3G2AABTbfe6qkI408.jpg)