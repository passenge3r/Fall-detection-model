# SDK-webRTC-错误码

> SDK-webRTC-错误码

> 更新时间: 2026-05-25T16:36:37.000+08:00

> 文档ID: 2148 | 来源树: 音视频

---

# ERTC Web 错误码

> 本教程基于 ERTC Web SDK 2.x 版本

## 错误码定义

### 一般性错误

| 定义 | code | 描述 |
| --- | --- | --- |
| ERR\_OK | 0 | 接口调用成功 |
| ERR\_UNKNOWN | 100001 | 未知错误 |
| ERR\_INIT\_FAILED | 100002 | 初始化失败 |
| ERR\_NOT\_SUPPORT | 100003 | 调用不支持 |
| ERR\_INVALID\_ARGUMENT | 100004 | 参数非法 |
| ERR\_REFUSED | 100005 | 调用被拒绝 |
| ERR\_NOT\_INIT | 100006 | SDK 尚未初始化 |
| ERR\_TIMEOUT | 100007 | 调用超时 |
| ERR\_REQUEST\_PARAMETER | 100009 | 接口请求参数错误 |
| ERR\_REQUEST\_UNKNOWN | 100010 | 接口请求异常 |
| ERR\_SDK\_CONNECTED | 100011 | SDK 连接异常 |

### 房间相关错误

| 定义 | code | 描述 |
| --- | --- | --- |
| ERR\_ROOM\_ENTER\_FAIL | 101001 | 进入房间失败 |
| ERR\_ROOM\_INVALID\_TOKEN | 101006 | 无效 token |
| ERR\_TOKEN\_EXPIRED | 101011 | token 异常或过期 |
| ERR\_ROOM\_EXIT\_FAIL | 101501 | 退出房间失败 |
| ERR\_SERVICE\_ACCESSTOKEN\_INVALID | 210002 | accessToken 异常或过期 |

### 设备相关错误

| 定义 | code | 描述 |
| --- | --- | --- |
| ERR\_DEVICE\_NO\_PERMISSION | 102001 | 设备未授权 |
| ERR\_CAMERA\_START\_FAIL | 102002 | 摄像头驱动异常 |
| ERR\_CAMERA\_SET\_PARAM\_FAIL | 102004 | 摄像头参数设置出错（参数不支持或其它） |
| ERR\_NO\_DEVICE | 102005 | 未查询到设备 |
| ERR\_MICROPHONE\_UNKNOWN | 102401 | 麦克风未知错误 |
| ERR\_MICROPHONE\_START\_FAIL | 102404 | 麦克风驱动异常 |
| ERR\_MICROPHONE\_SET\_PARAM\_FAIL | 102405 | 麦克风参数错误 |
| ERR\_SUBSCRIBE\_FAIL | 102902 | 订阅音视频失败 |

### 信令相关错误

| 定义 | code | 描述 |
| --- | --- | --- |
| ERR\_SIGNAL\_SEND | 104001 | 信令发送报错 |
| ERR\_SIGNAL\_RECEIVE | 104002 | 信令接收报错 |