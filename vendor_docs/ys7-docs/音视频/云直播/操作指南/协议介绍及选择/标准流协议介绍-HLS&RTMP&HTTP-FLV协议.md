# 标准流协议介绍-HLS&RTMP&HTTP-FLV协议

> 标准流协议介绍-HLS&RTMP&HTTP-FLV协议

> 更新时间: 2026-05-25T16:36:09.000+08:00

> 文档ID: 1752 | 来源树: 音视频

---

# 标准流直播协议

## 基本概念

HLS/RTMP/HTTP-FLV这几个协议是常见的直播标准协议，萤石开放平台除了提供ezopen协议外，还提供了HLS、RTMP、HTTP-FLV标准流协议供开发者接入

## RTMP介绍

RTMP （Real Time Messaging Protocol），即“实时消息传输协议”， 它实际上并不能做到真正的实时，一般情况最少都会有几秒到几十秒的延迟，是 Adobe 公司开发的音视频数据传输的实时消息传送协议，RTMP 协议基于 TCP，包括 RTMP 基本协议及 RTMPT/RTMPS/RTMPE 等多种变种，RTMP 是目前主流的流媒体传输协议之一，对CDN支持良好，实现难度较低，是大多数直播平台的选择，不过RTMP有一个最大的不足 —— 不支持浏览器，且苹果 ios 不支持，Adobe 已停止对其更新

RTMP目前在 PC 上的使用仍然比较广泛。

`注意：`RTMP依赖Flash Player，由于Chrome浏览器已经下架，因此无法在主流浏览器里支持。

## HTTP-FLV介绍

FLV（全称 Flash Video）是一种流媒体格式，由 Adobe 公司开发，并在 2003 年发布。而HTTP-FLV意思即使用HTTP协议流式的传输媒体内容，http\_flv&rtmp这两个协议实际上传输数据是一样的，数据都是flv文件的tag。基于http传输flv方式，flash player,主流播放器都能很好支持，延迟1-3秒左右。

## HLS介绍

HLS （Http Live Streaming）是由苹果公司定义的基于 HTTP 的流媒体实时传输协议，被广泛的应用于视频点播和直播领域，HLS 规范规定播放器至少下载一个 ts 切片才能播放，所以 HLS 理论上至少会有一个切片的延迟

HLS 在移动端兼容性比较好，ios就不用说了，Android现在也基本都支持 HLS 协议了，pc端如果要使用可以使用 hls.js 适配器

> HLS 的原理是将整个流分为多个小的文件来下载，每次只下载若干个，服务器端会将最新的直播数据生成新的小文件，当客户端获取直播时，它通过获取最新的视频文件片段来播放，从而保证用户在任何时候连接进来时都会看到较新的内容，实现近似直播的体验；HLS 的延迟一般会高于普通的流媒体直播协议，传输内容包括两部分：一部分 M3U8 是索引文件，另一部分是 TS 文件，用来存储音视频的媒体信息

---

## 协议对比

与标准流协议对比，ezopen在通用兼容性上是有所不足的，因此开发者需要根据自己的实际应用需求进行选择。

协议对比内容可以参见：[协议对比](/help/1753)

## 标准流直播协议格式

标准流的获取，可以参考直播地址获取地址：[前往获取](/help/1414)

详细格式如下：

#### **HLS协议**

https://open.ys7.com/v3/openlive/设备ID\_清晰度.m3u8?expire=1722172888&id=607322167286378496&t=5e61826cfe5910a5ecdc4c4b704ba28f2f62d3ea955a7c306885eaa714ae6b89&ev=100

#### **RTMP协议**

rtmp://xyrtmp.ys7.com:1935/v3/openlive/设备ID\_清晰度?expire=1722172888&id=607322166882480128&t=d8509e6b863f1145d753f8e6f4f94cd2e4b592ec33f0bc78dfcbbbf2d267afc4&ev=100&vc=3&supportH265=1

#### **HTTP-FLV协议**

https://xyrtmp.ys7.com:9188/v3/openlive/设备ID\_清晰度.flv?expire=1722172888&id=607322167100575744&t=1f723e53a1d408687c38c20a0d34b1f7d66b4557b6be6f71f64a7d1d96ea19ed&ev=100\*\*