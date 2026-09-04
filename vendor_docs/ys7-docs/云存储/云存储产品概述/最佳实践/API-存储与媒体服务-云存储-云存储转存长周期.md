# API-存储与媒体服务-云存储-云存储转存长周期

> API-存储与媒体服务-云存储-云存储转存长周期

> 更新时间: 2026-05-25T16:36:52.000+08:00

> 文档ID: 4982 | 来源树: 云存储

---

# 云存储录像转封装长期存储

> 该文档主要说明云存储如何转存长周期录像

## 场景说明

部分场景下，云存储开通7天循环、30天循环后，遇到一些场景需要把部分录像转存1年甚至更长周期录像，可参考该文档进行操作

| 场景 | 说明 | 备注 |
| --- | --- | --- |
| 连锁 | 场景：连锁门店一般会开通7天循环年套餐为主，但是如果遇到特殊事件，比如门店偷盗、门店破损事件等，则需要把门店该部分时间内的录像转存更长时间，比如1年或者5年 | 转成mp4存储更长时间 |
| 工地 | 场景：一般工地都是开通90天循环，或者1年循环为主，当遇到特殊事件：比如工地检查等，需要把当天甚至更长时间存储更久用作证据 | 转成mp4存储5年以上 |

## 云存储录像转封装

### **1.云点播空间管理**

由于云存储的产品定义是设备按月进行套餐开通，因此该产品暂时不支持空间管理等功能，在云存储产品上，我们有一套统一的空间管理功能模块，需要创建额外的存储空间进行管理。

可以通过空间管理相关接口，维护不同过期天数的存储空间，默认存储空间是永久存储。
  
相关接口列表如下

| 产品名称 | 功能点 | 接口名称 | 操作 |
| --- | --- | --- | --- |
| 云存储 | 空间管理 | 录像空间创建（POST） | [查看详情](https://open.ys7.com/help/4470) |
|  |  | 录像空间修改（PUT） | [查看详情](https://open.ys7.com/help/4471)  **注意：修改空间过期天数，只对新文件生效** |
|  |  | 录像空间删除（DELETE） | [查看详情](https://open.ys7.com/help/4472) |
|  |  | 录像空间列表查询（GET） | [查看详情](https://open.ys7.com/help/4473) |

### **2.提交转封装任务**

云存储的录像由于是按时间、按设备，是萤石私有的存储格式，是ps格式，因此要转成通用的存储，需要转存成mp4等格式进行存储。

云端录像转封装任务创建接口： [查看详情](https://open.ys7.com/help/3971)
请求示例

```
curl --location 'https://open.ys7.com/api/service/open/vod/media/trans/code' \
--header 'localIndex: 1' \
--header 'User-Agent: Apifox/1.0.0 (https://apifox.com)' \
--header 'accessToken: at.320gyv2s66ry9ggw0549qegu2apcsr2' \
--header 'deviceSerial: BC30551' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'busType=1' \  // 1:事件云存储 ; 
--data-urlencode 'startTime=2025-06-04 21:45:30' \
--data-urlencode 'endTime=2025-06-04 21:46:30' \
--data-urlencode 'format=MP4' \  // 转封装格式
--data-urlencode 'resultSpaceId=44028'   // 输出结果的云点播空间id ,不填写时使用默认云点播vodspace
```

创建转封装任务后，该接口返回示例如下，对应的taskId即为转封装任务id

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": {
        "taskId": "9c7802d2f9bf463794e2c0d"
    }
}
```

### **3.等待任务状态完成**

可以通过如下两种方式等待转封装任务完成

| 方式 | 操作内容 | 文档 |
| --- | --- | --- |
| webhook消息回调 | 通过webhook消息通知，监听转封装文件消息 | 前提条件: 在消息推送控制台开通消息推送服务，并勾选云录制消息，云录制消息类型：ys.open.cloud，  1、 [消息推送服务开通操作手册](https://open.ys7.com/help/566)   2、对接对应消息，消息报文文档 [录制结果回调消息](https://open.ys7.com/help/1384) ，云点播转封装子任务文件消息（video\_transcode\_sub\_file）的消息， 3、从消息报文中解析文件节点集合fileNodeIds，即为转封装的云点播文件 |
| webhook消息回调 | 通过webhook消息通知，监听任务状态为完成 | 前提条件: 在消息推送控制台开通消息推送服务，并勾选云录制消息，云录制消息类型：ys.open.cloud，  1、 [消息推送服务开通操作手册](https://open.ys7.com/help/566)   2、对接对应消息，消息报文文档 [录制结果回调消息](https://open.ys7.com/help/1384) ，处理messageType为 云点播转封装任务（video\_transcode）和 云点播转封装子任务（video\_transcode\_sub）的消息， 3、当taskStatus任务状态变成 COMPLETE(0, "已完成")，表示转封装任务已完成 |
| 周期轮询 | 周期轮询任务详情接口，并等待转封装任务完成 | 1、周期轮询任务详情，对应接口文档[查询任务详情](https://open.ys7.com/help/3972)  2、当taskStatus任务状态变成 COMPLETE(0, "已完成")，表示转封装任务已完成 |

### **4.查询转封装任务的文件列表**

待转封装任务正常完成后，可通过接口查询转封装文件列表： [查看详情](https://open.ys7.com/help/3717)

```
curl --location 'https://open.ys7.com/api/service/open/cloud/vod/task/files/997d83b69113414e9309830158aa2a15?expireSeconds=172800' \ // /api/service/open/cloud/vod/task/files/{taskId}，path路径的任务id，即为上述转封装任务id
--header 'accessToken: at.4x3isq8k85t2bfkw3pda1yv22wep1csq'
```

接口响应示例，拿到该响应结果，即可拿到**对应的folderNode(文件ID)和fileUrl(文件地址)**

```
{
    "meta": {
        "code": 200,
        "message": "操作成功",
        "moreInfo": null
    },
    "data": [
        {
            "folderNode": "r8gzkZPs",
            "fileName": "录像BD57407-1-20250402193258-20250402193759",
            "fileUrl": "https://openrecord.ys7.com/3650/BD5740777-1-c1cbc1d4e86d49a0981f5a-20250402193258-20250402193759-1645.mp4?Expires=1749875940&OSSAccessKeyId=LTAI4G6HFM3XPqa8rBjxHJRE&Signature=3KnrwBQ1tVR%2FGqlvah5Rfb%2FCfzU%3D&auth_key=1749791340-0-bde271cfa40d4ae3a0aa066bd913ac85-64a9fbade2b42133423f50856cdae437",
            "coverPic": "E1/1o4/14/c1cbc1d4e86d49a0981f54beea95280a/0/PTdbM2g/N1/e65d3b9b15b44baeb9cfea2c3a4/0/ae0bde06.jpg",
            "coverPicUrl": "https://openrecord.ys7.com/E1/1o4/14/c1cbc1d4e86d49a0981f54beea95280a/0/PTdbM2g/N1/e65d3b9b15aeb9cf93409ea2c3a4/0/ae0bde06.jpg?Expires=1749793140&OSSAccessKeyId=LTAI4G6HFM3XPqa8rBjxHJRE&Signature=y9jtzijDXz1a%2F8lZxy%2FpKDjXho8%3D&auth_key=1749791340-0-26f6637a1ff2409795527198d84687e0-76f7b53cfbe8a40314256c9532ff8740",
            "startTime": "2025-04-02 19:32:58",
            "stopTime": "2025-04-02 19:37:59",
            "fileSize": 19454699
        }
    ]
}
```

### **5.根据folderNode使用**

通过上述步骤，拿到云点播的文件节点(folderNode)后，  
可以直接根据folderNode来获取文件信息： [查看详情](https://open.ys7.com/help/4187)

```
curl --location 'https://open.ys7.com/api/service/open/vod/files?fileNodeIds=RGgho7%2CRnOops' \
--header 'accessToken: at.8bffs4pg6yedu84gcl0aauv24v'
```

也可以直接根据folderNode来获取文件链接： [查看详情](https://open.ys7.com/help/4402)

```
curl --location 'https://open.ys7.com/api/service/open/vod/file/downloadurl?expireSeconds=86400&fileNodeIds=6TeITTr2' \
--header 'accessToken: at.4x3isq8k85t2bfkw3pda1yv22wep1csq'
```

**拿到文件链接后，就可以在线访问或者下载了**