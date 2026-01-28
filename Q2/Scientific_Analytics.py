import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载数据
file_name = 'Honor_of_Kings_Peak_Data_2026.csv'
df = pd.read_csv(file_name, encoding='utf-8-sig')

# 2. 定义问题一的常数基准
MU_IDEAL = 0.5
SIGMA_IDEAL = 0.0043
LAMBDA = 0.05

# 3. 指标计算
df['Z_Score'] = (df['Win_Rate'] - MU_IDEAL) / SIGMA_IDEAL
df['S_Index'] = (df['Win_Rate'] - MU_IDEAL) * np.log(df['Pick_Rate'] * 100 + 1) + LAMBDA * df['Ban_Rate']
df['P_Value'] = 2 * (1 - stats.norm.cdf(np.abs(df['Z_Score'])))

# --- 核心统计报告 (控制台输出) ---
significant_op = df[df['Z_Score'] > 3].sort_values('Z_Score', ascending=False)
significant_bottom = df[df['Z_Score'] < -3].sort_values('Z_Score', ascending=True)

# 皮尔曼相关分析
tier_map = {'T0': 4, 'T1': 3, 'T2': 2, 'T3': 1, 'T4': 0}
df['Tier_Numeric'] = df['Tier'].map(tier_map)
corr_val, p_val_corr = stats.spearmanr(df['S_Index'], df['Tier_Numeric'], nan_policy='omit')

# 离散度倍率
sigma_actual = df['Win_Rate'].std()
dispersion_ratio = sigma_actual / SIGMA_IDEAL

print("-" * 60)
print("【问题二：科研统计深度报告】")
print("-" * 60)
print(f"1. 显著性检验结果 (显著水平 3-sigma):")
print(f"   - 统计显著超标(OP)英雄数: {len(significant_op)}")
print(f"   - 统计显著下水道(Bottom)英雄数: {len(significant_bottom)}")
print("\n   [Top 5 显著超标英雄名单]:")
print(significant_op[['Hero_Name', 'Win_Rate', 'Z_Score', 'P_Value']].head().to_string(index=False))

print(f"\n2. 关联度分析 (S-Index 与 官方热度梯度):")
print(f"   - Spearman Rho: {corr_val:.4f}")
print(f"   - P-Value: {p_val_corr:.4e}")

print(f"\n3. 版本平衡离散度:")
print(f"   - 理论随机偏差: {SIGMA_IDEAL:.4f}")
print(f"   - 实际观测偏差: {sigma_actual:.4f}")
print(f"   - 离散扩大倍率: {dispersion_ratio:.2f}x (不平衡程度量化指标)")
print("-" * 60)

# --- 科研风格绘图 (Scientific Plotting) ---
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_context("paper", font_scale=1.4) # 调整为适合论文引用的字体比例

# 图1: Z-Score 分布图 (使用深蓝科研色)
plt.figure(figsize=(9, 6))
sns.histplot(df['Z_Score'], bins=18, kde=True, color='#4C72B0', edgecolor='white', alpha=0.85)
plt.axvline(3, color='#C44E52', linestyle='--', linewidth=2, label='OP Critical (Z=3)')
plt.axvline(-3, color='#55A868', linestyle='--', linewidth=2, label='Bottom Critical (Z=-3)')
plt.title('Distribution of Hero Z-Scores (Peak Tournament 1350+)', fontsize=15, pad=15)
plt.xlabel('Z-Score (Standardized Deviation)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig("Scientific_Z_Score_Dist.png", dpi=300)

# 图2: S-Index 箱型图 (叠加热点散点图)
plt.figure(figsize=(9, 6))
# 使用学术配色 Set2，并添加散点分布展现数据透明度
sns.boxplot(data=df, x='Tier', y='S_Index', order=['T0', 'T1', 'T2', 'T3', 'T4'],
            palette='Set2', width=0.5, linewidth=1.2, fliersize=0)
sns.stripplot(data=df, x='Tier', y='S_Index', order=['T0', 'T1', 'T2', 'T3', 'T4'],
              color=".3", size=3, alpha=0.4, jitter=True)
plt.title('S-Index vs. Official Tier Classifications', fontsize=15, pad=15)
plt.xlabel('Official Heat Tier (Official)', fontsize=12)
plt.ylabel('Intensity Index (S)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("Scientific_S_Index_Boxplot.png", dpi=300)