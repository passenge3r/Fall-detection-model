# 海康NVR

> 海康NVR

> 更新时间: 2025-03-20T02:14:32.000+08:00

> 文档ID: 2836 | 来源树: 云接入

---

# · 完整接入流程：

## 一. 设备联网与网络配置（联网方式：有线联网）

### **1. 设备联网**

将NVR设备连接有线网络，并将电脑连接至同一局域网。

### **2. 打开设备本地配置页**

通过4200在局域网中搜索目标设备，并获取设备的IP地址。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1OUCAFINkAAFwA4b1GzA234.png)

在浏览器中输入对应IP地址，访问设备本地配置页。并填入用户名密码进行访问。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1OWmANM-VAAipUKPHNZY508.png)

### **3. 网络配置**

建议直接将“自动获取IPV4地址”打钩：如能获取到IP地址、子网掩码、默认网关、DNS服务器地址等参数，说明设备能访问路由器，可通过路由连接外网。（反之如果获取不到参数，可自行检查网络）

![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1Oa-AX7ILAAGiypRBu4Y995.png)

如果要求固定录像机IP地址：则需取消“自动获取IPV4地址”，手动设置参数，如下：

| 参数 | 说明 |
| --- | --- |
| IP地址 | 和摄像机、路由器同一个网段即可（IP地址的前3位保持一致） |
| 子网掩码 | 255.255.255.0 |
| 默认网关 | 路由器IP地址 |
| DNS服务器地址 | 114.114.114.114（首选），8.8.8.8（备用） |
| MTU字节 | 默认1500（可降低至1300） |

![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1OiuAPd4zAAHrfMcy2C8199.png)

## 二. 设备绑定

### **1. 设备启用萤石云**

配置路径：设备本地配置页-配置--网络--高级配置--平台接入

操作：平台接入方式选择“萤石云”，并进行启用。如果“验证码/加密秘钥”是空的，可自行设置6-12位字母（ABCDEF除外）或数字；如果已有（建议修改验证码）。完成后点击保存。
通过这个方式，您可以获取到设备序列号+设备验证码（部分设备可直接生成二维码）。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1OmeATE1RAAFfgfmoV-w050.png)

（注意！海康NVR设备，部分设备如直接通过外接显示器配置，无法获取设备验证码，仅可获取二维码。如您需要设备验证码，则需通过设备本地配置页方式获取。）

### **2. 将设备绑定至萤石开放平台开发者账号下**

这里，为了适配您的应用场景，我们提供了3种方式可支持您进行设备绑定。

    a）设备添加工具。
  
          下载、安装、登录“萤石云视频APP”，进入开放平台工具页面进行设备添加。
![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1GtuAHrnsAARP8CC5EZ0019.png)

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1KseATvakAAFM2oOWblQ467.png)

          如果您需要分享安装团队为您添加设备等，可进一步了解“B端设备添加工具”的应用方案。

    b）萤石开放平台控制台添加。

            登录萤石开放平台控制台：<https://open.ys7.com/console/home.html> ，进入“设备管理器-设备管理”页面，点击“萤石协议接入”按钮，输入设备序列号与验证码进行添加。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1JluAaxYrAAKqegI-qbM673.png)

    c）API设备添加接口添加

            您可通过设备添加接口：<https://open.ys7.com/help/661> 进行设备绑定。