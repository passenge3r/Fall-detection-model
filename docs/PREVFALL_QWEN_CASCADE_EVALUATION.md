# PreVFall 骨架预警 + Qwen3-VL 级联评估

更新日期：2026-08-25

## 1. 评估目的

验证Qwen3-VL应该在跌倒发生前负责预测，还是在骨架模型预警后负责视频复核。

基础触发器为PreVFall 9名受试者严格LOSO的RTMPose + ST-GCN++ 2秒预警模型。每个跌倒视频取其第一个位于真实2秒时距内的OOF触发窗口；每个非跌倒视频取第一个OOF误触发窗口。该协议得到70个真实事件触发、15个非跌倒误触发，另外2个跌倒视频未被骨架模型触发。

注意：这是“第二阶段确认器”评估，不是完整连续在线仿真。跌倒视频窗口的选取使用真实时距标签，且没有计入同一视频更早的误触发 episode，因此结果不能替代后续摄像头长时运行测试。

## 2. 两种Qwen时序窗口

### 因果即时复核

只使用触发时刻之前4秒RGB画面，不允许看到未来视频。

结果：70个骨架真实触发中，Qwen只确认1个；15个误触发均未确认。作为严格AND确认器时：

| 指标 | 结果 |
|---|---:|
| Accuracy | 34.26% |
| Precision | 100.00% |
| Recall | 1.39% |
| Specificity | 100.00% |
| F1 | 2.74% |
| Balanced Accuracy | 50.69% |

结论：通用Qwen3-VL无法仅凭跌倒前画面稳定预测未来2秒事件，不能否决骨架预警。

### 触发后延迟2.5秒复核

骨架模型立即给出预警，系统继续缓存2.5秒，再让Qwen分析覆盖触发前后约4.5秒的RGB片段。

结果：70个骨架真实触发中确认61个；15个误触发全部未确认。把Qwen确认作为“升级确认”时，在全部108视频上的指标为：

| 指标 | 骨架2秒预警 | Qwen延迟确认 |
|---|---:|---:|
| TP / TN / FP / FN | 70 / 21 / 15 / 2 | 61 / 36 / 0 / 11 |
| Accuracy | 84.26% | 89.81% |
| Precision | 82.35% | 100.00% |
| Recall | 97.22% | 84.72% |
| Specificity | 58.33% | 100.00% |
| F1 | 89.17% | 91.73% |
| Balanced Accuracy | 77.78% | 92.36% |

Qwen在骨架真实触发上的确认率为87.14%，在骨架误触发上的错误确认率为0%。

## 3. 延迟

85段延迟复核：

- 平均4.90秒/片段
- 中位数4.54秒/片段
- 最快2.90秒
- 最慢16.16秒（包含冷启动影响）

因此Qwen不适合阻塞实时预警，但适合在后台生成第二阶段确认和事件解释。

## 4. 正确的系统决策

```text
骨架达到HIGH（1秒时距）
→ 立即显示提前预警（不等待Qwen）
→ 继续缓存2.5秒RGB视频
→ Qwen异步复核
   ├─ 确认falling/prefall/postfall：升级为多模态确认事件
   ├─ 未确认：标记“骨架单路冲突”，交人工复核
   └─ 推理失败：保持原骨架告警，不中断服务
```

安全融合不允许Qwen撤销骨架预警；Qwen的100%精确率只适合作为当前数据上的升级确认结果，不能直接外推到真实家庭环境。

## 5. 最终推荐：1秒HIGH触发 + 延迟2.5秒

进一步的线上端到端检查发现，2秒MEDIUM可能在真正跌倒前较早出现，提前调度Qwen会只看到正常站立。为贴近在线运行，正式配置改成仅由1秒 `HIGH` 或已经确认跌倒触发Qwen。

严格LOSO触发清单包括69个真实高风险触发、7个非跌倒误触发，另有3个跌倒视频未被骨架1秒分支触发。延迟2.5秒复核后，Qwen确认68/69个真实触发，并拒绝7/7个误触发：

| 指标 | 骨架1秒HIGH | Qwen升级确认 |
|---|---:|---:|
| TP / TN / FP / FN | 69 / 29 / 7 / 3 | 68 / 36 / 0 / 4 |
| Accuracy | 90.74% | 96.30% |
| Precision | 90.79% | 100.00% |
| Recall | 95.83% | 94.44% |
| Specificity | 80.56% | 100.00% |
| F1 | 93.24% | 97.14% |
| Balanced Accuracy | 88.19% | 97.22% |

Qwen在骨架真实触发上的确认率为98.55%，误触发错误确认率为0%。平均推理4.71秒，中位数4.54秒。

## 6. 文件

- 即时复核结果：`results/prevfall_qwen_cascade_2s/predictions.csv`
- 即时复核汇总：`results/prevfall_qwen_cascade_2s/predictions.summary.json`
- 延迟复核结果：`results/prevfall_qwen_cascade_2s_delayed25/predictions.csv`
- 延迟复核汇总：`results/prevfall_qwen_cascade_2s_delayed25/predictions.summary.json`
- 触发清单：`data/metadata/prevfall_qwen_oof_triggers_2s_delayed25.csv`
- 推荐1秒路线结果：`results/prevfall_qwen_cascade_1s_delayed25/predictions.csv`
- 推荐1秒路线汇总：`results/prevfall_qwen_cascade_1s_delayed25/predictions.summary.json`
- 推荐1秒触发清单：`data/metadata/prevfall_qwen_oof_triggers_1s_delayed25.csv`
