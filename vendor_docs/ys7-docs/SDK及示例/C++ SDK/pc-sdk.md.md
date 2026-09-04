# pc-sdk.md

> C++ SDK 使用说明

> 更新时间: 2026-05-25T16:44:40.000+08:00

> 文档ID: 47 | 来源树: SDK及示例

---

## **萤石开放平台 PC SDK接口使用说明**

**特别说明1：** 本SDK提供的功能都已经在文档上说明，任何不在文档上说明的功能不支持，用户可以向我们提需求来完善功能。  
**特别说明2：** 请频繁查看 <https://open.ys7.com> 的内容更新，特别是FAQ栏目。  
**特别说明3：** 尽量多使用FAQ，我们对开发过程中遇到的多次被提问的问题进行汇总，FAQ能解决你90%的问题，请通过关键字进行搜索。  
**特别说明4：** 网络部署条件: \*.ys7.com开放所有端口（视频取流端口随机变化）

## 1.简介

本文档用于说明开放PCOPENSDK接口之间的关系以及接口调用顺序，对开放SDK各接口都有详细的说明。
主要分为四个部分:
第一部分为名词解释;
第二部分为SDK环境配置；
第三部阐述了开放SDK的主要调用流程;
第四部分对各模块接口进行了详细的说明。

## 2.名词解释

| 名词 | 注解 |
| --- | --- |
| authAddr | 开放平台认证中心地址，国内默认地址为：https://openauth.ys7.com，海外默认地址为: https://openauth.ezvizlife.com, 对于开发者而言，请填写此默认地址即可 |
| openAddr | 开放平台后台地址，国内默认地址为：https://open.ys7.com，海外默认地址为: https://open.ezvizlife.com, 对于开发者而言，请填写此默认地址即可 |
| appKey | AppKey的申请可以参阅: <https://open.ys7.com/view/app/app_edit.html> |
| accessToken | 访问令牌，由server返回给client用于认证 |
| expire | accessToken过期时间 |
| DeviceSerial | 设备序列号 |
| CameraNo | 设备通道号 |
| DeviceSerial+CameraNo | 摄像头唯一标志 |
| OSD | 视频视频当前时间 |
| PTZ | 云台控制，可以通过终端控制操作设备 |

## 3.SDK配置

1. 使用Visual Studio创建工程，将SDK库和头文件移入到此工程中。
2. DLL的调用方式有两种，一种是隐式加载，另外一种是显式加载。相对而言，隐式加载接入简单一些。而显式加载更加灵活一下。隐式加载时程序在启动的时候就将dll加载进来。我们下面简单展示一下隐式加载如何操作。
3. 配置SDK头文件的目录（Configuration Properties->c/c++->General->Additional Include Directories）
4. 隐式加载配置: 配置库所在目录(Configuration Properties ->Linker->Additional Library Directories)， 并将”OpenNetStream.lib”信息填入到Linker->Input->Additional Dependencies。

配置工作完成

## 4.功能介绍

1. **V1.0：** 授权登录、获取摄像头列表、直播预览、录像搜索、回放、对讲、设备添加删除、设备控制接口（云台）、视频本地录像、视频截屏等等。
2. **V2.5：** 支持推送功能，包括告警、设备下线、透明通道。
3. **V2.5：** 支持海外版本; 使用设备序列号+通道号代替CameraID; 支持推送告警图片下载; 支持获取设备预览清晰度能力级, 云台能力级, 对讲能力级。
4. **V3.1：** 支持回放片段连续播放; 支持微云服务。
5. **V3.2：** 支持海外重定向域名设置
6. **V4.0：** 支持P2P取流方式
7. **V4.2：** 支持Mac 64bit版本

## 5. SDK主要流程

### 5.1 初始化流程

![图1](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBjmuATFFpAAA59wSIRUE313.jpg)

1. 分配会话功能用于分配一个处理资源，在多任务处理的情况下，每个任务都需要调用OpenSDK\_AllocSession分配一个会话，否则将会出现无法预知的错误。分配会话的同时需要注册OpenSDK\_MessageHandler类型的回调函数，该函数主要用于错误码的抛出和信息的回调。
2. 预览, 回放, 对讲, 搜索录像 返回的结果通过OpenSDK\_MessageHandler回调函数返回。
3. [SDK 接口说明文档](http://open.ys7.com/doc/zh/pc/modules.html)

特别说明：SDK接口全部定义在OpenNetStream.dll中，打包的其他库为该动态链接库的依赖库。调用接口前需要加载OpenNetStream.dll，建议使用动态加载。

### 5.2 认证流程

![图2](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBju6AAxtPAAAv_8WOmBc204.jpg)

1. 萤石账号通过中间页登陆: 方法跳转到登录页，登录成功之后接口返回AccessToken.
2. 如果是B模式直接setAccessToken到SDK。[参考文档](/help/81)

\*\* 用户认证之后可以进行如下操作：\*\*

1. 通过获取设备列表的接口（支持分页）OpenSDK\_Data\_GetDevList，你可以从萤石云服务器获取当前登录账号的设备列表；
2. 通过deviceSerial和CameraNo对设备预览、回放、对讲、设备操作（云台控制）、查看告警列表（OpenSDK\_Data\_GetAlarmListEx）等功能接口调用；
3. 通过deviceSerial对摄像头列表中的设备进行删除操作；
4. 添加设备。

### 5.3 预览流程

![图3](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBjvyASxemAADNrWBgDb0325.jpg)

1. 预览接口为OpenSDK\_StartRealPlayEx, 它是异步接口, 预览的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=3(INS\_PLAY\_START)表示成功, MsgType=0(INS\_PLAY\_EXCEPTION)表示失败.
2. 预览播放成功后可以进行以下操作：录像、抓图、对讲、云台控制、声音开关，其中设备控制该接口的如云台控制、对讲，属于限制级接口，要优选通过判断设备的能力集来调用，设备能力集请查看OpenSDK\_Data\_GetDevDetailInfo.
3. OpenSDK\_SetVideoLevel用于设置视频清晰度（videoLevel），此调节在视频播放前设置，不过设置前需要判断要设置的清晰度是否支持, 可以通过设备列表中的值或者OpenSDK\_Data\_GetDevDetailInfo接口获取videoQualityInfos信息. 其中传入惨重bUpdate只有在用户重新登录或者刷新设备信息的时候才为true.
4. 如果MsgType=0(INS\_PLAY\_EXCEPTION), 则根据MessageInfo来判断错误信息, [错误信息参考](/help/48), 如果错误信息为UE105, 则可以根据ErrorCode确定具体错误码。
5. 录像功能通过调用OpenSDK\_SetDataCallBack来设置数据回调, 最终实现录制功能
6. 新增OpenSDK\_StartRealPlayNew接口，支持设置小权限token，使用方式和OpenSDK\_StartRealPlayEx相似，差别调用接口必须先获取小权限token

### 5.4 回放流程

![图4](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBjwWALCd8AABj3V3eNxw400.jpg)

1. 回放之前首先要搜索录像, 调用OpenSDK\_StartSearchEx接口,它是异步接口,搜索的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=20(INS\_RECORD\_FILE)表示录像搜索成功, 录像信息在MessageInfo中,如果MsgType=22(INS\_RECORD\_SEARCH\_FAILED)表示搜索失败, 查看ErrorCode确定具体原因.
2. 回放接口为OpenSDK\_StartPlayBackEx, 它是异步接口, 回放的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=3(INS\_PLAY\_START)表示成功, MsgType=0(INS\_PLAY\_EXCEPTION)表示失败.
3. 回放播放成功后可以进行以下操作：录像、抓图、声音开关，具体方法见接口手册；
4. OpenSDK\_GetOSDTime获取当前回放时间点，如果回放开始时间8:00，结束时间9:00，getOSDTime时间为8:30，那么播放进度为50%；
5. 回放播放成功后可以调用OpenSDK\_PlayBackPause（暂停远程回放播放）和 OpenSDK\_PlayBackResume（恢复远程回放播放）；
6. 如果MsgType=0, 则根据MessageInfo来判断错误信息, [错误信息参考](/help/48), 如果错误信息为UE105, 则可以根据ErrorCode确定具体错误码。
7. 回放结束根据消息MsgType=5(INS\_PLAY\_ARCHIVE\_END)；
8. 录像功能通过调用OpenSDK\_SetDataCallBack来设置数据回调, 最终实现录制功能；
9. 录像搜索接口OpenSDK\_StartSearchEx, 不支持超过24小时的搜索(云存储录像的限制).
10. 新增OpenSDK\_StartPlayBackNew接口，支持设置小权限token，使用方式和OpenSDK\_StartPlayBackEx相似，差别调用接口必须先获取小权限token,并且需要上级输入录像信息。

### 5.5 对讲流程

![图5](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBj1-AETkYAAA5koFP0io515.jpg)

1. 开始对讲接口为OpenSDK\_StartVoiceTalkEx, 它是异步接口, 回放的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=16(INS\_VOICETALK\_START)表示预览成功, MsgType=18(INS\_VOICETALK\_EXCEPTION)表示失败.
2. 停止对讲接口为OpenSDK\_StopVoiceTalk, 它是异步接口, 回放的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=17(INS\_VOICETALK\_STOP)表示预览成功
3. 对讲为客户端模式对接, sdk自身会调用麦克风来采集音频数据, 传递都设备端, 设备端的音频数据直接通过耳机来收听, 目前支持对讲的设备必须是双孔耳机, 一孔耳机, 一孔麦克.
4. 关于对讲功能，如果预览播放有声音输出，则在开启对讲前需要关闭预览播放的声音closeSound，关闭对讲后开启预览播放的声音openSound，详见demo；

### 5.6 推送流程

![图6](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBj2-AaYOPAACKElIDBOI623.jpg)

使用萤石PC OpenSDK, 通过发送邮件到open-team.com申请pushSecret，用于接受设备端到客户端的报文消息推送，申请时请提供以下信息（\*为必填）：

1. 环境(test2 /online)\*
2. 有效的appKey(开放平台注册)，必须与环境对应\*
3. 第三方应用名称\*
4. 第三方应用描述(非必要)

特别说明：告警模块和数据模块的告警列表是两种模式，告警模块是主动模式，当有告警发生时，会推送给回调函数；告警列表时被动获取模式，新告警的发送需要重新调用该接口获取。

### 5.7 获取数据信息流程

![图7](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBj4KAKv64AAA0kFHyo88419.jpg)

### 5.8 设备控制流程

![图8](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBj6KACeiGAAA0yMH7_iw965.jpg)

1. 云台控制接口为OpenSDK\_PTZCtrlEx, 它是异步接口, 控制的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=46(INS\_PTZCTRL\_SUCCESS)表示预览成功, MsgType=47(INS\_PTZCTRL\_FAILED)表示失败.
2. 布撤防接口为OpenSDK\_DevDefenceEx, 它是异步接口, 结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=23(INS\_DEFENSE\_SUCCESS)表示预览成功, MsgType=24(INS\_DEFENSE\_FAILED)表示失败.

### 5.9获取录像封面流程

1.SDK提供的获取录像封面接口是按录像片段来获取。

2.获取录像片段需要先查询录像列表。

3.然后调用OpenSDK\_GetLocalRecordCover接口，输入session 设备序列号 通道号 开始时间 结束时间 以及 本次请求的
索引 索引唯一 返回数据里会返回 输入的索引。

4.数据返回的格式为 4字节json长度 + json结构 + 图片信息。

5.json结构为 {
"type": 0,
"cmd": 2,
"seq": 1,
"result": 0,
"PicTimestamp": "2023-12-11T05:34:05",
"PicLen": 14768
}

6 seq 输入的索引 result：为0为获取成功 PicLen：图片长度

## 6.快速接入示范

本节旨在引导开发者进行快速接入，通过介绍几个关键的接口，并给出对应的界面和接口，以及代码范例，让开发者对sdk有个初步了解
首先请下载[Qt Demo](https://open.ys7.com/mobile/download.html?type=app)

### 6.1 Qt Demo功能概况

1. 功能展示, SDK API测试工具
2. 开发异常排查, 缺陷验证
3. 调用示例代码展示（提供了调用接口的源码）

### 6.2 Qt Demo工程环境

1. Qt Demo 所使用Qt SDK版本：Qt4.8.5
2. Qt Demo 两种开发模式：
   1). 下载Qt Creator for Windows，使用Qt Creator作为IDE进行开发, 通过打开OpenSDK\_Demo\_Qt.pro工程文件。
   2). Visual Studio Add-in for Qt4， 集成到Visual Studio 2008中进行开发, 通过打开OpenSDK\_Demo\_Qt.sln工程文件。

### 6.3 配置Demo配置文件（OpenSDK\_Demo\_Qt.ini）

| 字段 | 说明 | 数值 | 是否必填 |
| --- | --- | --- | --- |
| authAddress | 开放平台认证中心地址 | 国内默认地址为：https://openauth.ys7.com，海外默认地址为: https://openauth.ezvizlife.com, 对于开发者而言，请填写此默认地址即可 | 非, 如果需要Mid\_Login, 则必填 |
| platformAddress | 开放平台后台地址 | 国内默认地址为：https://open.ys7.com，海外默认地址为: https://open.ezvizlife.com, 对于开发者而言，请填写此默认地址即可 | 是 |
| appKey | 产品唯一标识, 向开放平台申请 | AppKey的申请可以参阅: <https://open.ys7.com/view/app/app_edit.html> | 是 |
| pushSecret | 推送服务唯一标识 | 如果需对接推送服务, 申请发邮件open-team@ezvizlife.com | 否, 如果对接Push\_StartRecv, 则必填 |
| isPlay | 是否播放 | true: opensdk内部调用播放库进行播放;false: opensdk不调用播放库播放 | 否, 默认true |
| saveData | 存储码流到本地 | true: 存储码流到可执行程序对应的目录;false: 不存储码流 | 否,默认true, 可执行程序目录为英文才支持 |
| dataUtf8 | 是否以Utf8格式输出数据 | true: 数据的输出为Utf8格式;false: 数据的输出为本地编码格式 | 否, 默认false |
| streamMeta | 码流是否原始数据输出 | true:码流原始数据输出;false:码流经过转封装库后输出, 且不加密 | 否, 默认false |

### 6.4 Demo的操作步骤要点

1. 在[萤石开发平台](https://open.ys7.com)创建一个新应用，获取AppKey和AppSecret。
2. 使用Notepad打开OpenSDK\_Demo\_Qt.ini文件进行配置。
3. 预览、回放、语音、云台控制等等操作都是基于登录认证操作之后。
4. 可以使用DebugView来获取Demo或者OpenSDK的日志文件，方便排查问题。
   注意：Demo工程目录中不要包含中文

### 6.5 获取摄像头列表

```
int OpenSDK_Data_GetDevList( const char* szAccessToken, int iPageStart, int iPageSize, void** pBuf, int* iLength);
```

说明：通过调用OpenSDK\_Data\_GetDevList，可以得到JSON格式的字符串, JSON串里面包含一个监控点列表信息。

### 6.6 预览功能

![PC 预览](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBknmAA-x1AADTt_N1xP0216.jpg)

1. 配置OpenSDK\_Demo\_Qt.ini中isPlay字段, 比方”isPlay =true”
2. 按照上述配置后, 启动Demo, 登录账户
3. 选择要预览的监控点, 点击” 开始”按钮进行预览

```
int OpenSDK_StartRealPlayEx(const char* szSessionId, HWND hPlayWnd, const char* szDevSerial, const int iChannelNo, const char* szSafeKey);
```

说明：通过调用OpenSDK\_StartRealPlayEx，传入设备序列号+通道号+窗口句柄, 如果设备是加密的, 则需要输入设备验证码.

### 6.7 回放功能

![PC 回放](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBkQ-Ae-fiAAEuAebvE30872.jpg)

1. 配置OpenSDK\_Demo\_Qt.ini中isPlay字段, 比方”isPlay =true”
2. 按照上述配置后, 启动Demo, 登录账户
3. 选择要回放的监控点, 点击”选搜索时间”按钮确定录像搜索的时间, 然后点击” 回放列表”来搜索录像.
4. 选择一段回放片段, 然后点击”开始”按钮开始回放.

```
int OpenSDK_StartPlayBackEx(const char* szSessionId, HWND hPlayWnd, const char* szDevSerial, const int iChannelNo, const char* szSafeKey, const char* szStartTime, const char* szStopTime);
```

说明：通过调用OpenSDK\_StartRealPlayEx，传入设备序列号+通道号+窗口句柄+开始时间+结束时间, 如果设备是加密的, 则需要输入设备验证码.

### 6.8 录制功能

1. 配置OpenSDK\_Demo\_Qt.ini中saveData字段, 比方”saveData=true”
2. 按照上述配置后, 启动Demo, 登录账户, 进行预览或者回放后, 可执行程序对应的目录下会生成文件. 效果如下:
   ![PC 录制](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBkUKACrSgAAAavGUamhQ984.jpg)

```
int OpenSDK_SetDataCallBack(const char* szSessionId, OpenSDK_DataCallBack pDataCallBack, void* pUser);
```

说明：萤石sdk目前不支持下载功能, 只支持录制. 录制功能依靠数据回调接口.具体请参考接口操作手册.

### 6.9 下载功能

![PC 下载](https://resource.eziot.com/group2/M00/00/67/CtwQF2FBkXCAJheBAABX2dXKzMs769.jpg)

1. 调用下载接口之前需要开通云存储功能，
2. 调用云存储录像搜索接口:OpenSDK\_StartSearchExtend(),搜索云存储录像(最大支持搜索一天的录像)，该接口为异步接口,搜索的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=20(INS\_RECORD\_FILE)表示录像搜索成功, 录像信息在MessageInfo中,如果MsgType=22(INS\_RECORD\_SEARCH\_FAILED)表示搜索失败, 查看ErrorCode确定具体原因.
3. 选择云存储录像,调用OpenSDK\_StartDownloadCloudFile(异步接口)进行下载, 下载的结果根据消息回调MessageHandler里面的MsgType判断, 如果MsgType=14(INS\_DOWNLOAD\_STOP)表示下载完成, MsgType=0(NS\_DOWNLOAD\_EXCEPTION)表示下载异常.
   如果需要解密码流数据则需要开启转封装功能。
4. 如果需要停止下载请调用OpenSDK\_StopDownloadCloudFile()接口,如果MsgType = INS\_USER\_STOP\_DOWNLOAD 表示停止成功;
5. 暂不支持跨片段连续下载。
6. 新增OpenSDK\_StartDownloadNew接口，使用前需要先获取小权限token.

## 7.常见问题

1. demo的源代码：[demo](http://download2.ys7.com/openweb/pc/EzvizQtDemoSRPM.zip)（开发环境VScode2008，不支持QT开发）。
2. Qt Demo中间页登录提示错误码-3, 这是什么原因?
   答复: 一般是Qt Demo配置文件中没有填写appkey的值导致.
3. 预览时返回2012错误码，是什么原因？
   答复：2012错误码，表示输入的验证码不正确
4. 如何查看OpenSDK的版本？
   答复：选择OpenSDK右键属性->详细信息，文件版本即当前OpenSDK的版本。

![PC 版本](https://resource.eziot.com/group2/M00/00/67/CtwQFmFBkY2AW-eZAACNqWoCvVw932.jpg)