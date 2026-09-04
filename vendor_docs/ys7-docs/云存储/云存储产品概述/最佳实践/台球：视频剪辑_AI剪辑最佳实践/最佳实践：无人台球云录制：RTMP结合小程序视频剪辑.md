#  最佳实践：无人台球云录制：RTMP结合小程序视频剪辑

>  最佳实践：无人台球云录制：RTMP结合小程序视频剪辑

> 更新时间: 2026-05-25T16:36:51.000+08:00

> 文档ID: 4316 | 来源树: 云存储

---

# 最佳实践：无人台球云录制：RTMP结合小程序视频剪辑

## 典型客户

科行天下、小铁等

## 客户使用说明

选择订单

![](https://resource.eziot.com/group2/M00/01/03/CtwQF2gQjxyACiSxAACTpAjNLHQ905.png)

获取视频

![](https://resource.eziot.com/group2/M00/01/03/CtwQFmgQjnKAIhpUAAMXOnb-MJM955.png)

获取开始与结束时间

![](https://resource.eziot.com/group2/M00/01/03/CtwQFmgQj32ABXmBAALBGrcmKkk386.png)

![](https://resource.eziot.com/group2/M00/01/03/CtwQF2gQkFuAMl0JAAK1rgUBu4k256.png)

支付订单，开始给客户生成并下载

![](https://resource.eziot.com/group2/M00/01/03/CtwQFmgQkLWAOKbkAAEpIVcMETw098.png)

# API接口及接口说明

![](https://resource.eziot.com/group2/M00/01/03/CtwQFmgN4r-ATHEsAACbwZOII7I494.png)

## 0.前提说明

①开发者需要在台球桌侧上方安装摄像头，若需要推荐摄像头，可以联系海康/萤石销售进行销售。

②请在萤石开放平台注册开发者账号。如您已有开发者帐号，可以跳过这一步。

③在消息推送控制台开通消息推送服务 消息推送服务开通操作手册

## 步骤1：集成小程序插件SDK

由于小程序插件SDK是基于live-player提供的，若开发者需要自定义UI页面，开发者可以自行集成微信live-player组件。（可自行搜索）

若UI可以使用萤石提供的UI样式，则可以直接集成小程序插件SDK。

集成地址：<https://open.ys7.com/help/1865>

## 步骤2：云录制2.0进行云端录像

1）第一步：视频录制

通过创建云录制任务，可以将录像文件存储到云端。建议：当客户开台即可调用对应开始时间，然后当用户结账即可结束录制。

第1步：录制任务相关接口：<https://open.ys7.com/help/2045>

第2步：视频录制得到文件，可以通过接口查询云端是否有录制文件：<https://open.ys7.com/help/2042>

第3步：获取录制文件后，获取录像的RTMP播放地址：<https://open.ys7.com/help/2864>

2）第二步

由于萤石小程序SDK暂未提供多个时间点的抓取，因此多个时间点需要开发者自行提供

当客户选择两个时间点后，开发着将两个时间点保存后调用视频剪辑接口

3）第三步

视频剪辑：开发者将获取到的视频剪辑时间点传给视频剪辑接口，并选择对应的录制模板，即可获取最终的录制mp4文件：<https://open.ys7.com/help/2863>

①视频剪辑接口地址：https://open.ys7.com/help/2863

②通过传入步骤2返回的多个时间戳起止点，将视频进行裁剪，添加转场效果，并合成，最终返回剪辑任务ID

备注：如果要制作一段精彩的视频，可以通过上传片头片尾、背景音乐、转场视频等进行合成

③上传片头片尾、背景音乐、转场视频等 点击控制台-云点播，点击上传音视频

④添加转场动效

转场效果：参考：<https://open.ys7.com/help/3737>

⑤视频剪辑文件查询：https://open.ys7.com/help/3717

通过传入剪辑任务ID，返回剪辑视频URL。

【begin\_time，end\_time】

调用示例：

```
curl --location --request POST 'https://open.ys7.com/api/service/cloudrecord/video/convert' 
--header 'accessToken: {{accessToken}}' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'Content-Type: application/json' \
--data-raw '{
 "timeLine": [
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 },
 {
 // 使用对焦切换转场
 "type": "Transition",
 "subType": "directional"
 }
 ],
 "in": 0,// 算法分析出来的begin_time/1000
 "out": 2// 算法分析出来的end_time/1000
 },
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 },
 {
 // 使用对焦切换转场
 "type": "Transition",
 "subType": "directional"
 }
 ],
 "in": 8,// 算法分析出来的begin_time/1000
 "out": 10// 算法分析出来的end_time/1000
 },
 {
 "type": 1,
 "inputProjectId":"tqjcjj",
 "fileId": "ab9a385906be42aca6e6ac67a63a6ced",
 "effects": [
 {
 // 原视频静音
 "type": "Volume",
 "gain": 0
 }
 ],
 "in": 15,// 算法分析出来的begin_time/1000
 "out": 17// 算法分析出来的end_time/1000
 }
 ],
 // 背景音乐，需要在云点播中进行上传
 "audioTimeLines": [
 {
 "type": 3,
 "fileId": "l17q8HCC"
 }
 ],
 "fileName": "合成视频1"
}'

---响应

{
 "meta": {
 "code": 200,
 "message": "操作成功",
 "moreInfo": null
 },
 "data": {
 "taskId":"12314214"//剪辑任务id
 }
}
```

4）在线下载/点播

获取到剪辑好的视频后，用户就可以点播了，当然也可以上传到精彩视频库里进行点播，获取播放地址：<https://open.ys7.com/help/3717>