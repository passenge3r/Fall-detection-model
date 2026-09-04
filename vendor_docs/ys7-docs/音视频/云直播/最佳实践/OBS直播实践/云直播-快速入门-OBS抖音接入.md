# 云直播-快速入门-OBS抖音接入

> 云直播-快速入门-OBS抖音接入

> 更新时间: 2026-05-25T16:36:17.000+08:00

> 文档ID: 1756 | 来源树: 音视频

---

# 云直播-快速入门-OBS抖音接入

## 直播教程（二）：如何在抖音进行监控设备的直播

抖音是一款全民都在使用的社交软件，拥有着上亿的用户，基于如此庞大用户量，不少用户在抖音上开展直播业务。 接下来将为大家介绍如何将接在萤石开放平台上的设备画面同步至抖音直播间。

准备工具：抖音直播伴侣（下载地址：https://zjsms.com/8nY1Ebq/）

OBS Studio(下载地址：[Download | OBS](https://obsproject.com/download/))

萤石开放平台控制台（网页链接：[登录-用户认证中心](https://open.ys7.com/console/device.html)）

注意:抖音直播伴侣开通需抖音账号粉丝至少1000粉。

Step1:下载OBS软件，下载地址：[Download | OBS](https://obsproject.com/download/)

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM4WAP_E2AADQigek94E800.jpg)

下载后打开OBS界面如图：![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM5KAZiDoAAEaaxfLN-A065.jpg)

Step2:在OBS下方的来源框中选择“+”，选择媒体源添加

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM9KAGQXXAAEpBb7a90A602.jpg)

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM9aAD5f_AAAty82RdBY769.jpg)

Step3:取消本地文件选择，在输入栏填入设备的的直播地址（rtmp,flv,hls地址均可）。如何找到设备直播地址请见step4。

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM9qAIXUQAAB7IGt-Q5k182.jpg)

Step4:在萤石开放平台官网-控制台-设备管理器-设备管理中找到需要直播的设备，点击播放地址-直播地址，在直播地址页面找到所需协议的直播地址

![](https://resource.eziot.com/group1/M00/01/80/CtwQEme9W6qAEef_AAQ6_aIxP4I694.png)

Step5:OBS启动虚拟摄像机

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM-qAcM28AANQ5p52FC8155.jpg)

Step6:打开抖音直播伴侣，添加素材，选择摄像头，摄像头选择OBS Virtual Camera

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuOQqAbUnQAAD-ZOaLiDM028.png)

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuORWAJNAHAABBRzeI1e4497.png)

Step7:点击开始直播，即可在抖音上进行监控画面的直播

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuOR2ARTWZAAUcPsThgJk153.png)

常见问题：

1.     视频编码类型非H264

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM_aANvqMAACOl_F4EsU920.jpg)

答：萤石部分设备在出厂时默认H265编码格式，OBS平台不支持H265编码格式。解决方法参考链接：[萤石开放平台-提供持续稳定的以音视频为主的全场景、多功能综合性服务](https://open.ys7.com/bbs/article/14)

2.     为什么不能直接对接抖音还要使用OBS？

答：抖音直播助手不支持直接直播地址推流，需要借助OBS的虚拟摄像机作为素材导入，若您的账号有政务和媒体机构的认证，可在抖音创作者服务平台-直播管理-创建直播中设置推流和拉流

如果你对直播方案有疑问[请联系邮箱：open-team@ezvizlife.com](mailto:%252525E8%AF%B7%E8%81%94%E7%B3%BB%E9%82%AE%E7%AE%B1%EF%BC%9Aopen-team@ezvizlife.com)\*\*直播教程