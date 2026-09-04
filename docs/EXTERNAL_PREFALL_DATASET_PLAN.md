# 跌倒预测外部数据集筛选与接入方案

更新日期：2026-08-14

## 结论

第一优先级选用 **Pre-VFall** 补充“跌倒早期征兆”训练；第二优先级使用 **OmniFall/UP-Fall** 的统一时间段标注做跨受试者和跨数据域验证。URFD、Le2i、MCFD等可继续用于普通跌倒检测或外部测试，但不作为早期风险预测的主训练集。

## 1. Pre-VFall：主要新增训练集

- 任务匹配度：高。数据集专门面向跌倒前异常征兆，而不仅是已经发生的跌倒。
- 规模：约22,000张筛选图像、原始视频与派生特征，约19.65GB。
- 人员：9名受试者。
- 视角：RGB相机45度和90度视角，包含前视和侧视。
- 类别：正常、异常、跌倒；异常包含虚弱、眩晕、谵妄混乱和正常压力脑积水式混乱。
- 跌倒方向：包含向前和侧向跌倒。
- 许可：CC BY 4.0。
- 局限：仍为健康年轻人模拟，不等同于真实老人；论文的三类标签需要进一步转成连续风险阶段和跌倒起点标注。

计划映射：

| 原始场景 | 本项目阶段 |
|---|---|
| normal | safe |
| confusion_delirium / confusion_nph | abnormal_long_term |
| dizzy_* / weakness_*中跌倒前片段 | prefall_far / prefall_mid / prefall_near |
| falling | falling |
| fallen | fallen |

不能把完整的 `dizzy_fall_*` 或 `weakness_fall_*` 视频直接整体标成预测阳性，必须先标注跌倒动作起始时刻，再生成严格截止于起始时刻之前的窗口。

## 2. OmniFall：统一标注与泛化测试框架

OmniFall统一了8个实验室跌倒数据集，并提供跨受试者、跨视角和跨域划分。公开统计包括约2,164段实验室视频、9,590个单视角时间段和13.81小时内容；其中UP-Fall有17名受试者、两个相机视角和较长连续序列。标签包含 `walk/fall/fallen/sit_down/sitting/lie_down/lying/stand_up/standing/other` 等类别，适合系统性加入容易误报的正常动作。

用途：

- 用 `fall` 时间段的开始时刻作为候选跌倒起点；
- 从起点前1/2/3秒生成预测窗口；
- 将 `sit_down`、`lie_down`、`kneel_down`、`squat_down` 等作为难负样本；
- 按官方跨受试者划分训练和验证；
- 使用OOPS-Fall或其他数据源做跨域外部测试。

注意：OmniFall的统一标注采用CC BY-NC 4.0，但原视频版权仍属于各原始数据集，视频必须从允许的官方来源取得。

## 3. 其他候选数据集

| 数据集 | 适用性 | 决定 |
|---|---|---|
| UR Fall Detection | 30段跌倒、40段ADL，RGB/深度/加速度同步，提供falling临时状态 | 适合作为小型外部测试，不足以解决跨人训练 |
| KFall | 32人、21类ADL、15类跌倒，具有跌倒起点和冲击时刻 | 非常适合预冲击研究，但主要是穿戴式IMU，不作为摄像头主模型训练集 |
| UNN-6 | RGB/红外，6类动作，视频仅约41MB | 可做快速兼容性测试，但只有36段RGB视频 |
| OmniFall OF-Syn | 12,000段合成视频，含年龄、视角、体型等元数据 | 可用于预训练或压力测试，不替代真实/实验视频测试 |

## 4. 数据划分和防泄漏规则

1. 同一受试者、同一试次的不同相机视角必须属于同一数据折。
2. 同一原始视频切出的所有窗口必须属于同一数据折。
3. 预测窗口的最后一帧必须早于标注的跌倒动作起点。
4. 测试集不得参与阈值选择、温度缩放或样本筛选。
5. 同时报告数据集内、跨受试者和跨数据集三组结果。
6. 主指标使用事件召回、平均提前量和误报事件/小时；窗口级PR-AUC仅作为辅助指标。

## 5. 建议实验顺序

1. 下载Pre-VFall元数据并核对文件结构，先选取1名受试者的小样本验证读取、RTMPose提取和时间标注。
2. 完成9名受试者的跌倒起点标注或复核，形成统一manifest。
3. 只用Pre-VFall训练，按受试者留一验证。
4. GMDCSA24与Pre-VFall联合训练，但测试仍保持数据集独立。
5. 用OmniFall中的坐下、躺下、跪下、下蹲等动作做难负样本测试。
6. 数据闸门通过后，再比较ST-GCN++有序阶段、时间到跌倒回归以及骨架+RGB双流模型。

## 6. 下载工具

新增脚本 `scripts/download_external_prefall_data.py`：

```powershell
# 仅生成来源清单，不下载大文件
.venv\Scripts\python.exe scripts\download_external_prefall_data.py omnifall-labels

# 下载OmniFall的小型标注文件
.venv\Scripts\python.exe scripts\download_external_prefall_data.py omnifall-labels --download

# 查询Pre-VFall的Figshare文件清单
.venv\Scripts\python.exe scripts\download_external_prefall_data.py prevfall

# 确认文件清单后再选择性下载；支持断点续传和容量上限
.venv\Scripts\python.exe scripts\download_external_prefall_data.py prevfall --download --include "*video*" --max-gb 20
```

标注下载后先执行预测资格审计，统计真正具有1/2/3秒跌倒前上下文的事件数：

```powershell
.venv\Scripts\python.exe scripts\audit_omnifall_prefall_eligibility.py `
  data\external\omnifall_labels\up_fall.csv `
  data\external\omnifall_labels\cmdfall.csv `
  --output data\external\omnifall_labels\prefall_eligibility.json
```
