# Lucia 论文蓝图

最后更新：2026-03-10  
目标：UIST 风格长文  
主要目标：将当前“SDK + 两个案例研究”的稿件，重构为一篇围绕共享 session 抽象与 plug-in 架构展开的统一系统论文。

## 1. 论文核心论点

整篇论文应该清晰地论证一件事：

**Lucia 是一个以 session 为中心的可穿戴 AI 原型系统，它通过共享的执行与日志流水线降低工程开发摩擦，并支持多种应用类别。**

这意味着论文**不应该**按以下方式组织：

- SDK 描述
- 案例研究 1
- 案例研究 2

而应该按以下方式组织：

- 问题背景与系统主张
- 系统架构
- 证明该系统能够改进开发流程并支持多种 plug-in 的证据

## 2. 核心 Claims

全文统一使用以下三个 claim：

1. **统一系统 claim**  
   Lucia 提供了一个以 session 为中心的可穿戴 AI 原型架构，具备共享的连接、流传输、路由和日志接口。
2. **开发效率 claim**  
   相比碎片化的基线工作流，Lucia 能显著降低原型开发摩擦。
3. **广泛适用且边界清晰的 claim**  
   Lucia 同时支持 egocentric video-QA 和度量感知两类 plug-in，并且能够清楚地揭示其优势与失败边界。

## 3. 最佳论文结构

## 标题

推荐方向：

**Lucia: A Session-Centered Wearable AI Prototyping System for Egocentric Video QA and Metric Perception**

更短的可选版本：

**Lucia: A Wearable AI Prototyping System with Shared Session Abstractions and Plug-in Modules**

## 摘要

使用 [01_manuscript_restructure.md](/Users/wf24018/home/LUCI/uist_upgrade/01_manuscript_restructure.md) 中的摘要草稿，等新增实验完成后，再修改最后两句。

## 1. 引言

### 目的

建立研究缺口、系统主张和论文贡献。

### 保留原论文中的内容

- 原文中关于可穿戴设备与 egocentric AI 快速发展的动机。
- 原文中“当前可穿戴 AI 软件基础设施仍然碎片化”的论点。
- 原文中“缺少统一 SDK 来支持实时数据采集、流传输与上层 AI 集成”的问题意识。

### 需要新增的内容

- 将 Lucia 重构为**系统贡献**，而不只是设备 SDK。
- 在引言早期引入 session abstraction。
- 明确写出三个 claim 与 RQ1-RQ3。
- 增加一个短段落，说明 video QA 和 measurement 只是构建在同一系统接口上的两个代表性 plug-in。

### 本节内容安排

第 1 段：

- 可穿戴 AI 正在快速增长
- egocentric 数据具有重要价值
- 当前开发工作流高度碎片化

第 2 段：

- 现有工作往往分别强调设备、模型或应用
- 目前缺少一种可复用的原型系统，能够把设备接入、应用执行与可复现分析统一起来

第 3 段：

- 引出 Lucia 作为解决方案
- 用一句话概括以 session 为中心的系统架构

第 4 段：

- 精确写出三项贡献

第 5 段：

- 引出 RQ1-RQ3
- 简要预告 A/B/C 三组评估

### 本节输出

- 一个主系统图的预告引用
- 贡献列表
- 研究问题

## 2. 相关工作

### 目的

将 Lucia 放在现有可穿戴 AI 系统、egocentric 推理流水线、stereo/depth 流水线和开发工具评估论文的语境中定位。

### 保留原论文中的内容

- 原有的 wearable computing 背景。
- 原有的 egocentric AI 和 LLM 辅助感知相关背景。
- 原有的 stereo/depth 与 object measurement 相关参考文献。

### 需要新增的内容

- 增加一个关于**toolkits 与 prototyping infrastructure**的小节。
- 增加一个关于**developer-facing evaluation**的小节。
- 改写比较逻辑，使 Lucia 被定位为**系统层贡献**，而不是单一应用 demo。

### 本节内容安排

2.1 Wearable 与 egocentric AI 系统

- smart glasses
- wearable cameras
- first-person assistants

2.2 面向 egocentric video 的导航推理

- ST-Think 类模型
- video-language reasoning

2.3 面向度量感知的 stereo/depth 融合

- SGBM
- monocular depth
- fused pipelines
- measurement systems

2.4 Toolkits、SDKs 与面向开发者的系统评估

- Lucia 的差异点：共享 session object、可复现协议、跨 plug-in 的统一执行路径

### 本节输出

- 一个收束段，明确指出研究缺口：  
  现有工作很少从“统一的 wearable AI prototyping layer”角度，同时用系统证据和开发者证据进行评估。

## 3. 系统总览

### 目的

让系统设计成为整篇论文的中心。

### 保留原论文中的内容

- ADB connection workflow
- wireless bridge configuration
- RTSP streaming 支持
- stereo synchronization 支持
- 那些为解释整条流水线所必须保留的 device access 细节

### 需要新增的内容

- 将 **session object** 引入为核心抽象。
- 引入面向下游应用的 **plug-in interface**。
- 引入 **logging and replay contract**。
- 增加 failure taxonomy 与 reproducibility 的论证。

### 本节内容安排

3.1 流水线概览

- User Trigger -> Lucia SDK -> Session Object -> Plug-in Module -> Output -> Logging/Replay

3.2 设备接入与传输层

- USB/ADB 支持
- wireless bridging
- RTSP streaming
- synchronization pathway

3.3 Session 抽象

- session 中包含什么：
  frames/clips、timestamps、device mode、sync metadata、prompt/query、config hash、module version
- 为什么这是核心贡献：
  所有应用共享同一套输入/输出/日志契约

3.4 Plug-in 接口

- video-QA plug-in（corridor-navigation 作为一个 benchmark task）
- measurement plug-in
- 未来 plug-in 也可复用同一封装

3.5 Logging、replay 与 failure taxonomy

- 引入 [03_session_log_schema.json](/Users/wf24018/home/LUCI/uist_upgrade/03_session_log_schema.json) 中的 schema
- 解释为什么可复现性对于 wearable AI systems 论文至关重要

### 本节输出

- **Main Figure 1**：完整系统流水线
- **Table 1**：session schema 概览

## 4. 原始内容映射

这一节**不应出现在最终论文里**。它只用于写作准备阶段。

### 必须保留的原始材料

1. Device/SDK 能力

- ADB connection
- file access and transfer
- network setup
- wireless bridging
- RTSP streaming

2. Video-QA plug-in 材料

- ST-Think integration
- route question setup
- retrospective 与 prospective navigation queries
- path correctness、direction-change correctness、followability 等指标
- 原文中关于“短程感知较强、长时程推理较弱”的观察

3. Measurement plug-in 材料

- dual-Lucia stereo rig
- monocular 与 stereo calibration
- SGBM 与 monocular depth fusion
- LLM-guided object detection/segmentation
- object size estimation
- 现有 calibration 统计结果

### 值得保留的已有结果

以下数值是从 PDF 中部分恢复出来的，在正式复用前必须对照原稿手工核对：

- monocular reprojection error：约 `0.210` pixels
- stereo reprojection error：约 `0.247` pixels
- epipolar alignment error：约 `0.188` pixels
- stereo baseline：约 `70.06 mm`
- navigation 类别级结果显示：视觉类问题更强，long-horizon reasoning 更弱

## 4. 评估

这一整节应该成为修订后论文的中心部分。

### 4.0 评估总览

### 目的

让读者明确看到：整篇评估是按照 claim 来组织，而不是按照 demo 顺序组织。

### 需要新增的内容

- 增加一个总括段：  
  “We evaluate Lucia through three evidence blocks corresponding to system quality, developer efficiency, and application breadth.”

### 本节输出

- 一个指向 A/B/C 三个 package 的路线图句子

## 4.1 Package A：平台基准测试（RQ1）

### 目的

证明 Lucia 在系统层执行与稳定性方面带来改善。

### 保留原论文中的内容

- 任何已有的 connectivity 和 streaming 实现细节，只要这些内容有助于解释 benchmark 的对象

### 需要新增的内容

- 基线对比
- setup friction tasks
- 弱网络与长时运行条件
- p50/p95 报告方式

### 本节内容安排

4.1.1 条件设置

- baseline workflow vs Lucia workflow
- USB vs Wi-Fi
- normal vs weak/lossy network
- short vs long duration

4.1.2 任务与指标

- discover/connect
- time-to-first-frame
- record clip
- export clip
- latency、fps、drops、reconnects、failures

4.1.3 结果

- 报告量化改进或性能权衡
- 展示 Wi-Fi 条件下降级或 reconnect 成本升高的位置

4.1.4 Takeaway 与 boundary

- 用一句话总结与 Claim 1 对应的结论
- 用一句话明确写出局限

### 本节输出

- **Figure A1**：setup friction 对比
- **Figure A2**：runtime stability / latency
- **Table A1**：平台指标汇总

## 4.2 Package B：开发者生产力试验（RQ2）

### 目的

证明 Lucia 是一个真正有价值的开发系统，而不仅仅是技术集成层。

### 保留原论文中的内容

- 无，这一部分基本是新增

### 需要新增的内容

- internal within-subject developer study
- completion time、errors、help requests、LOC/config effort、SUS、NASA-TLX

### 本节内容安排

4.2.1 参与者与研究设计

- 8 名内部参与者
- within-subject
- counterbalanced order

4.2.2 任务

- connect and stream
- record and export
- minimal navigation prototype
- minimal measurement prototype

4.2.3 测量项

- objective
- subjective
- qualitative

4.2.4 结果

- paired plots
- effect sizes
- workload / usability summary

4.2.5 Takeaway 与 boundary

- Lucia 降低了开发摩擦
- 局限：内部试验、样本较小

### 本节输出

- **Figure B1**：time / errors / effort 总结
- **Table B1**：SUS / TLX 与 paired statistics

## 4.3 Package C：Plug-in 评估与消融（RQ3）

### 目的

通过两种不同应用类别，在同一 session 接口下展示系统的广泛适用性与边界。

### 保留原论文中的内容

- 当前全部 navigation evaluation 内容
- 当前全部 measurement evaluation 内容
- 所有仍然有效的现有图表与结果

### 需要新增的内容

- 明确将二者重命名为 plug-ins
- 将二者统一到同一个 session / logging pipeline 下
- 增加 ablation 与条件分层分析

## 4.3.1 Plug-in A：Navigation Reasoning

### 保留原论文中的内容

- ST-Think integration
- route QA 设计
- retrospective / prospective tasks
- path correctness、direction-change accuracy、followability
- 当前已有的定性失败观察

### 需要新增的内容

- anchor ablation：
  no anchor、minimal anchor、structured anchor
- route complexity stratification
- hallucinated landmark rate
- latency breakdown

### 本节内容安排

1. Task and dataset setup
2. Baselines and variants
3. Metrics
4. Quantitative results
5. Failure analysis
6. Takeaway and boundary

### 本节输出

- **Figure C1**：video-QA ablation 图
- **Table C1**：按 route complexity 分层的 video-QA 指标

## 4.3.2 Plug-in B：Metric Perception and Measurement

### 保留原论文中的内容

- stereo rig 设计
- calibration procedure
- intrinsic / extrinsic calibration 结果
- SGBM plus monocular depth fusion
- object size measurement pipeline

### 需要新增的内容

- ablation：
  SGBM only、monocular only、fusion
- 按 object type、material、distance、lighting 进行 grouped errors 分析
- 映射到 failure taxonomy

### 本节内容安排

1. Calibration and geometric setup
2. Depth pipeline variants
3. Measurement task definition
4. Quantitative results
5. Condition-wise grouping
6. Takeaway and boundary

### 本节输出

- **Figure C2**：depth-fusion ablation
- **Figure C3**：grouped size-estimation errors
- **Table C2**：calibration 与 measurement 汇总

## 5. 讨论

### 目的

以 systems paper 的方式解释结果，而不是把它写成两个独立应用论文的拼接。

### 保留原论文中的内容

- 当前已有的 limitations 与 future directions

### 需要新增的内容

- 一个关于 Lucia 实际带来了什么的新小节
- 一个关于系统边界的新小节
- 一个关于 reproducibility 以及 logging contract 意义的新小节
- 一个标题明确的小节：
  **Why this is not only integration**

### 本节内容安排

5.1 Lucia 超越“应用拼装”的地方

- shared session object
- unified routing / logging
- reusable developer workflow

5.2 边界条件

- weak-network instability
- long-horizon navigation failures
- reflective / textureless measurement failures
- limited human-study scale

5.3 Reproducibility

- session logs
- artifacts
- regenerable figures / tables

5.4 Future directions

- 更多 plug-ins
- 更大规模的研究
- 更广泛的设备支持

## 6. 结论

### 目的

重新概括系统贡献与证据结构。

### 本节内容安排

- 一句话说明问题
- 一句话说明 Lucia 的解决方案
- 一句话说明 A/B/C 三类证据
- 一句话说明 reproducibility 与未来价值

## 7. 新增内容清单

以下内容并不属于原始论文，必须在升级版论文中明确写出来：

1. 与系统故事一致的新摘要
2. 精确的三条 contribution framing
3. RQ1-RQ3
4. Session abstraction 小节
5. Plug-in interface 小节
6. Unified session logging and replay 小节
7. Claim-evidence matrix 表格
8. Package A benchmark 小节
9. Package B developer pilot 小节
10. Navigation anchor ablation 小节
11. Measurement depth-fusion ablation 小节
12. Failure taxonomy 小节
13. “Why this is not only integration” 讨论段

## 8. 图表规划

建议目标图表如下：

1. Figure 1：Lucia 端到端系统流水线
2. Table 1：session schema 概览
3. Figure A1：setup friction 对比
4. Figure A2：runtime latency / stability
5. Table A1：平台 benchmark 指标
6. Figure B1：developer study 总结
7. Table B1：developer study 的 paired statistics
8. Figure C1：video-QA ablation
9. Table C1：video-QA 指标与边界案例
10. Figure C2：depth fusion ablation
11. Figure C3：grouped size-estimation errors
12. Table C2：calibration 与 measurement 总结
13. Table X：claim-evidence matrix
14. Figure X：failure taxonomy 与 case cards

## 9. 写作规则

起草时遵循以下规则：

1. 每一节都必须回答：这里的 systems contribution 是什么？
2. 每一个 evaluation subsection 结尾都必须有：
   - 一句 claim-level takeaway
   - 一句 limitation / boundary
3. 除非某些 API 细节直接支撑 claim，否则不要在正文中展开太多底层接口细节。
4. 尽量复用所有有效的原始结果，但必须重写其 framing，使其服务于统一的系统故事。
5. 从当前 PDF 往新稿转移内容时，在草稿中做如下标记：
   - `[ORIGINAL]`：来自当前稿件的复用内容
   - `[NEW]`：为升级版论文新增的内容

## 10. 起草顺序

建议按以下顺序写：

1. 引言
2. 系统总览
3. 相关工作
4. 先写 Plug-in A 和 Plug-in B，并尽量复用当前已有原始结果
5. 讨论
6. 等有了新数据之后，再补写 Package A 和 Package B
7. 最后再修改摘要和结论

## 11. 配套使用文件

写作时请与以下文件一起使用：

1. [01_manuscript_restructure.md](/Users/wf24018/home/LUCI/uist_upgrade/01_manuscript_restructure.md)
2. [02_claim_evidence_matrix.md](/Users/wf24018/home/LUCI/uist_upgrade/02_claim_evidence_matrix.md)
3. [03_session_log_schema.json](/Users/wf24018/home/LUCI/uist_upgrade/03_session_log_schema.json)
4. [04_package_a_platform_benchmark.md](/Users/wf24018/home/LUCI/uist_upgrade/04_package_a_platform_benchmark.md)
5. [05_package_b_developer_pilot.md](/Users/wf24018/home/LUCI/uist_upgrade/05_package_b_developer_pilot.md)
6. [06_package_c_plugin_ablations.md](/Users/wf24018/home/LUCI/uist_upgrade/06_package_c_plugin_ablations.md)
