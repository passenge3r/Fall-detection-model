# 云直播-快速入门-OBS直播接入

> 云直播-快速入门-OBS直播接入

> 更新时间: 2026-05-25T16:36:16.000+08:00

> 文档ID: 1755 | 来源树: 音视频

---

# 云直播-快速入门-OBS直播接入

## 直播教程（一）：OBS推流至各大直播平台

在直播行业盛行的背景下，慢直播这一直播方式逐渐走入大众的视野中，还记得火神山方舱医院建造时数百万群众在直播间观看建造全过程吗？还记得在第一场雪下进西湖时有数万观众线上观看断桥残雪的美景吗？

这些画面大部分都来自于摄像设备，如果你想要学习如何将摄像画面在各直播平台进行直播，就请往下看吧~

OBS是一个免费的开源的视频录制和视频实时流软件，其有多种功能并广泛使用在视频采集，直播等领域。市面上的大部分直播平台都兼容OBS进行推流直播，包括微博、腾讯云直播、斗鱼、虎牙等。基于个直播平台对OBS的兼容性，今天就先教大家如何连接设备-OBS-直播平台，实现将摄像头上的画面同步直播到各直播平台。

接下来以微博平台为例给大家介绍详细的步骤。

Step1:下载OBS软件，下载地址：[Download | OBS](https://obsproject.com/download/)

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM4WAP_E2AADQigek94E800.jpg)

下载后打开OBS界面如图：

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM5KAZiDoAAEaaxfLN-A065.jpg)

Step2:打开各直播软件的开播界面，选择PC端开播，并创建直播间。用户在创建直播间时平台会提供流地址和流密钥，这两个数据下一步会用到哦~  
微博直播PC端地址：https://me.weibo.com/content/live

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM6CAOpFHAAD1XrKKIX4615.jpg)

Step3:将流地址和流密钥信息填入OBS中，OBS打开右下角设置，打开推流，服务选择自定义，服务器内容填step2中的流地址，串流密钥填入step2中的流密钥

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM8qAG5r9AAEQTPr_14U921.jpg)

Step4:在OBS下方的来源框中选择“+”，选择媒体源添加

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM9KAGQXXAAEpBb7a90A602.jpg)![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM9aAD5f_AAAty82RdBY769.jpg)

Step4:取消本地文件选择，在输入栏填入设备的的直播地址（rtmp,flv,hls地址均可）。如何找到设备直播地址请见step5。

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM9qAIXUQAAB7IGt-Q5k182.jpg)

Step5:在萤石开放平台官网-控制台-设备管理器-设备管理中找到需要直播的设备，点击播放地址-直播地址，在直播地址页面找到所需协议的直播地址

![](https://resource.eziot.com/group1/M00/01/80/CtwQEme9W6qAEef_AAQ6_aIxP4I694.png)

Step6:OBS开始推流，直播平台上就可以实时看到

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM-qAcM28AANQ5p52FC8155.jpg)

![](https://resource.eziot.com/group1/M00/00/8B/CtwQE2LuM_GAGlV8AAF0TUuIYk8606.jpg)

常见问题：

1.     视频编码类型非H264

![](https://resource.eziot.com/group1/M00/00/8B/CtwQEmLuM_aANvqMAACOl_F4EsU920.jpg)

答：萤石部分设备在出厂时默认H265编码格式，OBS平台不支持H265编码格式。解决方法参考链接：[萤石开放平台-提供持续稳定的以音视频为主的全场景、多功能综合性服务](https://open.ys7.com/bbs/article/14)

2.     怎么对接其他的直播平台？

答：大部分直播平台支持OBS推流，用户可以先和直播软件确认。在直播软件的助手软件上都会提供推流服务器地址和串流密钥信息，将两个信息按照Step3方法填入，就能将OBS和直播平台连接起来。

3．有其他方式获取直播地址吗？

答：用户可以通过接口获取直播地址，接口：[文档概述 · 萤石开放平台API文档](https://open.ys7.com/help/82)，可以设置直播地址的过期时间，回放预览等。

后续将陆续推出其他直播软件的对接方式，敬请期待~

如果你有疑问或者迫不及待想要知道其他平台的直播对接方式，[请联系邮箱：open-team@ezvizlife.com](mailto:%25252525E8%AF%B7%E8%81%94%E7%B3%BB%E9%82%AE%E7%AE%B1%EF%BC%9Aopen-team@ezvizlife.com)