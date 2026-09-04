# 萤石开放平台 Java SDK

> 萤石开放平台 Java SDK

> 更新时间: 2026-05-25T16:44:40.000+08:00

> 文档ID: 4334 | 来源树: SDK及示例

---

## 概述

开发者云服务和开发者终端请求萤石开放平台资源都需要携带安全令牌。安全令牌是保证请求合法性和数据安全性的一种凭证。通过安全令牌，开发者也能确保其在开放平台上的操作合规、安全，并且能够对平台资源进行正常、有效的访问和使用。

## Java SDK 下载链接

可以直接从公共仓里集成，或者[点击下载](https://izhstatic.ys7.com/vasp-openweb/1776948503671_ezviz-openplatform-1.2.7.RELEASE.jar)，若公共仓版本低于下载地址版本，建议使用下载。

公共仓库Maven依赖

```
<dependency>
  <groupId>com.ezviz.open</groupId>
  <artifactId>ezviz-openplatform</artifactId>
  <version>1.1.6.RELEASE</version>
</dependency>
```

## 开发者指南

### Q: 要怎么使用SDK来颁发Token

A: 请使用com.ezviz.open.sdk.auth.token.TokenGenerator的子类，这些子类都支持接口方法 generateToken。每个接口和其参数的具体含义，请参阅SDK的Java doc文档。

### Q: 目前有哪几类Tokengenerator，有什么用？

A:

| 类名 | 说明 | 用途 |
| --- | --- | --- |
| com.ezviz.open.sdk.auth.token.nondevice.NonDeviceOpsTokenGenerator | 非设备类操作授权Token | 可以访问开放平台网关 |
| com.ezviz.open.sdk.auth.token.device.DeviceGeneralTokenGenerator | 设备操作类的授权Token | 可以访问开放平台网关，需要指定DeviceSerial，ChannelNo等参数后进行授权 |
| com.ezviz.open.sdk.auth.token.stream.StreamTokenGenerator | 取流操作Token | 取流Token，用于进行私有流取流。不能用于访问开放平台网关 |
| com.ezviz.open.sdk.auth.token.resource.GeneralResourceTokenGenerator | 资源访问Token （RTC中的通话token） | 用于访问资源服务器 |

### Q: 如何成为在颁发票据的时候贯彻安全原则

A: 为什么Token的颁发者要注意颁发Token的安全？因为任何终端，只要获得了票据后，就可以凭票据访问萤石开放平台的资源。这些资源被使用往往会有以下限制——

- 产生流量的操作会被计费
- 可能造成使用萤石开放平台的存储资源计费
- 可能造成网关接口访问次数被统计或因超出频率而被限流。

因为Token的颁发行为，本质上是开发者将自己的操作权限授权给Token的获得者，因此相关的费用和其他访问后果将由Token的颁发者负责。

为此，Token颁发者需要根据自己的业务特点，并且按照【权限最小原则】进行授权。**由于SecretKey保管不善而造成的信息泄漏，或者由于Token权限过大（有效期过长）造成的安全隐患，应由Token签发者自行负责。**

萤石开放平台设计中考虑了较多安全机制，来帮助Token颁发者限制颁发的Token的使用范围。萤石对开发者在颁发Token时的安全建议如下——

- 设置尽可能小的Token有效时间。如果Token马上就会被接收方使用，你可以控制Token过期时间仅为10秒钟。10秒之后Token会自动失效，这将大大增加攻击者利用的难度。
- 在Token中写入授权设备的特征码、设备序列号等操作参数，当终端持有Token在萤石云进行验证时，这些参数会被检查与Token中的是否一致。
- 针对开放平台网关操作，设置Token参数的UrlPattern属性，限定Token持有者仅可能凭借Token访问符合该模式的URL。
- 针对支持一次性操作的Token，设置useOnceOnly属性为true，指定该Token在萤石云上只能使用一次。
- 针对开放平台网关操作，设置Token参数的自定义属性（setAttribute），在访问网关时也会校验这部分参数。

总之，这些措施的目的都是为了更精确的秒数Token持有者在访问萤石云平台时的行为，确保Token颁发后不会被滥用。

## SDK描述

### com.ezviz.open.sdk.auth.token.nondevice.NonDeviceOpsTokenGenerator#generateToken(NonDeviceOpsParams params)

| 字段 | 类型 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| appid | String | 描述SaaS服务授权本次操作产生的流量费用被计入哪个应用（项目），该参数为预留参数，目前没有实际应用，可以填空字符串 | true |
| userId | String | 使用该业务功能的身份标识，该参数为预留参数，目前没有实际应用，可以填空字符串 | true |
| expire | int | 过期时间，相对于time(Token颁发时间)， expire秒后过期 | true |
| attributes | Map | 自定义属性 | false |
| time | long | SaaS服务可以不设置该字段，生成Token的时候会自动根据当前时间计算 | false |
| urlPattern | String | 该字段限制了终端可访问萤石开放平台API的范围。当终端访问萤石云时，会检查被访问，可以传/\*\* | false |

### com.ezviz.open.sdk.auth.token.device.DeviceGeneralTokenGenerator#generateToken(DeviceGeneralParams params)

| 字段 | 类型 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| appid | String | 描述SaaS服务授权本次操作产生的流量费用被计入哪个应用（项目），该参数为预留参数，目前没有实际应用，可以填appkey | true |
| deviceSerial | String | 本票据访问萤石云平台时，萤石会检查实际操作的设备是否与此处指定的设备序列号一致。 如果不一致，该取流视为未被授权。当然，前提条件是AppKey拥有者的帐号必须具备此该设备的权限。 | true |
| channelNo | String | 通道号 | false |
| resourceCatagory | String | 资源类型，包括video和global。如果不是OTAP设备标识，保留为空即可，如果是OTAP设备标识，一般为'video' | false |
| expire | int | 过期时间，相对于time(Token颁发时间)， expire秒后过期。 | true |
| action | String | 操作类型，可以传\* | true |
| time | long | SaaS服务可以不设置该字段，生成Token的时候会自动根据当前时间计算 | false |
| terminalIP | String | 终端IP地址。SaaS服务检测到本次操作的终端IP地址。 | false |
| useOnceOnly | boolean | 在有效期内，该Token是否可以反复使用。 | false |
| urlPattern | String | 该字段限制了终端可访问萤石开放平台API的范围。当终端访问萤石云时，会检查被访问 | true |

### com.ezviz.open.sdk.auth.token.stream.StreamTokenGenerator#generateToken(StreamParamsparams params)

| 字段 | 类型 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| appid | String | 描述SaaS服务授权本次操作产生的流量费用被计入哪个应用（项目），该参数为预留参数，目前没有实际应用，可以填appkey | true |
| deviceSerial | String | 本票据访问萤石云平台时，萤石会检查实际操作的设备是否与此处指定的设备序列号一致。 如果不一致，该取流视为未被授权。当然，前提条件是AppKey拥有者的帐号必须具备此该设备的权限。 | true |
| channelNo | String | 通道号。 注意：当actionType参数为TALK时，IPC设备对讲channelNo传0 | true |
| resourceCatagory | String | 资源类型，包括video和global。如果不是OTAP设备取流，保留为空即可，如果是OTAP设备标识，一般为'video' | false |
| expire | int | 过期时间，相对于time(Token颁发时间)， expire秒后过期。 业务方必须在过期之前开始取流。过期后无法取流。 | true |
| expire2 | String | 持续播放过期时间，视频可播放的最晚时间。从颁发Token时间开始，expire2秒以后过期 业务方取流成功后，会对播放中的通道定时检查，如果发现超过expire2规定的期限，那么播放将失效。 默认90天。 | false |
| actionType | StreamType | 操作类型，包括PREVIEW、PLAYBACK、TALK | false |
| time | long | SaaS服务可以不设置该字段，生成Token的时候会自动根据当前时间计算 | false |
| terminalIP | String | 终端IP地址。SaaS服务检测到本次操作的终端IP地址。 | false |
| useOnceOnly | boolean | 在有效期内，该Token是否可以反复使用。 | false |

### com.ezviz.open.sdk.auth.token.resource.GeneralResourceTokenGenerator#generateToken(GeneralResourceTokenParam params)

| 字段 | 类型 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| appid | String | 描述SaaS服务授权本次操作产生的流量费用被计入哪个应用（项目），该参数为预留参数，目前没有实际应用，可以填appkey | true |
| expire | int | 过期时间，相对于time(Token颁发时间)， expire秒后过期。 业务方必须在过期之前开始取流。过期后无法取流。 | true |
| time | long | SaaS服务可以不设置该字段，生成Token的时候会自动根据当前时间计算 | false |
| policy | List | 限定了一组行为能力，例如：定义一个包含了允许获取RTC地址行为、允许终端入会行为的策略。策略需关联资源，形成完整的资源访问。行为是指最小服务能力的定义，例如RTC地址行为，终端入会行为，指令下发行为等，具体行为定义，由业务方实现。 | true |

## 示例

### E1: 颁发非设备类小权限token：用于访问开放平台网关，授权可访问的非设备类资源API URL

可以在代码中设置UrlPattern，来限制Token持有者访问网关的API接口

```
NonDeviceOpsTokenGenerator generator = new NonDeviceOpsTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

NonDeviceOpsParams params = new NonDeviceOpsParams();
params.setAppid("");
params.setUserId("");
params.setExpire(3600);
params.setUrlPattern("/v3/conference/**");
String token = generator.generateToken(params);
//上述代码生成了一个Token，持有者可以在1小时（3600秒）内，访问/v3/conference/ 开头的所有API。
//其中**可以匹配任意层级的任意URL。
```

URLPattern的使用规则如下

- `?` 可以匹配任意单个字符。（不含目录分隔符 `/`）
- `*` 可以匹配任意0到n个字符。（不含目录分隔符 `/`）
- `**`  可以匹配任意层级的目录和字母。

Token颁发者可以通过限制请求中的关键参数。以防止Token使用者越权操作。

```
NonDeviceOpsTokenGenerator generator = new NonDeviceOpsTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

NonDeviceOpsParams params = new NonDeviceOpsParams();
params.setAppid("");
params.setUserId("");
params.setExpire(3600);
params.setUrlPattern("/v3/conference/**");

//指定访问开放平台API时，以下两个HTTP参数必须为指定的值。
//注意参数名（roomid、pairid）必须和实际请求开放平台时的HTTP query参数完全一致，包括大小写。
params.setAttribute("roomid", "room001");
params.setAttribute("pairid", "pair001");
			
String token = generator.generateToken(params);
```

### E2：颁发设备类小权限token：用于访问开放平台网关，授权可操作的设备资源

对于设备操作，Token颁发者应该将操作范围限定在一个设备上或一个通道上。

```
DeviceGeneralTokenGenerator generator = new DeviceGeneralTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

param = new DeviceGeneralParams();
// 设备序列号
param.setDeviceSerial("D12356643");
param.setChannelNo("1");

//设定该Token只能被以下终端使用
param.setTerminalIP("172.56.22.134");
//设置该Token只能调用抓图接口
params.setUrlPattern("/api/lapp/device/capture");
// 指定该取流Token可以使用多次，如果设置为true，代表该token仅可使用一次
param.setUseOnceOnly(false);
// 设定有效时间
param.setExpire(60);
String token = generator.generateToken(param);
//上述代码指定生成了一个Token，该Token需要在60秒内使用，可以对某个特定通道执行抓图操作
```

### E3: 颁发取流小权限token：用于在萤石SDK中进行私有流取流

取流授权中，您需要指定取流的设备序列号和通道号，从而防止持有人利用该Token去访问其他设备。

```
StreamTokenGenerator generator = new StreamTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

StreamParams params = new StreamParams();
// 是预览还是回放
params.setActionType(StreamType.PREVIEW);
// 设备序列号
params.setDeviceSerial("D12356643");
params.setChannelNo("1");
// 取流过期时间，15分钟
params.setExpire(900);
// 取流后用户播放有效期，7天。注意接收参数是Int，不要超过
params.setExpire2((int) TimeUnit.HOURS.toSeconds(8));

// 设置取流终端的IP
params.setTerminalIP("172.56.22.134");
// 指定该取流Token可以使用多次，如果设置为true，代表该取流token仅可使用一次
params.setUseOnceOnly(false);
String token = generator.generateToken(params);
System.out.println(token);
```

### E4: 颁发RTC 通话Token（资源访问Token）

```
GeneralResourceTokenGenerator generator = new GeneralResourceTokenGenerator();
generator.init(APP_KEY, SECRET_KEY);

GeneralResourceTokenParam param = new GeneralResourceTokenParam();
// 创建一个action，不同业务的action参数不同，这里以终端入会业务为例。
Action action= new Action("ERTC_INFO");
//设置业务参数：strRoomId
action.setAttribute("strRoomId", "ID1699430483");
//设置业务参数：customId
action.setAttribute("customId", "7ca19da6c7164bc5ad7e0a");
//RTC场景下，可以使用本token控制终端在会议中的权限。1(0b0001)：可发送音频流；2(0b0010)：可发送视频流；4(0b0100)：可发起屏幕共享。同时授予三个权限，将三个权限对应编码相加。1+2+4=7。
action.setAttribute("permission", "7");
param.addAction(action);
// 设置appid
param.setAppid("f758a146b2b24fc7b9705e232bce9f02");
// 设置过期时间，最长过期时间为604800秒（7天）
param.setExpire(604800);
String token = generator.generateToken(param);
```

## FAQ

- Q: 生成Token的用处是什么？意味着什么？

  A: Token的中文含义是票据。它就象是一张高铁车票（非常类似）——在售票处，铁路公司在验明你的身份证，并且收到你的钱之后，颁发给你这样一个【凭证】，你可以持有这个【凭证】乘坐对应车次的高铁。
  在我们业务中，SaaS业务方可以在验明终端用户的身份和权限后，颁发一个票据（Token），作为该终端后续可以访问萤石云平台资源的凭证。因此一个Token（票据），意味着SaaS业务方将自己访问萤石云平台的权限，（临时性地）授予了某个终端（或三方）。

  上一句话中，“SaaS业务自己访问萤石云平台的权限”，意味着这次授予，无法超过SaaS业务方自身访问萤石云平台的权限范围。
  “临时性地”，表示授予的权限是存在有效期的，并且这个有效期不会很长。
- Q: Token的实际用法是怎么样的？

  A： 在我们的设想中，终端（PC、移动端、设备端）向SaaS服务（云眸/云耀/融合云、三方开发者）发起申请，告知SaaS服务自己要在萤石云上做一个什么操作。SaaS服务需要检查这次操作是否符合终端的身份权限，在检查后，颁发Token对终端进行授权。
  终端凭借Token(票据)来萤石云进行操作，萤石会检查——

  - Token（票据）是否伪造的。
  - Token（票据）是否过期了。
  - 这个Token来自哪个开发者（SaaS服务）
  - 这个Token授权的行为，是否与终端本次申请的操作的行为一致。（例如：终端不能拿着一个授权其操作设备A的票据，到萤石云平台来操作设备B）。
  - 颁发Token（票据）的开发者，是否具有执行此项操作的权限。

  上述检查都通过后，萤石云按终端本次的要求进行动作。
- Q：Token是如何防止伪造的？

  A: Token是SaaS服务颁发权限的凭证，就像一张动车票一样，有很多限制。终端在获得Token(票据)后，有可能试图修改和伪造Token来萤石云操作。如果这种行为能够得逞，那么整套机制也就没有存在的价值了。因此Token必须有防伪机制，在铁路系统中，这一行为由负责检票的检票员（现在是检票机）进行。

  - 一个开发者不能仿冒其他开发者生成Token
  - 终端要操作的行为和目标，如果发生了变化，能被检票方察觉。

  采用的方法是Token中会包含大量与本次操作相关信息—— 操作参数、操作目标、Token颁发者的AppKey这些都会被记录Token中。由于Token算法是公开的，因此防伪的任务被交付给现代密码学的研究成果。
  我们采用HMACSHA256算法，对操作参数进行摘要并计算出签名。
  为了防止开发者A冒充另一个开发者生成签名，签名使用开发者的Secret Key进行加密，因此每个开发者都必须保护好自己的Secret Key。**不要把Secret Key存储或传输到不安全的地方——比如移动端、网页代码中。** 由于生成Token需要传入SecretKey，**Token应当只在开发者的服务端程序生成。**
- Q： 如果给终端颁发了一个Token，然后有后悔了，能撤除吗？

  A: Token是基于加密运算来验证的，因此目前萤石云平台不提供撤回Token的功能。如果出现安全问题，您可以更换您的Appkey和SecretKey。要注意：更换后，开发者之前所有颁发的Token将全部失效。各个终端需要重新向SaaS服务申请新的Token才能访问萤石云。

## Release Note

v 1.0.16.RELEASE

- 修复StreamTokenGenerator编解码器参数完整性。

v 1.2.7.RELEASE

- 修复取流类小权限token解析兼容问题。