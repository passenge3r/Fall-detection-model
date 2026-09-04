# 海康IPC（非4G）

> 海康IPC（非4G）

> 更新时间: 2025-03-20T02:14:27.000+08:00

> 文档ID: 2834 | 来源树: 云接入

---

# · 完整接入流程：

## 一. 设备联网与网络配置（联网方式：有线联网）

### **1. 设备联网**

将IPC设备连接有线网络，并将电脑连接至同一局域网。

### **2. 打开设备本地配置页**

通过4200在局域网中搜索目标设备，并获取设备的IP地址。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1FICATUAdAAFwA4b1GzA358.png)

在浏览器中输入对应IP地址，访问设备本地配置页。并填入用户名密码进行访问。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1FNKAfqD7AAipUKPHNZY673.png)

### **3. 网络配置**

建议直接将“自动获取IPV4地址”打钩：如能获取到IP地址、子网掩码、默认网关、DNS服务器地址等参数，说明设备能访问路由器，可通过路由连接外网。（反之如果获取不到参数，可自行检查网络）

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1FX2AF87bAAGiypRBu4Y716.png)

如果要求固定摄像机IP地址：则需取消“自动获取IPV4地址”，手动设置参数，如下：

| 参数 | 说明 |
| --- | --- |
| IP地址 | 和摄像机、路由器同一个网段即可（IP地址的前3位保持一致） |
| 子网掩码 | 255.255.255.0 |
| 默认网关 | 路由器IP地址 |
| DNS服务器地址 | 114.114.114.114，备用可填写当地运营商的DNS地址 |
| MTU字节 | 默认1500（可降低至1300） |

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1FniAGCoiAAHrfMcy2C8011.png)

## 二. 设备联网与网络配置（联网方式：Wi-Fi联网）

海康IPC设备进行Wi-Fi配网时，对于设备配网这一步骤，我们提供了两种方案。   
方案一：远程设备确权（设备无需连接有线网络）  
方案二：局域网设备确权（设备在配置过程中需要连接有线网络）。您可以根据您的现场环境进行选择。

### **方案一：通过APP配网**

- 下载、安装、登录“萤石云视频APP”，进入开放平台工具页面进行设备添加。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1GaeAMvhjAARUEEoozkg566.png)
![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1KseATvakAAFM2oOWblQ467.png)

- 如果您需要分享安装团队为您添加设备等，可进一步了解“B端设备添加工具”的应用方案。

### **方案二：通过电脑访问设备配置页配网**

1.  设备联网。

     将NVR设备连接有线网络，并将电脑连接至同一局域网。

2.  打开设备本地配置页。

     通过4200在局域网中搜索目标设备，并获取设备的IP地址。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1HKKAS2b0AAFwA4b1GzA882.png)

在浏览器中输入对应IP地址，访问设备本地配置页。并填入用户名密码进行访问。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1HNeASeeGAAipUKPHNZY113.png)

3.  配置网卡WLAN参数。

     配置-网络-基本配置-TCP/IP-WLAN，启用自动获取，保存。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1IAKAagM8AAGwLzX1n6A249.png)

4.  连接Wi-Fi网络。

     点击配置-网络-高级配置-WiFi，选择需要连接的路由器WiFi网络，输入秘钥（路由器wifi密码），保存。
若无法启用WiFi，请先关闭Wlan热点。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1IDiAMl4fAAGUgYdgj-w147.png)

保存成功以后，退出此页面，再进入此界面搜索，如wifi连上去了，会看到该wifi信号右边显示"已连接"。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1IGiAJA9qAACHxIw_0C4212.png)

提醒：启用WIFI后，需要保存，重新进此界面搜索，要不然会搜索不到无线名称！

5.  固定wlan的网络参数。

     配置-网络-基本配置-TCP/IP-Wlan，取消自动获取，使用设备LAN口自动获取到的地址，掩码，网关信息作为Wlan口固定的网络参数，点击保存。

![](https://resource.eziot.com/group1/M00/01/2C/CtwQEmZ1Ii2AQHCWAACmOuryCIo654.png)

6.  拔网线测试。

     请拔掉网线，请用之前设置的Wlan网卡固定IP地址，测试网页访问能否登录？

![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1IqWAND5nAAHIYZq14-0094.png)

如果还可以登录，说明wifi连接正常；如果无法登录，说明wifi未连接，请核对上述设置步骤，重新排查一下。

## 三. 设备绑定

### **1. 设备启用萤石云**

配置路径：设备本地配置页-配置--网络--高级配置--平台接入  
操作：平台接入方式选择“萤石云”，并进行启用。如果“验证码/加密秘钥”是空的，可自行设置6-12位字母（ABCDEF除外）或数字；如果已有（建议修改验证码）。完成后点击保存。  
通过这个方式，您可以获取到设备序列号+设备验证码（部分设备可直接生成二维码）。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1I4SATvwaAAFfgfmoV-w123.png)

### **2. 将设备绑定至萤石开放平台开发者账号下**

这里，为了适配您的应用场景，我们提供了3种方式可支持您进行设备绑定。

1.  设备添加工具。

- 下载、安装、登录“萤石云视频APP”，进入开放平台工具页面进行设备添加。
  ![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1GtuAHrnsAARP8CC5EZ0019.png)

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1KseATvakAAFM2oOWblQ467.png)

- 如果您需要分享安装团队为您添加设备等，可进一步了解“B端设备添加工具”的应用方案。

2.  萤石开放平台控制台添加。

- 登录萤石开放平台控制台：<https://open.ys7.com/console/home.html> ，进入“设备管理器-设备管理”页面，点击“萤石协议接入”按钮，输入设备序列号与验证码进行添加。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1JluAaxYrAAKqegI-qbM673.png)

3.  API设备添加接口添加

- 您可通过设备添加接口：<https://open.ys7.com/help/661> 进行设备绑定。