# 微信小程序音视频SDK接入文档

> 微信小程序音视频SDK接入文档

> 更新时间: 2026-05-25T16:36:37.000+08:00

> 文档ID: 496 | 来源树: 音视频

---

# 微信小程序音视频SDK接入文档

## 简介

WeChat\_ERTC\_SDK支持微信小程序主要提供以下API：

- 初始化
- 加入房间（enterRoom）
- 离开房间（leave）
- 支持 发布音视频流（pushStream）
- 支持 停止发布音视频流 （stopPushStream）
- 支持 订阅远端的音视频流 （pullPeerStream）
- 支持 停止订阅远端的音视频流 （stopPullPeerStream）
- 支持 暂停发送本地音视频流 （pausePushStream）
- 支持 恢复发送本地音视频流 （resumePushStream）
- 支持 暂停接收远端音视频流 （pausePullPeerStream）
- 支持 继续接收远端音视频流 （resumePullPeerStream）
- 支持 设置监听事件，监听房间状态（onRoomInfoChange）

sdk下载地址：

## API详情

**1、初始化**
初始化对象,目前仅支持通过内部引入的方式导入，例如，wechat-ertc-sdk存放在同目录下lib文件夹中。

```
import {WeChat_ERTC} from './lib/wechat-ertc-sdk'

const WeRtc = new WeChat_ERTC({
    appID: '', // 应用appID
    accesstoken: '', // 开放平台接口访问令牌，每个token独立拥有7天生命周期，若accesstoken过期，请调用更新token接口
    roomId: '',
    customId: '',
    rtctoken: ''
})
```

**2、加入房间**

```
WeRtc.enterRoom();
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 |  |  |
| 响应参数 | Promise | 空promise对象 |

**3、离开房间**

```
WeRtc.leave();
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 |  |  |
| 响应参数 | Promise | 空promise对象 |

**4、发布音视频流**

```
WeRtc.pushStream(streamtype: int = 3); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | streamtype | 非必填，默认值为3（小程序无大小流，默认为大流）表示默认同时发布音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**5、停止发布音视频流**

```
WeRtc.stopPushStream(streamtype: int = 3); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | streamtype | 非必填，默认值为3（小程序无大小流，默认为大流）表示默认同时发布音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**6、暂停发送本地音视频流**

```
WeRtc.pausePushStream(streamtype: int = 3); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | streamtype | 非必填，默认值为3（小程序无大小流，默认为大流）表示默认同时发布音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**7、恢复发送本地音视频流**

```
WeRtc.resumePushStream(streamtype: int = 3);; // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | streamtype | 非必填，默认值为3（小程序无大小流，默认为大流）表示默认同时发布音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**8、订阅远端的音视频流**

```
WeRtc.pullPeerStream(clientId: int, streamtype: int); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | clientId | 必填，远端的ID，需要取哪个对等端的流 |
|  | streamtype | 必填，默认值为3（小程序无大小流，默认为大流）表示默认同时订阅音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**9、暂停接收远端音视频流**

```
WeRtc.pausePullPeerStream(clientId: int, streamtype: int); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | clientId | 必填，远端的ID，需要暂停接收哪个对等端的流 |
|  | streamtype | 必填，默认值为3（小程序无大小流，默认为大流）表示默认同时订阅音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**10、继续接收远端音视频流**

```
WeRtc.resumePullPeerStream(clientId: int, streamtype: int); // 1-视频流大流，2-音频流
```

参数说明：

|  | 参数名 | 参数描述 |
| --- | --- | --- |
| 请求参数 | clientId | 必填，远端的ID，需要继续接收哪个对等端的流 |
|  | streamtype | 必填，默认值为3（小程序无大小流，默认为大流）表示默认同时订阅音视频流，可选值为1/2/3 |
| 响应参数 | Promise | 空promise对象 |

**11、设置监听事件，监听房间状态**

房间状态改变时会触发，其中的state会将房间状态抛出。 可通过绑定onRoomInfoChange，当state状态发生变化时自动抛出，也可通过getRoomInfo方法自动获取。

onRoomInfoChange触发时间节点：websocket返回以下信令发生变化时，均会抛出

```
WeRtc.onRoomInfoChange: (state: string, roomState: object) =>> {};

WeRtc.getRoomInfo(roomState: object) =>> {}
```

参数说明：

| 流程编号 | 事件 | 返回参数 | 接口描述 |
| --- | --- | --- | --- |
| 1 | stream-added | roomState | 房间内远端有音视频流加入。streamtype: 1 大流 2 音频 4 小流 8 屏幕共享流 |
| 2 | stream-removed | roomState | 房间内远端有音视频流离开 |
| 3 | video-rotation | roomState | 远端有视频旋转。 |
| 4 | mute-audio | roomState | 远端有用户已停止发送音频流 |
| 5 | mute-video | roomState | 远端有用户已停止发送视频流 |
| 6 | unmute-audio | roomState | 远端有用户恢复发送音频流 |
| 7 | nmute-video | roomState | 远端有用户恢复发送视频流 |
| 8 | clientJoin | roomState | 远端有用户加入房间 |
| 9 | clientLeave | roomState | 远端有用户离开房间 |
| 10 | error | code | 表示错误码 |

**微信sdk音视频通话房间信息**
RoomState 结构 {
state : number, // 房间状态
push\_rtmp: string // 推流地址
persons: Array, // 房间所有成员状态的数组，一个Person对象代表一个成员。
}

```
Person 结构 {
    id: string, // 成员clientId
    astate： number, // 0 开起，1 关闭，2 禁用
    vstate： number, // 0 开起，1 关闭，2 禁用
    streams： Array<StreamInfo>, // 通过该地址，可播放该成员的流，目前只有一路
    self： boolean, // 如果是自己这个属性为true, 其他人为false。
}

StreamInfo 结构 {
    stream_type: int, //流类型，1 大流 2 音频  8 屏幕共享流
    angle: number, //角度
    codec: number, // 编码类型
    fps: number, // 帧率
    rtmp: string，// 由内部控制，不需要使用，使用Person结构下的RTMP地址即可。
    state: null, // 预留字段
}
```

**微信sdk音视频通话过程中，错误码列表**