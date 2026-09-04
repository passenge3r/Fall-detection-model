# SDK-webRTC-网络质量检测

> SDK-webRTC-网络质量检测

> 更新时间: 2026-05-25T16:36:36.000+08:00

> 文档ID: 2852 | 来源树: 音视频

---

# ERTC Web 网络质量检测

> 本教程基于 ERTC Web SDK 2.1.x 版本

### 功能说明

上层通过监听 SDK 已有的网络质量通报 "REPORT\_NETWORK\_QUALITY" 事件，基于 SDK 已有的 API，实现通话前网络检测。

### 兼容性

|  | chrome | firefox | edge | safari | opera |
| --- | --- | --- | --- | --- | --- |
| windows | 80 | 80 | 80 | - | 90 |
| mac | 80 | 99 | 80 | 14.1.1 | 90 |

### 实现过程

1. 调用 new ERTC() 创建两个 ertc 实例对象，分别称为 uplinkERTC 和 downlinkERTC，并让这两个 ERTC 都进入同一个房间。
2. 使用 uplinkERTC 进行推流，监听 REPORT\_NETWORK\_QUALITY 事件来检测上行网络质量。
3. 使用 downlinkERTC 进行拉流，监听 REPORT\_NETWORK\_QUALITY 事件来检测下行网络质量。
4. 整个过程可持续 30s 左右，最后取平均网络质量，从而大致判断出上下行网络情况。

#### API 调用时序图

![](https://resource.eziot.com/group1/M00/01/1C/CtwQE2Y-53aAFZ7tAADfNA4O4Fk072.png)

#### 示例代码

```
import ERTC from "ertc-web";
// ......

let uplinkERTC = null; // 用于检测上行网络质量
let downlinkERTC = null; // 用于检测下行网络质量
let testResult = {
  // 记录上行网络质量数据
  uplinkNetworkQualities: [],
  // 记录下行网络质量数据
  downlinkNetworkQualities: [],
  average: {
    uplinkNetworkQuality: 0,
    downlinkNetworkQuality: 0,
  },
};

// 1. 检测上行网络质量
async function testUplinkNetworkQuality() {
  return new Promise((resolve, reject) => {
    uplinkERTC = new ERTC(ertcSettings);
    uplinkERTC
      .enterRoom({
        accessToken: roomState["accessToken1"],
        appId: roomState["appId1"],
        roomId: roomState["roomId1"],
        userId: roomState["userId1"],
      })
      .then((res) => {
        if (res.code === 0) {
          uplinkERTC
            .startLocalVideo()
            .then((res2) => {
              if (res2.code === 0) resolve(res2);
              else reject(res2);
            })
            .catch(reject);
        } else {
          reject(res);
        }
      })
      .catch(reject);
    uplinkERTC.on(ERTC.EVENT.REPORT_NETWORK_QUALITY, (event) => {
      const { uplink } = event;
      testResult.uplinkNetworkQualities.push(event.uplink);
    });
  });
}
// 2. 检测下行网络质量
async function testDownlinkNetworkQuality() {
  return new Promise((resolve, reject) => {
    downlinkERTC = new ERTC(ertcSettings);
    downlinkERTC
      .enterRoom({
        accessToken: roomState["accessToken2"],
        appId: roomState["appId2"],
        roomId: roomState["roomId2"],
        userId: roomState["userId2"],
      })
      .then((res) => {
        if (res.code === 0) {
          downlinkERTC
            .subscribeStream({
              userId: roomState["userId1"],
              type: ERTC.STREAM_TYPE.VIDEO_ONLY,
            })
            .then((res2) => {
              if (res2.code === 0) resolve(res2);
              else reject(res2);
            })
            .catch(reject);
        } else {
          reject(res);
        }
      })
      .catch(reject);
    downlinkERTC.on(ERTC.EVENT.REPORT_NETWORK_QUALITY, (event) => {
      const { downlink } = event;
      testResult.downlinkNetworkQualities.push(downlink);
    });
  });
}
// 3. 开始检测,先上行发布视频，避免下行在上行未加入房间前进行订阅
try {
  await testUplinkNetworkQuality();
  await testDownlinkNetworkQuality();
} catch (error) {
  console.error(error);
  return;
}
// 4. 30s 后停止检测，计算平均网络质量

setTimeout(() => {
  // 计算上行平均网络质量
  if (testResult.uplinkNetworkQualities.length > 0) {
    testResult.average.uplinkNetworkQuality = Math.round(
      testResult.uplinkNetworkQualities.reduce(
        (value, current) => value + current.quality,
        0
      ) / testResult.uplinkNetworkQualities.length
    );
  }
  if (testResult.downlinkNetworkQualities.length > 0) {
    // 计算下行平均网络质量
    testResult.average.downlinkNetworkQuality = Math.round(
      testResult.downlinkNetworkQualities.reduce(
        (value, current) => value + current.quality,
        0
      ) / testResult.downlinkNetworkQualities.length
    );
  }
  console.log("网络检测结果：", testResult);
  // 检测结束，清理相关状态。
  uplinkERTC.leaveRoom();
  downlinkERTC.leaveRoom();
}, 30 * 1000);
```

### 网络质量分析

拿到上下行平均网络质量后，可以对照下列枚举值，判断当前网络好坏：

| 数值 | 描述 |
| --- | --- |
| 1 | 网络状况优 |
| 2 | 网络状况良好 |
| 3 | 网络状况中 |
| 4 | 网络状况差 |
| 5 | 网络状况极差 |
| 6 | 网络状况不可用 |
| 0 | 网络状况未知 |