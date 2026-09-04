# 海康IPC（4G）

> 海康IPC（4G）

> 更新时间: 2024-06-24T13:41:22.000+08:00

> 文档ID: 2835 | 来源树: 云接入

---

# · 完整接入流程：

### 海康4G设备的添加过程中涉及到“设备确权”这一步骤，因此整体有两种方案。 方案一：远程设备确权（设备无需连接有线网络）； 方案二：局域网设备确权（设备在配置过程中需要连接有线网络）。您可以根据您的现场环境进行选择。

## 方案一：远程设备确权（设备无需连接有线网络）

### **一. 设备绑定**

当前我们仅提供“设备添加工具”，帮助您进行该类设备的绑定。

1.  设备添加工具。

- 设备通电，并确认设备指示灯状态。
    
  ![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1LPyAHkFSAAuqMFHM1cE129.png)
- 下载、安装、登录“萤石云视频APP”，进入开放平台工具页面进行设备添加。
    
  ![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1GtuAHrnsAARP8CC5EZ0019.png)
  ![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1LmGAZ4AqAAL7l434CNw269.png)
- 确认设备信息
    
    
             ![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1LomAOiFbAACEo6xUbYU389.png)
- 选择进入sim卡设备激活模式
    
    
             ![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1LreAeIWGAACgaQq3wpU696.png)
- 按照app提示进行设备激活，直至完成设备添加。

## 方案二：远程设备确权（设备需连接有线网络）

### **一. 设备绑定**

1.  设备联网（连接有线网络）

     将IPC设备连接有线网络，并将电脑连接至同一局域网。
  
  
2. 打开设备本地配置页

    通过4200在局域网中搜索目标设备，并获取设备的IP地址。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1L1WAXL9PAAFwA4b1GzA768.png)

      在浏览器中输入对应IP地址，访问设备本地配置页。并填入用户名密码进行访问。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1L3qAL7-6AAipUKPHNZY032.png)
  
3. 启用萤石云服务

    设备本地配置页-配置--网络--高级配置--平台接入

    操作：平台接入方式选择“萤石云”，并进行启用。如果“验证码/加密秘钥”是空的，可自行设置6-12位字母或数字；如果已有（建议修改验证码）。完成后点击保存。
通过这个方式，您可以获取到设备序列号+设备验证码（部分设备可直接生成二维码）。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQE2Z1L7aAHK8lAALqnn9CnkM788.png)

      您也可以选择通过用户令牌（超链接）的模式进行设备添加。
  
  
4. 将设备绑定至萤石开放平台开发者账号下

    这里，为了适配您的应用场景，我们提供了3种方式可支持您进行设备绑定。

    a）设备添加工具。
  
          下载、安装、登录“萤石云视频APP”，进入开放平台工具页面进行设备添加。
![](https://resource.eziot.com/group1/M00/01/2C/CtwQE2Z1GtuAHrnsAARP8CC5EZ0019.png)

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1KseATvakAAFM2oOWblQ467.png)

            如果您需要分享安装团队为您添加设备等，可进一步了解“B端设备添加工具”的应用方案。
  
  
      b）萤石开放平台控制台添加。

            登录萤石开放平台控制台：<https://open.ys7.com/console/home.html>，进入“设备管理器-设备管理”页面，点击“萤石协议接入”按钮，输入设备序列号与验证码进行添加。

![](https://resource.eziot.com/group1/M00/01/2D/CtwQEmZ1NMeAI_KZAAKqegI-qbM110.png)

      c）  API设备添加接口添加。

            您可通过设备添加接口：<https://open.ys7.com/help/661> 进行设备绑定。