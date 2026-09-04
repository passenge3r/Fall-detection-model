# RTMP格式电视上墙配置

> RTMP格式电视上墙配置

> 更新时间: 2026-05-25T16:36:13.000+08:00

> 文档ID: 4916 | 来源树: 音视频

---

# 视频上墙产品操作指南

# 1 什么是电视上墙

监控电视墙由多个电视单元拼接而成的一种超大屏幕电视墙体，便于监控人员实时发现被监控目标的异常状况，如下图所示：

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbLk-AD-3DAAb0zh4KYys135.png)

# 2 解码器上云的原理说明-以海康解码器为例

为方便业务场景为大面积远距离监控的用户，萤石开放平台目前支持监控电视墙的海康解码器接入（主要为以下型号：DS-6A01UD、DS-6A04UD、DS-6A08UD、DS-6A10UD、DS-6A12UD、DS-6A16UD），并能通过开放平台配置需要用于监控的设备RTMP视频流接入上墙，原理如下图所示：

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbL3eADhoUAACPgEeghGo313.png)

# 3 解码器如何配置到萤石开放平台

## 3.1 注册

第一步：进入解码器web的配置->网络->设备接入->萤石云页面。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbMHyAfTQUAADqt1Z1qUU736.png)

第二步：开启【启用】，点击【保存】。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbMH-AUM4NAAEI-xl0fbk695.png)

第三步：刷新web页面，查看注册状态是否更新。若显示在线，则表示注册成功。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbMIOAdC7bAADtYbz0qwA954.png)

## 3.2 绑定设备

### 3.2.1 新出货设备

按照平台操作手册添加解码器，这里需要获取解码器的序列号和设备令牌/设备验证码。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbMIaAP7AmAAJCJCQ_eWA175.png)

设备序列号在设备的铭牌上可以获取，【设备令牌/设备验证码】按以下两种方式提供：

方式一：获取【设备令牌/设备验证码】字符串，先点击【刷新】，再点击【复制】，然后再平台上粘贴即可。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbMImAN-olAADygqEb-a4665.png)

方式二：扫码获取，点击查看后用手机APP扫码即可。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbMIyAMubsAAFAlBX9PKM622.png)

### 3.2.2 现场存量设备

对于已出厂且没有萤石云验证码的设备想要上正式平台，萤石SDK也给出了方案，可以登录萤石开放平台官网添加小助手了解并添加。

# 4 RTMP视频格式上墙具体配置步骤

## 4.1 如何进入配置界面

第一步：登录萤石开发平台，点击右上角控制台-设备管理-点击右侧的设备配置（设备需为解码器）。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbRkyAf9ssAAFojWvsESg833.png)

第二步：弹出以下画面后，点击立即配置。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbRpeALP7rAAG91pJEqlw359.png)

## 4.2 墙配置

点击后会进入以下画面：

第一步：点击左侧的墙配置，单击“编辑墙规格”，同时左侧可修改电视墙的名称。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbR-yAbizhAADQSVEwknc924.png)

第二步：根据实际连接的屏幕数量，在墙规格中输入行列数或按住鼠标左键来框选范围，单击 “保存”。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbSE6ALymWAACmRQnwNJA233.png)

## 4.3 配置电视墙输出

第一步：配置输出口参数，回到墙配置，单击输出口的设置。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbSJiAN1cxAACwSPyFnpc171.png)

第二步：根据设备连接的显示屏的类型，设置输出口参数，并单击“保存”。

类型一：BNC

单击BNC输出口的设置，选择 LCD 电视墙的视频制式。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbSM6AYYODAADIErTf3U8268.png)

类型二：HDMI

单击HDMI输出口的设置，设置如下参数：

DVI模式的兼容性较好，HDMI模式支持内嵌音频输出。如果选择AUTO，设备输出口的输出模式会自动适配屏幕支持的输出模式。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbSRaAH5I6AADnhdDYhQc510.png)

输出方式一：如果选择LCD输出方式，根据需求来选择输出口分辨率。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbSUSAdNjMAADLLG3MHng916.png)

输出方式二：如果选择 LED 输出模式，直接设置屏幕的宽和高。

− 若选择带载模式，请确保设置的分辨率（宽 × 高）小于 260 万像素。

− 若选择裁剪模式，请确保设置的分辨率小于基准分辨率（选择 LCD 时显示的分辨率）。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbSXaAXHMCAADJmMALzU8870.png)

若类型一或类型二都设置好了，可以单击“复制到”，勾选输出口，将当前输出口的参数复制到所选的其他输出口。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbScWAH1v0AADR2P0oBhk104.png)

## 4.4 关联输出口至电视墙

第一步：单击“显示输出编号”。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbSgmAKBFZAACwue9ZFB4490.png)

第二步：

①根据实际屏幕上显示的输出编号，将对应的输出口拖到电视墙的屏幕上，比如下图中的BNC1、HDMI1等。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbSjeAQFHvAAC0L3W_nII459.png)

②拖过去后会显示如下画面

注：如需批量关联输出口至电视墙，通过按住 Ctrl 键来选择多个输出口，并将其拖到右侧电视墙的屏幕上。 如需取消关联的单个输出口，单击该屏幕右上角的![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbSsmAeDyeAAACqkmmDc0977.png)。 如需取消关联的所有输出口，单击“解绑所有输出口”。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbSnOAEBIlAADoTv-SvgM631.png)

## 4.5 配置输出背景

在“墙配置”页面上方，单击“输出背景”，可修改背景颜色。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbS3KAa-IPAAGHbG4hByk071.png)

## 4.6 信号源配置

萤石开放平台提供RTMP流视频上墙，具体操作如下：

第一步：单击“墙操作→信号源”，单击＋，选择“URL地址”。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbS8aAW7kMAAC9j8_OBF4473.png)

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbS-CAQwlXAADMFEaEFeM255.png)

第二步：回到控制台-设备管理，选择需要视频上墙的设备，点击右侧视频直播。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbTJ6AQ7htAAGCmotSZM0530.png)

进去后往下滑看右侧，单击生成地址。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbTMCAQ-UnAAF3kY2bKRM995.png)

选择RTMP播放地址（URL）信息部分，点击下方的复制获取。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbTOiAJdfiAAGFxzNixbE231.png)

第三步：再回到信号源配置，将复制的RTMP播放地址粘贴到下图位置，点击保存。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbTTCABee-AADq5WtbK-0726.png)

第四步：保存好后会显示到左侧，然后拖入到需要展示的屏幕即可，同时点击拖好后的设备信息，会显示右侧内容，按需编辑即可。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbXVOACzboAADYzgJxCJo697.png)

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbXXiALSu_AAD9_mv5KfA840.png)

当添加的网络信号源已经失效时，可通过按住Ctrl键或Shift键来选择多个网络信号源，再单击上方![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbXbSAcSxJAAADR7d1ClA692.png)进行批量删除。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbXbeAeWMpAAD6946imRg096.png)

## 4.7 关联信号源至电视墙

注：最多支持关联1路4K本地信号源至电视墙。

前往“墙操作”，按需选择以下方式，将信号源关联至电视墙：

情况1——关联单个信号源：选择单个信号源，将其拖动到电视墙。

- 当关联单个信号源至LCD电视墙时，信号源窗口默认占满单个屏幕。
- 当关联单个信号源至LED电视墙时，信号源窗口默认占满整个LED电视墙。

![](https://resource.eziot.com/group2/M00/01/09/CtwQFmjbXoSAa73jAADRt6XnP4w208.png)

情况2——选择以下任一方式来关联多个信号源：

- 将视频输入信号组或新建的网络信号源分组直接拖动到电视墙。本地信号源默认加入视频输入信号组。
- 按住Ctrl键选择同一分组内的多个信号源，将其拖动至电视墙。

![](https://resource.eziot.com/group2/M00/01/09/CtwQF2jbXoeAM4zbAADCFOLthZI224.png)