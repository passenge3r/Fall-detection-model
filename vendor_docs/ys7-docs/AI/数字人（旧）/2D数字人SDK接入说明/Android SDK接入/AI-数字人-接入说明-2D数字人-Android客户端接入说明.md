# AI-数字人-接入说明-2D数字人-Android客户端接入说明

> AI-数字人-接入说明-2D数字人-Android客户端接入说明

> 更新时间: 2026-05-25T16:37:53.000+08:00

> 文档ID: 2420 | 来源树: AI

---

# Android客户端接入说明

### 一. 准备工作

#### 1.1 账号注册

进入萤石云开放平台<https://open.ys7.com/cn/s/index> , 进行账号注册 ;

#### 1.2 获取AccessToken

1. 进入萤石开放平台->控制台->基础服务->账号中心->应用信息->获取AppKey、Secret；

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086096744_image.png)

2. 点击“通过接口获取”，进入<https://open.ys7.com/help/19>，根据接口获取AccessToken；

#### 1.3 创建数字人项目

1. 进入萤石开放平台->控制台->产品中心->AI服务->数字人->会话互动

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086252086_image_1.png)

2. 获取appId

![imagepng](https://appres.ys7.com/AppYs-SmartCustomerService/1718086261769_image_2.png)

3. 购买2d互动数字人并发,获取uid(请联系产品经理开通对应的并发)

### 二.如何接入

#### 2.1 集成环境

1. 接入语言: Kotlin/JAVA
2. 库名称: ezviz-dh-release.aar
3. 环境准备:支持 Android minsdk 28
4. 开发环境: Android Studio 2.6及以上
5. NDK支持架构: armeabi-v7a, arm64-v8a

#### 2.2 接入说明

1. 以提供的aar包的形式进行集成:

将**ezviz-dh-release.aar**包放入主工程的libs目录下，然后在主工程的build.gradle 文件中加入如下代码：

```
dependencies {
 //...
 //依赖 ezviz-dh-release.aar
 implementation files('libs/ezviz-dh-release.aar')

 //用于网络请求,原项目已依赖的话,可忽略
 implementation 'com.squareup.retrofit2:retrofit:2.9.0'
 implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
}
```

2. 权限配置

SDK的使用过程需要进行联网及网络信息操作,请在清单文件中配置如下权限:

```
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.INTERNET" />
```

#### 2.3 使用说明

注: 数字人控件相关方法请在主线程调用;

1. 创建数字人显示控件:

```
//创建数字人控件(参数1:上下文)
//(数字人控件也可以通过xml创建) 
//注:如需重启数字人,请先调用EzDigitalHumanPlayer的stop()方法停止数字人,
//移除老的ezDigitalHumanPlayer,再重新创建新的ezDigitalHumanPlayer并初始化,add进布局即可;
val ezDigitalHumanPlayer = EzDigitalHumanPlayer(context)
//如果是代码创建数字人控件,需将其进当前页面的布局中
//ez_dh_container.addView(ezDigitalHumanPlayer)
```

2. 设置数字人初始化配置:

通过**EzDigitalHumanPlayer**的**setInitConfig**方法设置**EzDhInitConfig**对象, **EzDhInitConfig**必须要设置如下两个参数:

| 参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| appId | string | 是 | 在萤石开放平台,创建2d数字人项目时获取; |
| accessToken | string | 是 | 根据萤石开放平台申请的appKey和secret通过接口获取accessToken;**注:** accessToken具有**时效性**,时效7天,请保证在有效期内使用\*\*[需自行获取和维护]\*\*; |
| uid | string | 是 | 在萤石开放平台的2d数字人项目中购买并发数后,会获得对应的uid;**注:** 同一个uid对应一路并发,无法同时多处使用; |

```
ezDigitalHumanPlayer.setInitConfig(EzDhInitConfig().apply {
     this.appId = mAppId
     this.accessToken= mAccessToken
     this.uid = mUid
 })
```

3. 设置数字人事件回调

```
//设置数字人播放器事件回调
     ezDhPlayer.setEzDhPlayerEventCallback(object : EzDhPlayerEventCallback {
         /**
          * 数字人启动播放成功
          * 在数字人启动后,通过该回调通知接入方启动成功(可以做隐藏loading等操作)
          */
         override fun onDhStartSucceed() {
             super.onDhStartSucceed()
             //do something
         }

         /**
          * 数字人启动播放失败
          */
         override fun onDhStartFailed(code: Int, msg: String) {
             super.onDhStartFailed(code, msg)
             /**
              * code:错误码
              * msg:错误信息
              * 建议:关闭页面,结束数字人,处理对应错误
              * */
         }

         /**
          * 数字人播放错误
          */
         override fun onError(code: Int, msg: String, isNeedFinish: Boolean) {
             super.onError(code, msg, isNeedFinish)
             /**
              * code:错误码
              * msg:错误信息
              * isNeedFinish:是否需要关闭页面,结束数字人
              *  -true:表示该错误需要关闭页面,结束数字人
              *  -false:表示该错误不影响数字人主流程运行
              * 建议:isNeedFinish=true时,关闭页面,结束数字人,检查失败原因
              * (请勿直接重启数字人,建议检查错误原因后再重启数字人,防止失败原因未处理,导致无限循环重启;)
              * (注:若业务需要重启数字人,也请自行控制重启次数,防止error未处理导致无限重启!)
              */
         }
     })
```

4. 启动数字人

上述配置请在启动数字人之前调用

```
//启动数字人
ezDigitalHumanPlayer.start()
```

5. 发送文本驱动消息

注:需要数字人启动成功后调用
注: 发送文本间隔必须大于1s , 字符串最长4000字节, 文本不可以是纯符号的无意义字符; (文本驱动失败,onError会返回对应错误)

```
//入参:msg为需要驱动数字人说话的字符串
ezDigitalHumanPlayer.sendTextMsg(msg)
```

6. 打断当前数字人播报

在数字人播报过程中,调用此方法可以进行打断

```
ezDigitalHumanPlayer.interrupt()
```

7. 结束数字人

```
//结束数字人(请确保在页面退出时调用停止方法,确保资源释放)
//注:结束数字人后,如需重新使用,需要重新创建数字人控件,进行配置后进行开启
ezDigitalHumanPlayer.stop()
```

8. 更新accessToken

在数字人sdk运行过程中，有可能会出现网络波动导致重连操作，需要accessToken进行验证，所以**需要数字人sdk使用过程中，accessToken均需在有效期内**（在长时间使用数字人sdk过程中，accessToken有可能会过期，通过萤石开放平台接口获取accessToken时，会一同返回过期时间）；
**在accessToken到期前，如果数字人sdk在运行中，需要通过该方法，进行对accessToken进行更新；**

```
//更新accessToken(请保证accessToke正确且在有效期内使,否则数字人将无法正常工作)
ezDigitalHumanPlayer.refreshAccessToken(mAccessToken)
```

9. 设置debug日志文件

是否支持存储debug日志文件，默认关闭(注：仅调试使用，线上版本请不要开启！)
参数1：是否开启（默认关闭）
参数2：日志文件存储路径（非必要参数，参数1为true时，需要传入）

```
//自定义日志存储文件夹
var logPath = ""//例：this.getExternalFilesDir("ezdh")?.absolutePath

//是否支持存储debug日志文件，默认关闭(注：仅调试使用，线上版本请不要开启！请使用APP自有日志逻辑进行日志管理,便于问题排查)
//如需使用，请在EzDigitalHumanPlayer创建前，进行开启

//开启
//EzDigitalHumanBase.enableDebugLogToFile(true, logPath)

//关闭
EzDigitalHumanBase.enableDebugLogToFile(false)
```

10. 详细见Demo

#### 2.4 错误码

注: 接入方在遇到Error,需要重新初始化Player时,建议控制重新初始化Player的次数,防止出现长时间错误引起循环启动;

1. onDhStartFailed错误码

| code | 含义 | 措施 |
| --- | --- | --- |
| 4002 | 未在主线程执行 | 修改代码 |
| 4003 | 必要的配置信息不完整 | 修改代码 |
| 4004 | 代码异常 | 提供日志向我们反馈 |
| 4005 | 数字人已经启动 | 无需处理 |
| 4007 | 无法连接服务,请检查网络后重试 | 检查网络 |
| 4008 | 连接服务超时 | 退出数字人,可重新创建player重启 |
| 4400 | 入参错误 | 退出数字人,请检查appId及uid是否正确 |
| 4412 | 用户无可用会话数或会话数超过最大限制 | 退出数字人,检查可用并发数 |
| 5020 | 服务异常 | 退出数字人,提供日志向我们反馈 |
| 5021 | 创建会话失败(服务异常导致) | 退出数字人,提供日志向我们反馈 |
| 5022 | 创建会话失败(会话被关闭) | 退出数字人,可重新创建player重启 |
| 5023 | 创建会话失败(建流失败) | 退出数字人,可重新创建player重启 |
| 5024 | 创建会话失败(状态异常) | 退出数字人,提供日志向我们反馈 |

2. onError错误码

| code | 含义 | 措施 |
| --- | --- | --- |
| 310002 | token过期或异常 | 退出数字人,修改代码,定期刷新token |
| 310003 | 数字人播放超时 | 退出数字人,检查网络等异常项 |
| 310004 | 设备会话被占用 | 退出数字人,检查可用并发数 |
| 310005 | 文本指令发送过快(间隔大于1秒) | 修改代码,按照要求发送文本 |
| 310006 | 文本指令字符串超出最长4000字节 | 修改代码,按照要求发送文本 |
| 310007 | 不支持该文本指令文本播报 | 修改代码,按照要求发送文本 |
| 100012 | 触发文本限流 | 修改代码,按照要求发送文本 |
| 110013 | 会话已关闭 | 退出数字人 |
| 110014 | 数字人会话未就绪 | 退出数字人 |
| 110015 | 当前状态不允许输入文本 | 修改代码,按照要求发送文本 |
| 110018 | 会话不存在 | 退出数字人 |
| 100001 | 文本参数错误 | 修改代码,按照要求发送文本 |
| 100014 | 并发配额不足 | 退出数字人,检查可用并发数 |
| 100015 | 数智人形象已过期 | 退出数字人,检查过期 |
| 400000 | 系统错误 | 提供日志向我们反馈 |
| <0 | 系统错误 | 提供日志向我们反馈 |

#### 2.5 注意事项

1. 请勿设置 android:hardwareAccelerated="false"，关闭硬件加速之后，可能会导致视频流无法渲染;
2. sdk需要kotlin环境,请自行添加kotlin支持;
3. sdk需要AndroidX环境,请开启AndroidX后使用
4. 接入方需要自行获取及维护萤石云开放平台获取的AccessToken,确保数字人使用期间AccessToken均处于有效状态;

#### 2.6 示例Demo使用

需要在**com.ezviz.ezdhdemo.MainActivity.kt**文件中,自行添加获取**appId, uid**和**accessToken**,相关逻辑;