# capacity.md

> 设备能力集说明

> 更新时间: 2026-05-25T16:38:09.000+08:00

> 文档ID: 77 | 来源树: OPEN_API

---

### 设备能力集介绍

设备能力集是用来表征设备所具有的能力的一个集合.根据设备能力集,可以明确 的知道,设备支持哪些功能.

> 由于能力集会持续更新,如发现该说明不存在的字段,请及时反馈open-team@ezvizlife.com

用户可以通过调用[查询设备能力集接口](https://open.ys7.com/help/678)来获取设备能力集

| 序号 | 字段 | 能力集字段说明 |
| --- | --- | --- |
| 1 | support\_defence | 是否支持布撤防,活动检测开关 |
| 2 | support\_talk | 是否支持对讲: 0-不支持, 1-全双工, 3-半双工 |
| 3 | support\_defenceplan | 是否支持布撤防计划 0-不支持， 1-支持,2-支持新的设备计划协议 |
| 4 | support\_disk | 是否支持存储格式化 0-不支持, 1-支持 |
| 5 | support\_privacy | 是否支持隐私保护 0-不支持, 1-支持 |
| 6 | support\_message | 是否支持留言 0-不支持, 1-支持 |
| 7 | support\_alarm\_voice | 是否支持告警声音配置 0-不支持, 1-支持 |
| 8 | support\_auto\_offline | 是否支持设备自动上下线 0-不支持, 1-支持 |
| 9 | supprot\_encrypt | 是否支持视频图像加密 0-不支持, 1-支持 |
| 10 | support\_upgrade | 是否支持设备升级 0-不支持, 1-支持 |
| 11 | support\_cloud | 该设备型号是否支持云存储 0-不支持, 1-支持 |
| 12 | support\_cloud\_version | 该设备版本是否支持云存储 0-不支持, 1-支持 需要和support\_cloud组合使用: support\_cloud = 1 , support\_cloud\_version = 1 才支持云存储 support\_cloud =1 ,support\_cloud\_version = 0,该型号的设备支持云存储,但是当前固件版本不支持云存储 support\_cloud = 0 该型号的设备不支持云存储 |
| 13 | support\_wifi | 是否支持WI-FI: 0-不支持, 1-支持netsdk配置WI-FI,2-支持带userId的新WI-FI配置方式,3-支持一键配置WI-FI |
| 14 | support\_capture | 是否支持封面抓图: 0-不支持, 1-支持 |
| 15 | support\_modify\_pwd | 是否支持修改设备加密密码: 0-不支持, 1-支持 |
| 16 | support\_resolution | 视频播放比例 16-9表示16:9分辨率,默认16-9 |
| 17 | support\_multi\_screen | 是否支持多画面播放 0-不支持, 1-支持(客户端使用,与设备无关) |
| 18 | support\_upload\_cloud\_file | 是否支持手机拍照上传到云存储 0-不支持，1-支持 |
| 19 | support\_add\_del\_detector | 是否支持app远程添加删除外设(探测器): 0-不支持, 1-支持 |
| 20 | support\_ipc\_link | 是否支持IPC与A1联动关系设置: 0-不支持, 1-支持 |
| 21 | support\_modify\_detectorname | 是否支持修改外设(探测器)名称: 0-不支持, 1-支持 |
| 22 | support\_safe\_mode\_plan | 是否支持定时切换安全功能模式: 0-不支持, 1-支持 |
| 23 | support\_modify\_detectorguard | A1设备是否支持单独布撤防: 该字段不存在:不支持  该字段存在:各个外设用逗号隔开，如表顺序排列，每个值32位数值按位标识每种模式下是否可以设置某个模式下，某个探测器如果可以设置使能这个参数，就该位置1 例如"support\_modify\_guard":"0,0,7,7,7,0,7,0,0,0" 为下面的能力说明  探测器类型 | 外出模式(bit0) | 睡眠模式(bit1) | 在家模式(bit2) || 烟感 | 0 | 0 | 0 || | 紧急按钮 | 0 | 0 | 0 || | 门磁 | 1 | 1 | 1 || | 红外 | 1 | 1 | 1 || | 幕帘 | 1 | 1 | 1 || | 紧急按钮 | 0 | 0 | 0 || | 单体门磁 | 1 | 1 | 1 || | 警号 | 0 | 0 | 0 || | 燃气探测器 | 0 | 0 | 0 || | 水患探测器 | 0 | 0 | 0 || |
| 24 | support\_weixin | 是否支持微信互联:0-不支持, 1-支持 |
| 25 | support\_ssl | 是否支持声源定位:0-不支持, 1-支持 |
| 26 | support\_related\_device | 是否支持关联设备 0-无关联设备, 1-关联监控点或N1, 2-关联探测器或A1, 3-关联监控点探测器或R1, 4-关联多通道设备 |
| 27 | support\_related\_storage | NVR/R1是否支持关联IPC存储: 0-不支持, 1-支持 |
| 28 | support\_remote\_auth\_randcode | 是否支持设备远程授权获取密码, 0-不支持, 1-支持 |
| 29 | support\_sdk\_transport | 是否支持设备跨公网配置的能力级：0-不支持, 1-支持 |
| 30 | ptz\_top\_bottom | 是否支持云台上下转动 0-不支持, 1-支持 |
| 31 | ptz\_left\_right | 是否支持云台左右转动 0-不支持, 1-支持 |
| 32 | ptz\_45 | 是否支持云台45度方向转动 0-不支持, 1-支持 |
| 33 | ptz\_zoom | 是否支持云台缩放控制 0-不支持, 1-支持 |
| 34 | ptz\_preset | 是否支持云台预置点 0-不支持, 1-支持 |
| 35 | ptz\_common\_cruise | 是否支持普通巡航 0-不支持, 1-支持 |
| 36 | ptz\_figure\_cruise | 是否支持花样巡航0-不支持, 1-支持 |
| 37 | ptz\_center\_mirror | 是否支持中心镜像0-不支持, 1-支持 |
| 38 | ptz\_left\_right\_mirror | 是否支持左右镜像 0-不支持, 1-支持 |
| 39 | ptz\_top\_bottom\_mirror | 是否支持上下镜像 0-不支持, 1-支持 |
| 40 | ptz\_close\_scene | 是否支持关闭镜头 0-不支持, 1-支持 |
| 41 | support\_wifi\_2.4G | 是否支持2.4G无线频段 0-不支持, 1-支持 |
| 42 | support\_wifi\_5G | 是否支持5G无线频段 0-不支持, 1-支持 |
| 43 | support\_wifi\_portal | 是否支持营销wifi，只有support\_wifi\_2.4G=1的时候才生效：1-支持但不能设置营销页（X1），2-支持且可以设置营销页，0-不支持 |
| 44 | support\_unbind | 是否支持用户解绑设备 0-不支持, 1-支持reset键解绑，2-支持界面点击确定按钮解绑 |
| 45 | support\_auto\_adjust | 是否支持自适应码流 0-不支持, 1-支持 |
| 46 | support\_timezone | 是否支持时区配置 0-不支持, 1-支持 |
| 47 | support\_language | 支持的语言类型：ENGLISH,SIMPCN,.... |
| 48 | support\_close\_infrared\_light | 是否支持红外开关 0-不支持, 1-支持 |
| 49 | support\_modify\_chan\_name | 是否支持通道名称配置到设备（IPC/NVR) 0-不支持, 1-支持 |
| 50 | support\_ptz\_model | 0-支持直连+转发云台控制， 1-支持直连云台控制，2-支持转发云台控制 |
| 51 | support\_talk\_type | 0-采用上面的麦克风, 1-对讲采用下面的麦克风 |
| 52 | support\_chan\_type | 通道类型，1-数字通道，2-模拟通道 |
| 53 | support\_flow\_statistics | 是否支持客流统计 0-不支持, 1-支持 |
| 54 | support\_more | 是否支持设备设置功能 0-不支持, 1-支持   注:设备设置页面新增"更多配置"，该项按【设备能力级】实现，更多配置进入H5网页展现 |
| 55 | support\_remote\_quiet | A1是否支持远程消警（静音）功能 0-不支持, 1-支持 |
| 56 | support\_customize\_rate | 是否支持自定义码率 0-不支持, 1-支持 |
| 57 | support\_rectify\_image | 是否支持畸形矫正 0-不支持, 1-支持 |
| 58 | support\_bluetooth | 是否支持蓝牙 0-不支持, 1-支持 |
| 59 | support\_p2p\_mode | 默认0，表示老的p2p协议；配置为1，表示该版本支持新的p2p协议 |
| 60 | support\_microscope | 是否支持显微镜功能 0-不支持, 1-支持 |
| 61 | support\_sensibility\_adjust | 是否支持移动侦测灵敏度调节 0-不支持, 1-支持 |
| 62 | support\_sleep | 是否支持睡眠功能 0-不支持, 1-支持 |
| 63 | support\_audio\_onoff | 是否支持声音开关设置 0-不支持, 1-支持 |
| 64 | support\_protection\_mode | 0：无防护模式，可能有活动检测（根据support\_denfence(序号1)判断） 1：只有防护模式2：有防护模式，可能有活动检测（根据support\_denfence判断(序号1))能力级配置情况举例：   | support\_protection\_mode | support\_denfence || A1 | 1 | 1 | | 普通IPC | 0 1 || C1S | 2 | 1 | | |
| 65 | support\_rate\_limit | 是否支持高清码率限制 0-不支持码率限制, 1-支持高清码率限制 |
| 66 | support\_userId | 是否支持通过UserID关联设备 0-不支持, 1-支持 |
| 67 | support\_music | 是否支持儿歌播放功能 0-不支持, 1-支持 |
| 68 | support\_replay\_speed | 是否支持调节回放播放速度功能 0-不支持, 1-支持(仅IPC支持) |
| 69 | support\_reverse\_direct | 是否支持反向直连功能 0-不支持, 1-支持 |
| 70 | support\_channel\_offline\_notify | 是否支持通道下线通知,支持后通道下线会触发ideoloss的告警 0-不支持, 1-支持 |
| 71 | support\_fullscreen\_ptz | 是否支持全景云台功能 0-不支持, 1-支持(C6B等云台摄像机支持).如存在能力集support\_fullscreen\_ptz\_12(序号82),则优先参考能力集support\_fullscreen\_ptz\_12 |
| 72 | support\_preset\_alarm | 是否支持预置点告警联动 0-不支持, 1-支持(C6B等云台摄像机支持) |
| 73 | support\_intelligent\_track | 是否支持智能跟踪 0-不支持, 1-支持(C6B等云台摄像机支持) |
| 74 | support\_key\_focus | 是否支持一键聚焦 0-不支持, 1-支持(F1、F2等变焦摄像机支持) |
| 75 | support\_volumn\_set | 是否支持音量调节 0-不支持, 1-支持 |
| 76 | support\_temperature\_alarm | 是否支持温湿度告警 0-不支持, 1-支持( F2、C1S等带温湿度传感器的摄像机支持) |
| 77 | support\_mcvolumn\_set | 是否支持麦克风音量调节：0-不支持，1-支持 |
| 78 | support\_unlock | 是否支持支持开锁 0-不支持, 1-支持 |
| 79 | support\_noencript\_via\_antproxy | 是否支持支持走代理时可以自动加密“没有开启视频加密”的流 0-不支持, 1-支持 |
| 80 | support\_device\_offline\_notify | 是否支持设备下线通知 0-不支持, 1-支持 |
| 81 | support\_fullscreen\_ptz\_12 | 是否支持全景云台功能 0-不支持, 1-支持(C6B等云台摄像机支持,12张全景云台图片) |
| 82 | support\_speech\_recognition | 是否支持语音识别 0-不支持, 1-支持 |
| 83 | support\_message\_cover | 是否支持留言封面 0-不支持, 1-支持 |
| 84 | support\_nat\_pass | 是否支持NAT组合为3-4的NAT穿透（P2PV2.1） 0-不支持, 1-支持 |
| 85 | support\_nvr\_whitelist | NVR是否支持白名单成员管理 0-不支持, 1-支持 |
| 86 | support\_voice\_alarmclock | 是否支持语音闹钟功能 0-不支持, 1-支持 |
| 87 | support\_new\_talk | 是否支持新对讲服务 0-不支持, 1-支持 |
| 88 | support\_fullday\_record | 是否支持全天录像配置开关 0-不支持, 1-支持 |
| 89 | support\_query\_play\_connections | 是否支持查询当前预览，回放链接信息 0-不支持, 1-支持 |
| 90 | support\_ptz\_auto\_reset | 是否支持云台自动复位 0-不支持, 1-支持 |
| 91 | support\_fisheye\_mode | 是否支持鱼眼模式 0-不支持, 1-支持 |
| 92 | support\_custom\_voice | 是否支持自定义语音 0-不支持, 1-支持(语音闹钟，告警声音使用) |
| 93 | support\_new\_sound\_wave | 是否支持声波配置（高频版本） 0-不支持, 1-支持 |
| 94 | replay\_chan\_nums | X3或者N1可以关联的通道数 |
| 95 | support\_horizontal\_panoramic | 是否支持水平全景 0-不支持, 1-支持 |
| 96 | support\_active\_defense | 是否支持主动防御功能：0-不支持，1-主动防御按钮，2-主动防御按钮+灯光提醒开关 |
| 97 | support\_motion\_detect\_area | 是否支持移动侦测区域绘制 0-不支持, 1-支持 |
| 98 | support\_chan\_defence | 是否支持通道布撤防 0-不支持, 1-支持 |
| 99 | ptz\_focus | 是否支持焦距模式 0-不支持, 1-支持 |
| 100 | support\_pir\_detect | 是否支持红外检测能力 0-不支持, 1-支持(猫眼) |
| 101 | support\_doorbell\_talk | 是否支持门铃呼叫能力 0-不支持, 1-支持(猫眼) |
| 102 | support\_face\_detect | 是否支持人脸检测能力 0-不支持, 1-支持(猫眼) |
| 103 | support\_restart\_time | 设备重启时间，配置单位为秒数，默认120s |
| 104 | support\_human\_filter | 是否支持人形过滤能力 0-不支持, 1-支持)(C5SI型号，设备通过智能芯片硬件来支持) |
| 105 | support\_human\_service | 是否支持人形检测能力 0-不支持, 1-支持 (设备+平台服务开通，实现人形检测服务能力设备通过更新软件版本可以支持) |
| 106 | support\_ap\_mode | 是否支持添加设备配置WiFi使用，0：不支持，1：smartconfig+声波失败后，支持AP配网，2：设备默认AP配网 |
| 107 | support\_continuous\_cloud | 是否支持连续云存储 0-不支持, 1-支持,注:与support\_cloud(序号11)完全无关 |
| 108 | support\_doorbell\_sound | 是否支持门铃声音 0-不支持, 1-支持 |
| 109 | support\_associate\_detector | 是否支持关联探测器 0-不支持, 1-支持 |
| 110 | support\_modify\_username | 是否支持修改门锁用户备注名称 0-不支持, 1-支持 |
| 111 | support\_transfertype | 预览取流格式传输类型：0-tcp，1-udp，默认0表示tcp |
| 112 | support\_vertical\_panoramic | 是否支持垂直全景(与support\_horizontal\_panoramic(序号96)对应) 0-不支持, 1-支持 |
| 113 | support\_alarm\_light | 是否支持安防灯 0-不支持, 1-支持 |
| 114 | support\_alarm\_area | 是否支持安防灯 0-不支持, 1-支持 |
| 115 | support\_chime | 是否支持门铃扩展 0-不支持, 1-支持 |
| 116 | support\_video\_mode | 是否支持support\_video\_mode 0-不支持, 1-支持 |
| 117 | support\_relation\_camera | 是否支持W2D 关联摄像机功能 0-不支持, 1-支持 |
| 118 | support\_pir\_setting | 是否支持PIR(红外)区域设置 0-不支持, 1-支持 |
| 119 | support\_battery\_manage | 是否支持电量管理 0-不支持, 1-支持 |
| 508 | support\_smart\_app | 支持设置页面智能应用 0-不支持,1-固定c6设备跳转,2-动态智能应用 |