# ezuikit-js 预初始化

> ezuikit-js 预初始化描述

> 更新时间: 2026-05-25T16:44:28.000+08:00

> 文档ID: 4869 | 来源树: SDK及示例

---

# EZUIKit 预初始化

**请确保EZUIKit版本不低于8.1.14**

EZUIKit8.1.14及以上版本已支持提前获取设备取流播放所必须的参数。

通过提前获取取流播放所需的参数，减少SDK初始化耗时10%~15%。

## 预初始化流程示例

#### 1、在项目中引入EZUIKit

```
import EZUIKit from "ezuikit-js";
```

#### 2、调用EZUIKit抽象类暴露的静态方法提前获取参数

```
EZUIKit.EZUIKitPlayer.preInit({
  url: "ezopen://open.ys7.com/XXXXXXXXX/1.live",
  accessToken: "at.xxxxxx"
}).then((res) => {
  console.log("preInit success:", res);
}).catch((err) => {
  console.log("preInit fail:", err);
})
```

**入参说明**

| 字段 | 类型 | 含义 | 是否必填 | 备注 |
| --- | --- | --- | --- | --- |
| url | string | 播放地址 | 是 | 播放地址，规则与初始化的url相同 |
| accessToken | string | 鉴权token | 是 |  |
| env | object | 设备环境 | 否 | 详见海外&多语言文档 |
| token | object | 小权限token | 否 | 详见小权限token接入说明文档 |

#### 3、初始化SDK取流播放

```
const player = new EZUIKit.EZUIKitPlayer({
  id: "player",
  url: "ezopen://open.ys7.com/XXXXXXXXX/1.live",
  accessToken: "at.xxxxxx",
  width: 720,
  height: 480,
  ... // 其他初始化参数
})
```

## 注意事项

1、需要确保预初始化的参数与初始化时传入的保持一致，否则可能导致部分设备操作、播放器功能异常。

2、预初始化参数会在首次初始化完成后被清除。