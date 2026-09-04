# ERTC SDK Android 错误码.md

> ERTC SDK Android 错误码

> 更新时间: 2026-05-25T16:36:32.000+08:00

> 文档ID: 1825 | 来源树: 音视频

---

# **ERTC-SDK Android错误码**

#### Updated Time 2023/08/30

通知用户在使用音视频通话过程中出现的警告和错误

## RTCError

| 定义 | 取值 | 描述 |
| --- | --- | --- |
| ERR\_OK | 0 | 默认值 |
| 一般性错误 |  |  |
| ERR\_UNKNOWN | 100001 | 未知错误 |
| ERR\_INIT\_FAILED | 100002 | 初始化失败 |
| ERR\_NOT\_SUPPORT | 100003 | 调用不支持 |
| ERR\_INVALID\_ARGUMENT | 100004 | 参数非法 |
| ERR\_REFUSED | 100005 | 调用被拒绝 |
| ERR\_NOT\_INIT | 100006 | SDK尚未初始化 |
| ERR\_TIMEOUT | 100007 | 调用超时 |
| ERR\_NOT\_IN\_ROOM | 100008 | 房间内用户不存在 |
| 房间相关错误 |  |  |
| ERR\_ROOM\_ENTER\_FAIL | 101001 | 进入房间失败 |
| ERR\_ROOM\_INVALID\_PARAMETER | 101002 | 进入房间参数错误 |
| ERR\_ROOM\_INVALID\_APPID | 101003 | 不是有效的App ID |
| ERR\_ROOM\_INVALID\_ROOM | 101004 | 房间号无效 |
| ERR\_ROOM\_INVALID\_USERID | 101005 | 无效的用户 |
| ERR\_ROOM\_INVALID\_TOKEN | 101006 | 无效token |
| ERR\_ROOM\_ENTER\_TIMEOUT | 101007 | 进入房间超时 |
| ERR\_ROOM\_INVALID\_SERVICE | 101008 | 服务不可用 |
| ERR\_ALREADY\_IN\_USE | 101009 | 资源已被占用 |
| ERR\_PASSWORD | 101010 | 进入房间密码错误 |
| ERR\_ROOM\_TOKEN\_EXPIRED | 101011 | token过期 |
| ERR\_ROOM\_SERVICE\_TIMEOUT | 101012 | 服务超时 |
| ERR\_ROOM\_ID\_FULL | 101020 | 房间已满 |
| ERR\_ROOM\_EXIT\_FAIL | 101501 | 退出房间失败 |
| 设备相关错误 |  |  |
| ERR\_DEVICE\_NO\_PERMISSION | 102001 | 设备未授权 |
| ERR\_CAMERA\_START\_FAIL | 102002 | 摄像头驱动异常 |
| ERR\_CAMERA\_BUSY | 102003 | 摄像头正在被占用中 |
| ERR\_CAMERA\_SET\_PARAM\_FAIL | 102004 | 摄像头参数设置出错（参数不支持或其它） |
| ERR\_MICROPHONE\_UNKNOWN | 102401 | 麦克风未知错误 |
| ERR\_MICROPHONE\_CAPTURE\_FAIL | 102402 | 采集音频错误 |
| ERR\_MICROPHONE\_BUSY | 102403 | 无麦克风或麦克风正在使用中 |
| ERR\_MICROPHONE\_START\_FAIL | 102404 | 麦克风驱动异常 |
| ERR\_MICROPHONE\_SET\_PARAM\_FAIL | 102405 | 麦克风参数错误 |
| ERR\_MICROPHONE\_STOP\_FAIL | 102406 | 停止麦克风失败 |
| ERR\_SPEAKER\_START\_FAIL | 102801 | 扬声器驱动异常 |
| ERR\_SPEAKER\_SET\_PARAM\_FAIL | 102802 | 扬声器设置参数失败 |
| ERR\_SPEAKER\_PLAY\_FAIL | 102803 | 播放音频错误 |
| ERR\_SPEAKER\_STOP\_FAIL | 102804 | 停止扬声器失败 |
| 编解码错误 |  |  |
| ERR\_VIDEO\_ENCODE\_FAIL | 103201 | 视频编码失败 |
| ERR\_VIDEO\_UNSUPPORT\_RES | 103202 | 不支持的视频分辨率 |
| ERR\_AUDIO\_ENCODE\_FAIL | 103203 | 音频编码失败 |
| ERR\_AUDIO\_UNSUPPORT\_SMAPLERATE | 103204 | 不支持的音频采样率 |
| ERR\_MEDIA\_LOAD\_FAILED | 103205 | 媒体模块加载失败 |
| 网络相关错误 |  |  |
| ERR\_SERVICE\_APPID\_NOTEXIST | 210017 | appId不存在 |
| ERR\_SERVICE\_APPID\_TOKEN\_NOTMATCH | 210018 | AccessToken与AppId不匹配 |
| ERR\_SERVICE\_TOKEN\_TIMEOUT | 210002 | AccessToken失效 |
| ERR\_SERVICE\_BAD\_GATEWAY | 200502 | 服务器异常 |