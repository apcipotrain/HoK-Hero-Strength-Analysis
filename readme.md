![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Build](https://img.shields.io/badge/Status-Practice%20Project-orange.svg)
![Award](https://img.shields.io/badge/Target-MCM%20S%20Award-red.svg)

# 基于蒙特卡洛模拟与贝叶斯平滑算法的王者荣耀英雄强度评估

# (Game Hero Strength Evaluation Based on Monte Carlo Simulation and Bayesian Smoothing)

## 📌 项目概述

本项目针对《王者荣耀》2025-2026 赛季，通过抓取职业联赛（KPL）与巅峰赛（Peak Data）的多维数据，构建了一套量化平衡性评估体系。

**核心解决问题：**

1. **基准设定**：理想平衡状态下，英雄胜率的波动区间是多少？
2. **强度量化**：如何综合胜、选、禁数据判定英雄是否“超标”？
3. **版本分析**：哪个分路才是当前版本的“答案”？
4. **鲁棒性验证**：模型在不同玩家水平（全分段 vs 巅峰赛）下是否依然可靠？

------

## 🛠️ 技术建模路径

项目采用了 **“基准模拟 - 强度评估 - 先验修正 - 灵敏校验”** 的技术路线：

### 1. 蒙特卡洛模拟 (Monte Carlo Simulation)

利用随机抽样算法模拟 $10^6$ 场完全随机对局，确立英雄胜率的理想分布（$\mu=0.5, \sigma=0.0043$），为异常值判定提供统计学“零假设”基准。

![Image of a normal distribution curve showing standard deviations](https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTw1JV6G1jkNeD9luqM3yYHhgKqKpy0RoqDb5KXYU-rFytQaM4EUNATms8ntKZScx5jSQkvfB3sQL__28r1miMNrBLKx1OuZ5RkeRoHMe2OZv92hXk)

Shutterstock



### 2. 英雄强度指数 (S-Index)

构建非线性评价模型，融合 **Win Rate (胜率)**、**Pick Rate (出场率)** 与 **Ban Rate (禁用率)**。通过 **Z-Score 检验** 识别出具有显著“厚尾效应”的超标英雄。

### 3. 贝叶斯平滑修正 (Bayesian Smoothing)

针对职业赛（KPL）样本量小、数据波动大的特征，引入贝叶斯平滑算法进行期望修正，消除小样本导致的统计偏误，确保分路影响力判定的稳健性。

### 4. 灵敏度分析 (Sensitivity Analysis)

对比“精英生态（Pro/Peak）”与“普通生态（All-Rank）”的指标偏移。实证发现：

- **高分段**：受机制驱动，中路与游走影响力领先。
- **低分段**：受数值驱动，发育路与打野影响力反超。

------

## 📂 仓库结构

Plaintext

```
├── data/                       # 原始数据集 (CSV)
│   ├── KPL_2025_Total.csv      # 职业赛全年度统计
│   └── Peak_Data_Results.csv   # 巅峰赛强度计算结果
├── scripts/                    # 核心建模脚本
│   ├── simulation.py           # 蒙特卡洛分布模拟
│   ├── strength_eval.py        # S-Index 英雄强度计算
│   └── lane_sensitivity.py     # 分路影响力与灵敏度对比
├── figures/                    # 科研可视化图表
└── README.md                   # 项目说明文档
```

------

## 📊 关键结论

- **版本核心位**：当前为“游走-中路”双核节奏版本（I-Index > 19）。
- **英雄分化**：识别出吕布、马可波罗等英雄存在“环境无关性弱势”，建议进行机制重塑。
- **模型表现**：模型对竞技环境变化表现出极高的灵敏度响应，验证了以高分段数据判定版本的科学性。

------

## 🚀 快速开始

1. **克隆项目**：

   Bash

   ```
   git clone https://github.com/YourUsername/HoK-Balance-Analysis.git
   ```

2. **安装依赖**：

   Bash

   ```
   pip install pandas numpy matplotlib seaborn scipy
   ```

3. **运行分析**：

   Bash

   ```
   python scripts/lane_sensitivity.py
   ```

------

## ⚠️ 注意事项（Precautions & Disclaimer）

**1. Data Fidelity & Logic Warning (数据可靠性与逻辑预警)**

- **CN:** **重要提示**：**除 `Data` 文件夹内的赛事数据经过人工校对保证准确外，**其余文件夹（尤其是 Q2 部分）多数英雄数据由 AI 读图生成，未经深度修正，**存在大量原始数据错误**。同时，因笔者练手之作，论文部分逻辑尚存不顺之处，模仿学习时需格外谨慎——本篇极有可能是一篇“喜提美赛 S 奖”水平的论文，如有疏漏，先行致歉。（主要是太懒了，把精力花在美赛上。）
- **EN:** **IMPORTANT**: Only the tournament data in the `Data` folder is manually verified. Other datasets (especially in Q2) were generated via AI image recognition without thorough correction, resulting in **significant data errors**. Furthermore, as a practice project, some logical inconsistencies persist. Readers should exercise extreme caution when mimicking this workflow—this paper is highly likely to be at a "Successful Participant (S Award)" level in MCM/ICM. Apologies for any oversights. (The main reason is that I am too lazy.)

**2. Research & Academic Use Only (仅限学术研究)**

- **CN:** 本项目结论仅供数学建模交流参考。数据采样有时效性，不代表官方立场，亦不构成博弈建议。
- **EN:** This project is for academic exchange only. Data is time-sensitive and does not represent official stances or betting advice.

**3. Environmental Sensitivity (环境灵敏度警示)**

- **CN:** 模型在精英环境与普通环境下结论差异巨大，请勿混淆使用，以免产生决策错位。
- **EN:** The model shows significant logic divergence between "Elite" and "General" environments. Avoid cross-application to prevent strategic misalignment.

**4. Copyright & Credits (版权说明)**

- **CN:** 英雄属性版权归官方所有。算法模型引用请注明本仓库地址。
- **EN:** Hero attributes are copyrighted by the official team. Please credit this repository when citing original algorithms.

**5. Lane Influence Divergence (分路权重偏移)**

- **CN:** 分路核心权重随竞技层级下移存在剧烈漂移，结论仅适用于特定高水平环境。
- **EN:** Lane influence weights shift drastically with skill levels; conclusions apply strictly to high-rank contexts.

------

## ⚖️ 版权声明

本项目所使用数据均源于公开渠道（王者营地、KPL 官网）的手动提取，仅供学术交流与建模参考，严禁用于商业用途。