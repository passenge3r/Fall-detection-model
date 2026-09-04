# ertc-web & 智能体语音对讲

> ertc-web & 智能体语音对讲

> 更新时间: 2026-05-25T16:37:59.000+08:00

> 文档ID: 5165 | 来源树: AI

---

# ertc-web & 智能体语音对讲 接入指南

## 概述

本文档介绍如何基于 `ertc-web` 库接入智能体语音对讲能力。通过该方案，开发者可以在 Web 端实现与 AI 智能体的实时语音通话，并支持实时字幕（ASR 文字回传）、音量监听等功能。

## 目录

- [环境要求](#%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82)
- [安装依赖](#%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96)
- [类型声明](#%E7%B1%BB%E5%9E%8B%E5%A3%B0%E6%98%8E)
- [快速开始](#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
- [核心 API](#%E6%A0%B8%E5%BF%83-api)
- [完整接入示例](#%E5%AE%8C%E6%95%B4%E6%8E%A5%E5%85%A5%E7%A4%BA%E4%BE%8B)
- [事件监听](#%E4%BA%8B%E4%BB%B6%E7%9B%91%E5%90%AC)
- [字幕消息数据结构](#%E5%AD%97%E5%B9%95%E6%B6%88%E6%81%AF%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)
- [常见问题](#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

---

## 环境要求

- 浏览器需支持 WebRTC（Chrome 70+、Firefox 60+、Safari 12+），详细见Webrtc 兼容情况：<https://open.ys7.com/help/1905>
- 需要 HTTPS 环境（WebRTC 要求安全上下文），localhost 开发环境除外

## 安装依赖

当前文档基于 `ertc-web@2.1.3-alpha.18` 版本编写，最新版本详见：<https://open.ys7.com/help/1905>

```
npm install ertc-web@2.1.3-alpha.18
# 或
pnpm add ertc-web@2.1.3-alpha.18
```

## 类型声明

```
declare module 'ertc-web' {
  class ERTC {
    constructor(config: ERTCConfig);
    /** 注册插件（静态方法） */
    static extend: (plugins: any[]) => void;
    /** 发起智能体语音呼叫 */
    agentCall: (config: AgentCallConfig) => Promise<void>;
    /** 停止/挂断当前通话 */
    agentStop: () => Promise<void>;
    /** 监听本地麦克风音量变化 */
    observeVolumeChange: (config: VolumeObserverConfig) => void;
    /** 注册事件监听 */
    on: (event: string, callback: Function) => void;
    /** 移除事件监听 */
    remove: (event: string, callback: Function) => void;
  }
  export default ERTC;
}
```

### 参数类型说明

```
/** ERTC 构造函数配置 */
interface ERTCConfig {
  /** 是否开启调试日志 */
  debug?: boolean;
}

/** agentCall 呼叫参数 */
interface AgentCallConfig {
  /** 用户鉴权 Token */
  accessToken: string;
  /** ERTC 应用 ID（在 RTC 平台创建的项目 ID） */
  ertcAppId: string;
  /** 智能体应用 ID */
  agentAppId: string;
}

/** 音量监听配置 */
interface VolumeObserverConfig {
  /** 音量回调触发间隔（毫秒） */
  interval: number;
  /** 音量回调函数，audioLevel 范围 0~1 */
  callback: (audioLevel: number) => void;
}
```

---

## 快速开始

接入分为 4 步：初始化 → 发起呼叫 → 监听事件 → 挂断清理。

### 1. 初始化 ERTC 实例

```
import ERTC from 'ertc-web';
import { TalkAgent } from 'ertc-web/plugins';

// 注册智能体对讲插件（全局只需执行一次）
ERTC.extend([new TalkAgent()]);

// 创建实例
const ertc = new ERTC({
  debug: true,       // 开发阶段建议开启
});
```

> **注意**：`ERTC.extend()` 是静态方法，全局调用一次即可。`new ERTC()` 建议在组件外部创建，避免重复实例化。

### 2. 发起呼叫

```
ertc.agentCall({
  accessToken: 'your-access-token',
  ertcAppId: 'your-ertc-app-id',
  agentAppId: 'your-agent-app-id'
})
.then(() => {
  console.log('通话已接通');
  // 在此处开始监听音量、字幕等事件
})
.catch((err) => {
  console.error('呼叫失败:', err.msg || err.message);
});
```

### 3. 挂断 / 停止通话

```
ertc.agentStop();
```

---

## 核心 API

| 方法 | 说明 | 返回值 |
| --- | --- | --- |
| `ERTC.extend(plugins)` | 注册插件（静态方法，全局调用一次） | `void` |
| `ertc.agentCall(config)` | 发起智能体语音呼叫 | `Promise<void>` |
| `ertc.agentStop()` | 挂断/停止当前通话 | `Promise<void>` |
| `ertc.observeVolumeChange(config)` | 监听本地麦克风音量 | `void` |
| `ertc.on(event, callback)` | 注册事件监听 | `void` |
| `ertc.remove(event, callback)` | 移除事件监听 | `void` |

---

## 事件监听

### `custommsg` — 实时字幕/文字消息

通话建立后，智能体会通过 `custommsg` 事件回传 ASR 识别文字和智能体回复文字。

```
ertc.on('custommsg', (data: { msg: string }) => {
  const parsed = JSON.parse(data.msg);

  // parsed 结构：
  // {
  //   textId: string,         // 文本消息唯一标识
  //   data: {
  //     type: 1 | 2,          // 1 = 用户语音识别文字, 2 = 智能体回复文字
  //     text: string,         // 文字内容（增量更新，同一 textId 的 text 会不断补全）
  //   }
  // }

  const roleMap = { 1: 'user', 2: 'assistant' };
  const role = roleMap[parsed.data.type];
  const uniqueKey = `${parsed.textId}_${role}`;

  if (!parsed.data.text) return; // 空内容直接忽略

  // 根据 uniqueKey 判断是更新已有消息还是新增消息
  // 同一个 textId + role 的消息，text 字段会持续更新
});
```

### `error` — 错误事件

```
ertc.on('error', (err: { message?: string; msg?: string }) => {
  console.error('通话异常:', err.message || err.msg);
});
```

> **提示**：注册事件监听前，建议先调用 `ertc.remove(event, fn)` 移除同一回调引用，避免重复监听。

---

## 音量监听

通话接通后调用 `observeVolumeChange` 可实时获取本地麦克风输入音量，用于驱动音量动画等 UI 效果。

```
ertc.observeVolumeChange({
  interval: 150,  // 每 150ms 回调一次
  callback: (audioLevel: number) => {
    // audioLevel 范围 0 ~ 1
    // 可用于驱动音量条动画
    setVolume(audioLevel);
  }
});
```

---

## 完整接入示例

以下是一个 React 组件的完整接入示例，包含呼叫、挂断、音量监听、字幕显示的完整流程：

```
import { useState, useEffect, useCallback } from 'react';
import ERTC from 'ertc-web';
import { TalkAgent } from 'ertc-web/plugins';

// ========== 1. 初始化（组件外部，全局执行一次） ==========
ERTC.extend([new TalkAgent()]);
const ertc = new ERTC({ debug: true });

// ========== 2. 字幕消息类型 ==========
interface VoiceMessage {
  role: 'user' | 'assistant';
  content: string;
  key: string;
  typing?: boolean;
}

type CallStatus = 'wait' | 'calling' | 'talking';

// ========== 3. 组件实现 ==========
export default function VoiceChat({
  accessToken,
  ertcAppId,
  agentAppId,
  onClose
}: {
  accessToken: string;
  ertcAppId: string;
  agentAppId: string;
  onClose: () => void;
}) {
  const [status, setStatus] = useState<CallStatus>('wait');
  const [volume, setVolume] = useState(0);
  const [messages, setMessages] = useState<VoiceMessage[]>([]);

  // ---- 发起呼叫 ----
  const handleCall = useCallback(() => {
    if (status !== 'wait') return;
    setStatus('calling');

    ertc
      .agentCall({ accessToken, ertcAppId, agentAppId })
      .then(() => {
        setStatus('talking');
        startListeners();
      })
      .catch((err) => {
        setStatus('wait');
        console.error('呼叫失败:', err.msg || err.message);
      });
  }, [status, accessToken, ertcAppId, agentAppId]);

  // ---- 挂断 ----
  const handleHangup = useCallback(() => {
    ertc.agentStop();
    setStatus('wait');
    onClose();
  }, [onClose]);

  // ---- 事件回调（保持引用稳定，便于 remove） ----
  const onCustomMsg = (data: { msg: string }) => {
    const parsed = JSON.parse(data.msg);
    const roleMap: Record<number, 'user' | 'assistant'> = {
      1: 'user',
      2: 'assistant'
    };
    if (!parsed.data.text) return;

    const role = roleMap[parsed.data.type];
    const key = `${parsed.textId}_${role}`;

    setMessages((prev) => {
      const existing = prev.find((m) => m.key === key);
      if (existing) {
        return prev.map((m) =>
          m.key === key ? { ...m, content: parsed.data.text } : m
        );
      }
      return [...prev, { role, content: parsed.data.text, key, typing: true }];
    });
  };

  const onError = (err: any) => {
    console.error('通话异常:', err?.message || err?.msg);
    handleHangup();
  };

  // ---- 注册事件监听 ----
  const startListeners = () => {
    // 音量监听
    ertc.observeVolumeChange({
      interval: 150,
      callback: (audioLevel: number) => setVolume(audioLevel)
    });

    // 先移除再监听，避免重复注册
    ertc.remove('custommsg', onCustomMsg);
    ertc.on('custommsg', onCustomMsg);

    ertc.remove('error', onError);
    ertc.on('error', onError);
  };

  // ---- 组件卸载时清理 ----
  useEffect(() => {
    return () => {
      ertc.agentStop();
    };
  }, []);

  return (
    <div>
      <div>状态: {status}</div>
      <div>音量: {volume}</div>

      {/* 字幕列表 */}
      <div>
        {messages.map((msg) => (
          <div key={msg.key}>
            <strong>{msg.role === 'user' ? '我' : '智能体'}:</strong>
            <span>{msg.content}</span>
          </div>
        ))}
      </div>

      {/* 操作按钮 */}
      {status === 'wait' && <button onClick={handleCall}>拨打</button>}
      {status === 'calling' && <span>接通中...</span>}
      {status === 'talking' && <button onClick={handleHangup}>挂断</button>}
    </div>
  );
}
```

---

## 通话状态流转

```
wait ──(agentCall)──> calling ──(Promise resolve)──> talking
  ^                      |                              |
  |                      |  (Promise reject)            |  (agentStop / error)
  └──────────────────────┘──────────────────────────────┘
```

| 状态 | 说明 |
| --- | --- |
| `wait` | 空闲，等待用户操作 |
| `calling` | 呼叫中，等待接通 |
| `talking` | 通话中，可进行语音交互 |

---

## 字幕消息数据结构

`custommsg` 事件回调中 `JSON.parse(data.msg)` 的结构：

```
interface CaptionMessage {
  /** 文本消息唯一 ID，同一段话的增量更新共享同一个 textId */
  textId: string;
  data: {
    /** 消息类型：1 = 用户（ASR识别），2 = 智能体回复 */
    type: 1 | 2;
    /** 文字内容（增量覆盖，非追加） */
    text: string;
    /** 该段文字是否已完成 */
    finished: boolean;
  };
}
```

> **关键点**：同一个 `textId + role` 的消息，`text` 字段是覆盖式更新（不是追加），直接用最新的 `text` 替换之前的内容即可。

---

## 常见问题

### Q: 呼叫失败，提示接通失败？

- 检查 `accessToken` 是否有效且未过期
- 检查 `ertcAppId` 和 `agentAppId` 是否正确
- 确认浏览器已授予麦克风权限
- 确认当前网络环境可访问 ERTC 服务域名

### Q: 听不到智能体声音？

- 检查浏览器是否有自动播放策略限制（需用户交互后才能播放音频）
- 确认设备音频输出设备正常

### Q: 字幕不显示？

- 确认已在 `agentCall` 成功回调中注册了 `custommsg` 事件监听
- 检查 `data.msg` 是否能正常 JSON 解析
- 注意过滤 `text` 为空的消息

### Q: 重复收到字幕消息？

- 确保注册监听前先调用 `ertc.remove(event, fn)` 移除旧的监听器
- 避免在组件重渲染时重复注册事件

### Q: 组件卸载后仍有通话？

- 务必在组件的 `useEffect` 清理函数中调用 `ertc.agentStop()` 确保通话断开