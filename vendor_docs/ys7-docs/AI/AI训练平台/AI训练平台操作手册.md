# AI训练平台操作手册

> AI训练平台操作手册

> 更新时间: 2026-07-02T17:21:44.000+08:00

> 文档ID: 4521 | 来源树: AI

---

**硬件适配说明：当前通过本AI训练平台训练生成的算法模型，仅支持C6C-dev设备安装部署。**

# 1.进入页面

## 1.1进入萤石开放平台网页，点击右上角控制台选项

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3WCAF9WvAAlIQPiMBZ0051.png)

## 1.2在控制台左侧选择AI服务，进入AI训练平台

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3WmAWoaiAAKtRJKMBDM276.png)

# 2.AI训练平台页面介绍

## 2.1算法仓库

### 2.1.1选择行业类型

行业类型包含工商企业，智慧监管，智慧建筑，智慧商贸，智慧农业等行业。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3WuAFgodAAtPE7WIZ3w118.png)

### 2.1.2选择算法类型

算法类型包含混合监测模型，物体监测模型，图像单标签分类。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3W2AS_L6AAuMzexr5vQ724.png)

## 2.2数据管理

### 2.2.1数据集

#### 2.2.1.1创建训练集

点击右上角选择创建训练集。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3W6Ae2yVAAHLHick4hA558.png)

在创建训练数据集时，需要填写数据集名称；选择算法类型（混合监测模型，物体监测模型，图像单标签分类）；标注方式（目前四边形标注还未开发）；版本备注。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3XCAMCGJAACpFYv4z9k212.png)

#### 2.2.1.2创建测试集

点击右上角选择创建测试集。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3XOAGCJBAAF_xghQZms427.png)

在创建测试数据集时，填写内容和步骤和上述创建训练测试集保持一致。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3XWAPjPCAACe4ZgHJRY671.png)

#### 2.2.1.3发布训练数据集版本

在创建完数据集后，需要针对数据集进行版本发布。点击右侧全部版本的选项（该操作适用于第一次创建数据集然后发布版本，如果是对已发布的数据集更新可以点击右侧的创建新版本）

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3XiAZKWlAAG1K2Vxxzw860.png)

在数据集全部版本页面中，可以看出显示版本未发布并且未达到训练标注。需要在右侧先点击数据导入按钮。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3XqAI3eIAAG4mmnm46E149.png)

在数据导入中选择图片上传或文件夹上传两种方式，并注意上传的说明条件。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3X2AJvhWAAIG6dPJXGc116.png)

在完成图片上传后要对图片进行标注，点击右侧的标注图片

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3X-AeLyAAApYTve6Fc0652.png)

在进入数据集图片标注页面后点击右侧的新建检测对象标签。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3YKAT1XcAA-dgJsOKWY105.png)

其中需要填写数据集中对象名称和属性，属性为检测对象属性（如安全帽检测填写的属性值如下图所示）

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3YSAEOirAAJ1E4fUl_w193.png)

标注操作：选择属性值矩形工具双击屏幕选择框选起点松开鼠标选择框选终点框选完毕。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3YeASC9UAA9ItDBPis0888.png)

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3YmANvO-AA-Yz8Wv4T0885.png)

在完成数据集的图片标注后，就可以发布当前版本，点击发布按钮就可以在后续模型管理使用中使用到这个数据集。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3YyAKgXuAAKxb_iIiKs924.png)

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3Y6AZHrVAALKW5N6d3g468.png)

后续需要更新该数据集里面的内容时，可以在全部版本页面点击创建新版本页面，选择继承已有版本和创建全新版本。

![](https://resource.eziot.com/group1/M00/01/90/CtwQEmii3ZCAU-DCAAIootUe7Sw196.png)

数据集右侧的编辑选项，可以修改数据集名称。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3ZOAJDg_AAGuCoW2CJ4914.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3ZWAM5GTAAHMExw8_ko278.png)

数据集右侧的删除选项，可以删除该数据集。

![](https://resource.eziot.com/group1/M00/01/90/CtwQE2ii3ZiACouOAAGwgBIgDrI392.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3ZuANGo2AAHbLTaXP88317.png)

#### 2.2.1.4发布测试数据集版本

在数据集全部版本页面中，可以看出显示版本未发布并且未达到训练标注。需要在右侧先点击数据导入按钮。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3Z2ACSZkAAHB31J_-sQ633.png)

在数据导入中选择图片上传或文件夹上传两种方式，并注意上传的说明条件。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3Z-AMClkAAILPWyHivA198.png)

在完成图片上传后要对图片进行标注，点击右侧的标注图片

在进入数据集图片标注页面后点击右侧的新建检测对象标签。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3aGAexHGAAiBupr6CvQ488.png)

其中需要填写数据集中对象名称和属性，属性为检测对象属性（如安全帽检测填写的属性值如下图所示）

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3bCAMhFvAAGJe_n5ejY182.png)

标注操作：选择属性值矩形工具双击屏幕选择框选起点松开鼠标选择框选终点框选完毕。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3aqAa5GwAA7yOEiZlgg738.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3ayAUAxlAA8AHvJkxHU997.png)

数据集右侧的编辑选项，可以修改数据集名称。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3bCAMhFvAAGJe_n5ejY182.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3bWAPn7GAAG2eDW9je4110.png)

数据集右侧的删除选项，可以删除该数据集。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3biAP91TAAGFKNZlytE602.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3bqAdnbjAAHFezP9dA0827.png)

### 2.2.2在线标注

针对已经发布的数据集，可以在左侧的在线标注的页面对该数据集进行在线标注。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3b2AQz79AAUJ3cttnuw313.png)

## 2.3模型管理

### 2.3.1我的模型

#### 2.3.1.1创建模型

处理完模型使用的数据集后，在模型管理我的模型里点击创建模型，输入模型名称和选择的模型算法（目前算法支持只有列表里面的算法，其它算法后续会陆续上新）。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3cGASGBVAAKb2r1ul2o265.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3cOAAjuLAABtFBSFIDA955.png)

#### 2.3.1.2训练模型

创建完的模型我们需要点击该模型的全部版本，进入全部版本页面后点击立即训练（该操作针对新建的没有经过训练的模型，已经有版本的模型直接点击训练新模型选项）。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3cmAE3KqAALS_2k9WvU068.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3cuABgmMAAI5oJkGuEs701.png)

在创建新模型中，需要填写14个步骤，其中云部署的应用类型后续会陆续上新。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3c2ASYwFAAMtXJ1Pusw147.png)

其中第三步选择训练数据集，需要确定训练数据集和版本号，以及检测对象的标签类型。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3c-AHpHIAAKPHv-4xG4165.png)

#### 2.3.1.3测试模型

在训练完模型后，可以在我的模型全部版本中看到已经训练完的版本，点击测试按钮。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3dGAHPKWAAOI_GcfjAA007.png)

在创建模型测试页面，选择该模型的测试数据集。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3dOAO_jJAAOR88YdGpI524.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3daANWcDAAMzOLl-eYQ425.png)

#### 2.3.1.4查看模型版本详情

针对已经训练并测试完的模板版本，同样也可以在我的模型全部版本页面中点击查看详情，查看该模型版本的具体信息。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3diALE_IAAOJNMyZdiM205.png)

进入版本详情页面，可以看到该版本的相关信息。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3dqAW_KWAAUITlj37CA973.png)

在评估报告页面中可以看到物体检测评估报告和图像分类评估报告，可以查看出目前模型的模型分析详情。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3dyAcHV5AAL0XGn-lI0512.png)

### 2.3.2模型训练

在模型训练页面，可以针对已经创建的模型创建模型训练。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3d6AemfNAAPkFP68Csg987.png)

在模型训练主页面中，可以通过筛选训练状态，训练数据集来查看自己的模型信息。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3eCAP-wZAAPYG2afnOw876.png)

### 2.3.3模型测试

在模型测试页面，可以针对已经训练完成的模型创建模型测试。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3eaAYy1wAAPiHwaEPp8767.png)

在模型测试主页面，可以针对已经测试完成的模型查看测试报告。

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3eiAOZV9AAKq1KyPxYM857.png)

## 2.4安装模型

在安装模型的页面，可以针对适配的设备型号进行模型安装，将训练测试完成的模型应用到该设备的日常使用场景中。

![](https://resource.eziot.com/group1/M00/01/91/CtwQE2ii3eqABry_AAG934ZVJ5c056.png)

![](https://resource.eziot.com/group1/M00/01/91/CtwQEmii3euAYVG3AABCMTCDzIc746.png)