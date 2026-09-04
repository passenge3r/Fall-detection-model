# 体验示例程序 - Windows

> 体验示例程序 - Windows

> 更新时间: 2026-05-25T16:36:28.000+08:00

> 文档ID: 1996 | 来源树: 音视频

---

# 体验示例程序 - Windows

# windows

在正式使用ERTC服务之前，你可以使用我们提前编译好的示例程序来体验基本功能。

1. [下载示例程序](https://open.ys7.com/cn/s/download)
2. 修改配置文件

   1. 打开配置文件config.ini
   2. 修改字段appId

      成功创建项目后，萤石云会给每个项目自动分配一个APP ID作为项目唯一标识。你可以在[项目管理](https://open.ys7.com/console/rtc/projectManage.html)页面查看项目的App ID。

      ![Untitled.png](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUuoKAMRVPAAHHEAA5gAk230.png)
   3. 修改字段appsecret和accesstoken

      appsecret和accessToken可以在[控制台的账号中心/应用信息](https://open.ys7.com/console/application.html)中获取：

      ![Untitled.png](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUvFCAPCVnAAWpovg5a-w177.png)
3. 加入房间

   启动EZRTCTest.exe程序，并填写roomid和userid.

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQEmWUvFOAc7vIAAEaCh051sU413.png)

   在我们已经开启的ERTC项目中，我们用roomid区分不同的会话，userid区分不同的用户。

   加入相同roomid的不同用户将被拉入同一个会话。

   我们在另外一台机器上（同一机器也可以）打开另外一个EZRTCTest.exe程序，进入同样的房间。

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUvFSARkBHAAEYPM2DFkI473.png)
4. 打开本地摄像头

   选择本地摄像头，并勾选EnableVideo，打开本地摄像头。

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUvFqAcLcsAARl9yriLEI184.png)
5. 打开本地麦克风

   选择本地麦克风，并勾选EnalbeMic，打开本地麦克风

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQEmWUvFyAB5uMAAR_QIMyDak189.png)
6. 共享本地桌面

   选择本地的一个显示器，并勾选EnableShare，可以共享本地的一个桌面

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUvF6AIhXdAARwLyTBreY147.png)
7. 订阅

   在同一房间的另外一个客户端,会自动订阅对端的音频。点击StartVideo订阅对端的摄像头，勾选SubScreen订阅对端的桌面共享。

   ![Untitled](https://resource.eziot.com/group1/M00/00/F8/CtwQE2WUvF6AIhXdAARwLyTBreY147.png)