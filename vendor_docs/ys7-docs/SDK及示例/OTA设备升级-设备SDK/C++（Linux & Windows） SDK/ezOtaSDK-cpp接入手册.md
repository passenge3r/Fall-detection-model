# ezOtaSDK-cpp接入手册

> ezOtaSDK-cpp接入手册

> 更新时间: 2026-05-25T16:44:41.000+08:00

> 文档ID: 1866 | 来源树: SDK及示例

---

# 1.概述

ezOtaSDK 是设备接入萤石云平台的一个重要的工具套件，该套件提供以下能力：

| 功能点 | 描述 |
| --- | --- |
| 设备认证、安全 |  |
| 设备查包 |  |
| 可升级固件包下载 |  |
| 下载/升级进度上报 |  |

# 2.名词解释

| 名词 | 含义/作用 | 获取方式 |
| --- | --- | --- |
| productKey | 产品ID，萤石开放平台中产品的唯一标识。在业务中用于唯一标识产品信息。在SDK集成等中均需应用。 | 开放平台OTA控制台-产品获取详情可见[《快速入门》-3.1产品管理](https://open.ys7.com/help/1715)。 |
| deviceLicense | 产品密钥，确认产品使用权限，在SDK集成等中均需应用。 | 开放平台OTA控制台-产品获取详情可见[《快速入门》-3.1产品管理](https://open.ys7.com/help/1715)。 |
| deviceName | 设备序列号，设备实际的序列号。由您定义。需要保证产品下唯一，不可重复。 | 由您定义，可提前导入萤石OTA控制台，便于管理。详情可见[《快速入门》-3.1产品管理](https://open.ys7.com/help/1715)。 |
| deviceId | 设备ID，设备注册并激活后平台颁发的唯一ID。萤石开放平台中设备唯一标识。 | SDK在第一次注册激活成功或向平台获取并回调给设备保存，设备拿到后必须固话保证不丢失。后续可在萤石开放平台OTA控制台-设备列表中获取。详情可见[《快速入门》-3.1产品管理](https://open.ys7.com/help/1715)。 |
| dasHttpPort | 升级接入服务端口号，默认https为443端口 |  |
| dasHttpHost | 升级接入服务域名 | http:dev.ys7.com |
| deviceMac | 设备网卡的MAC地址 |  |

# 3.OTA产品接入流程

1. 在OTA控制台中创建产品信息，并获取productKey与deviceLicense（即产品ID与产品密钥）——详见[《使用指南》](https://open.ys7.com/help/1715)3.1.1创建产品（产品线）
2. 在控制台中创建产品模块。——详见[《使用指南》](https://open.ys7.com/help/1715)3.4.1添加模块
3. 在控制台中导入设备信息。——详见[《使用指南》](https://open.ys7.com/help/1715)3.3.1导入设备
4. ezOtaSDK设备接入。——详见本文档
5. 上传升级包、下发升级任务。激活设备后升级——详见详见[《使用指南》](https://open.ys7.com/help/1715)3.5、3.6内容

## 3.1ezOtaSDK设备接入流程

![](http://resource.eziot.com/group2/M00/00/B6/CtwQFmUk-TuARExaAAEZ3X9apaQ357.png)

# 4.ezOtaSDK库文件依赖关系

## 4.1库文件列表：

libota.a(.so)：OTA升级模块

libcomm.a(.so)：公共组件模块，日志、json、http、https

libezos.a(.so)：系统抽象接口，用于兼容linux、windows、rt-thread、freeRTOS等系统

libmbedtls.a(.so)：SSL加密模块，对于使用HTTPS可选择使用mbedtls或者openssl

## 4.2头文件列表

ezOtaSDK.h：SDK接口头文件

ezOtaSDK\_error.h：SDK错误码描述

## 4.3库文件依赖关系

![](http://resource.eziot.com/group2/M00/00/B6/CtwQF2Uk-j6AHmN4AABfbZ7RlE4423.png)

## 4.4SDK目录结构

- doc——接入文档
- example——参考demo
- - cpp\_example——cpp测试demo
- - jni\_example——jni测试demo
- inc——头文件
- lib——库文件

# 5.设备接口调用流程

## 5.1SDK初始化流程

初始化前先设置日志级别，每次启动只需初始化一次即可

- c接口：OTA\_API int ezOtaSDK\_init(ezOtaSDK\_init\_info\_t \*info);
- return 0 - 成功,other-失败\ref ezOtaSDK\_errcode\_e

![](http://resource.eziot.com/group2/M00/00/B6/CtwQF2UlBt-AJgzrAAFIOsne98Q527.png)

## 5.2查升级包流程

查包间隔建议在5分钟以上每次

查包前确保SDK已经初始化

- c接口：OTA\_API int ezOtaSDK\_query\_package(ezOtaSDK\_modules\_t \*modules, ezOtaSDK\_firmwarePackageList\_t \*packageList);
- \retval 0 - 成功
- \retval ota\_errcode\_no\_package-没有查到有部署固件包

![](http://resource.eziot.com/group2/M00/00/B6/CtwQFmUlBymAJxrhAAGgZBmUA5s949.png)

## 5.3下载固件包流程

必须在有查到可升级包的情况下才可以调用下载接口，否则调用无效

下载升级

- c接口：OTA\_API int ezOtaSDK\_download\_package(ezOtaSDK\_upgradePackage\_info\_t \*upInfo);
- return 0 - 成功,other-失败\ref ezOtaSDK\_errcode\_e
  ![](http://resource.eziot.com/group2/M00/00/B6/CtwQF2UlB52APpgTAAC321qgij0501.png)

# 6.SDK错误码说明

见ezOtaSDK\_error.h文件

# 7.SDK接口说明(参考demo为testota.cpp)

## 7.1设置SDK日志级别

```
/** 
*  \brief    初始化日志接口并设置日志级别，在SDK初始化前设置
*  \method     ezOtaSDK_set_log_level
*  \param[in]     log_level 日志级别ezOtaSDK_logLevel_e
*  \param[in]  log_path 非必须，日志文件保存路径，默认在可执行文件目录下
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_set_log_level(int log_level, const char *log_path);
```

表7.1-1 ezOtaSDK\_set\_log\_level接口定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | log\_level | 设置日志级别 | 必须 |
| const char \* | log\_path | 设置日志文件保存路径 | 非必须 |

## 7.2SDK初始化接口

```
/** 
*  \brief      SDK初始化 
*  \method     ezOtaSDK_init
*  \param[in]     info:初始化信息
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_init(ezOtaSDK_init_info_t *info);
```

表7.2-1 ezOtaSDK\_init接口定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| ezOtaSDK\_init\_info\_t | info | 初始化信息结构体 | 必须 |

表7.2-2 ezOtaSDK\_init\_info\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | byFile | 0：configInfo为ezOtaSDK\_config\_info\_t结构体,1：configInfo为文件路径 | 必须 |
| ezOtaSDK\_getDeviceId\_cb | getDevid\_cb | 获取deviceId回调函数 | 必须 |
| ezOtaSDK\_setDeviceId\_cb | setDevid\_cb | 设置deviceId回调函数 | 必须 |
| void \* | configInfo | byFile=0：configInfo为ezOtaSDK\_config\_info\_t结构体byFile=1：configInfo为文件路径 | 必须 |
| void \* | userData | 用户指针 | 非必须 |

表7.2-3 ezOtaSDK\_ config\_info \_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| unsigned short | dasHttpPort | 平台端口 | 必须 |
| char[] | dasHttpHost | 平台域名 | 必须 |
| char[] | deviceMac | 设备网卡的MAC地址 | 必须 |
| char[] | devVersion | 设备固件版本号 | 必须 |
| ezOtaSDK\_license\_info\_t | productLicense | 产品license信息，与控制台产品信息中的“产品密钥”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.1产品管理 | 必须 |

表7.2-4 ezOtaSDK\_license\_info\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| char[] | productKey | 产品ID，萤石开放平台中产品的唯一标识。在业务中用于唯一标识产品信息。在SDK集成等中均需应用。开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 | 必须 |
| char[] | deviceName | 设备序列号，设备实际的序列号。由您定义。需要保证产品下唯一，不可重复。由您定义，可提前导入萤石OTA控制台，便于管理。详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.3设备管理 | 必须 |
| char[] | deviceLicense | 产品密钥，确认产品使用权限，在SDK集成等中均需应用。开放平台OTA控制台-产品获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.1产品管理。 | 必须 |

## 7.3SDK反初始化接口

```
/** 
*  \brief      SDK反初始化 
*  \method     ezOtaSDK_fini
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_fini();
```

## 7.4SDK查包接口

```
/** 
*  \brief      查询升级接口    
*  \method     ezOtaSDK_query_package
*  \param[in]     modules:模块信息
*  \param[out]    packageList：查到的可升级包列表
*  \return     成功返回0，失败返回非0
*  \retval     0 - 成功
*  \retval     ota_errcode_no_package-没有查到有部署固件包
*  \retval     非0 - 失败，\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_query_package(ezOtaSDK_modules_t *modules, ezOtaSDK_firmwarePackageList_t *packageList);
```

表7.4-1 ezOtaSDK\_modules\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | num | 查询的模块数量，支持多模块升级例如：1个应用表示一个模块，子系统也属于一个模块 | 必须 |
| ezOtaSDK\_module\_t \*[] | moduleList | 模块的信息列表 | 必须 |

表7.4-2 ezOtaSDK\_module\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | supportDiff | 是否支持差分升级 | 必须 |
| char [] | mod\_name | 设备型号/模块名称模块ID，获取详情可见[《使用指南》](https://open.ys7.com/help/1715)-3.4模块管理。 | 必须 |
| char [] | fw\_ver | 设备/模块当前的版本号，格式必须为V1.0.0 build 220427格式 | 必须 |

表7.4-3 ezOtaSDK\_firmwarePackageList\_t定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | num | 查询到的可升级模块数量 |
| ezOtaSDK\_firmwarePackageInfo\_t \*[] | PackageInfo | 查询到的可升级包信息 |

表7.4-4 ezOtaSDK\_firmwarePackageInfo\_t定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | fileType | 固件包类型，0：整包；1：差分包与控制台上传包时的“升级包类型”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| char [] | filesize | 升级包文件大小 |
| char [] | mod\_name | 模块名称/型号模块ID，与控制台上传包时的“所属OTA模块”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| char [] | fw\_ver | 模块最新的固件版本号, 格式为:V1.1.0 build 220427格式与控制台上传包时的“升级包版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| char [] | fw\_ver\_dst | 与控制台上传包时的“待升级版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| char \*\* | filepath | 升级包文件路径 |
| char [] | digest | 升级包MD5签名，用于校验与控制台上传包时的“Md5”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| char [] | dsc | 升级包描述，例如：本次升级迭代了xxxxx内容，解决了xxxxxBUG与控制台上传包时的“升级包描述”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 |
| ezOtaSDK\_upgrade\_conditions\_t | conditions | 升级条件 |

表7.4-5 ezOtaSDK\_upgrade\_conditions\_t定义

| 参数类型 | 参数名称 | 说明 |
| --- | --- | --- |
| int | silent\_upgrade | 升级方式：0-触发升级,1-静默升级 |
| int | battery\_limit | 升级时和下载固件包时最低电量要求：限制百分比:0-100,0表示不限制 |
| int | network\_limit | 固件包下载网络要求 0-不限制,1-非流量模式可以下载（非4G/5G模式可下载） |
| char [] | startTime | 允许/建议下载和升级的开始时间00:00（小时：分钟） |
| char [] | endTime | 允许/建议下载和升级的开始时间00:00（小时：分钟） |

## 7.5SDK开始下载固件包接口

```
/** 
*  \brief      开始下载固件包
*  \method     ezOtaSDK_start_download
*  \param[in]     dwInfo:需要下载的固件包信息
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_start_download(ezOtaSDK_download_info_t *dwInfo);
```

表7.5-1 ezOtaSDK\_download\_info\_t定义

| 参数类型 | 参数名称 | 说明 | 是否必须 |
| --- | --- | --- | --- |
| int | byfile | OTA文件临时存储方式1：SDK自己写文件，0：SDK回调给设备保存 | 必须 |
| int | fileType | 固件包类型，0：整包；1：差分包与控制台上传包时的“升级包类型”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| char[] | mod\_name | 模块名称/型号模块ID，与控制台上传包时的“所属OTA模块”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| char[] | fw\_ver | 需要下载的固件版本号, 格式为:V1.1.0 build 220427格式与控制台上传包时的“升级包版本号”值相同，详见[《接入指南》](https://open.ys7.com/help/1715)3.5.1添加升级包 | 必须 |
| char[] | fw\_ver\_dst | 如果为差分包需要输入当前模块的固件版本号与控制台上传包时的“待升级版本号”值相同，详见《接入指南》3.5.1添加升级包 | 必须 |
| ezOtaSDK\_dwFile\_cb | dwFile\_cb | 固件包下载流回调，byfile=1时必须实现 | 必须 |
| ezOtaSDK\_dwStatus\_cb | dwStatus\_cb | 固件包下载状态、进度回调函数 | 必须 |
| ezOtaSDK\_dwStatus\_cb | dwStatus\_cb | 固件包下载状态、进度回调函数 | 必须 |
| char \* | dirpath | byfile=1时必须设置，ota文件临时存放目录路径，目录后面不要带/ | 非必须 |
| void \* | userData | 用户指针 | 非必须 |
| ezOtaSDK\_dwFile\_cb | dwFile\_cb | 必须 |  |

## 7.6SDK停止下载固件包接口

```
/** 
*  \brief      停止下载固件包
*  \method     ezOtaSDK_stop_download
*  \param[in]     mod_name 模块名称/模块型号/固件识别码
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_stop_download(const char* mod_name);
```

## 7.7SDK上报升级结果接口

```
/** 
*  \brief    上报升级结果
*  \method     ezOtaSDK_report_upgrade_result
*  \param[in]     errCode,0-升级成功，其他-升级失败错误码，失败错误码使用ezDevSDK_error.h文件内的ezOtaSDK_upgrade_errcode_e
*  \return     0-成功,other-失败\ref ezOtaSDK_errcode_e
*/
OTA_API int ezOtaSDK_report_upgrade_result(ezOtaSDK_module_t *module, int errCode);
```

# 8. 参考用例

见cpp\_example/testota.cpp