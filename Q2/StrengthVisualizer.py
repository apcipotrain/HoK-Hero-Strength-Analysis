import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 定义文件名（请确保文件名与文件夹中的实际名称完全一致）
file_name = 'Honor_of_Kings_Peak_Data_2026.csv'

# 2. 读取数据并定义为 df
# 如果你的 CSV 文件是用 utf-8-sig 存的，建议加上 encoding 参数
df = pd.read_csv(file_name, encoding='utf-8-sig')

# 计算强度指数 S (Intensity Index)
sigma = 0.0043
lam = 0.05
df['S_Index'] = (df['Win_Rate'] - 0.5) * np.log(df['Pick_Rate'] * 100 + 1) + lam * df['Ban_Rate']

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['SimHei'] # 解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False

# --- 案例一：三维热力气泡图 (你要求的原版配色) ---
plt.figure(figsize=(12, 8))
# 使用 RdYlGn 调色盘：绿色代表强度高，红色代表强度低
sc = plt.scatter(df['Pick_Rate'], df['Win_Rate'], s=df['Ban_Rate']*1500 + 50,
                c=df['S_Index'], cmap='RdYlGn', alpha=0.7, edgecolors='gray')
plt.colorbar(sc, label='Intensity Index (S)')

# 为 S 指数排名前 10 的英雄添加标注
top_10 = df.nlargest(10, 'S_Index')
for i, row in top_10.iterrows():
    plt.annotate(row['Hero_Name'], (row['Pick_Rate'], row['Win_Rate']), xytext=(5,5),
                 textcoords='offset points', fontsize=10, fontweight='bold')

plt.axhline(0.5, color='black', lw=1, ls='--')
plt.title('Win Rate vs. Pick Rate (Bubble Size = Ban Rate)', fontsize=15)
plt.xlabel('Pick Rate (登场率)', fontsize=12)
plt.ylabel('Win Rate (胜率)', fontsize=12)
plt.savefig("Bubble_Chart_Intensity.png", dpi=300)

# --- 案例二：四象限策略分析图 (用于分类讨论) ---
plt.figure(figsize=(12, 8))
avg_pr = df['Pick_Rate'].mean()
sns.scatterplot(data=df, x='Pick_Rate', y='Win_Rate', size='Ban_Rate', sizes=(20, 500), alpha=0.5, color='royalblue')
plt.axhline(0.5, color='red', linestyle='--', alpha=0.5) # 胜率平衡线
plt.axvline(avg_pr, color='blue', linestyle='--', alpha=0.5) # 平均登场率线

# 区域标注
plt.text(df['Pick_Rate'].max()*0.7, 0.54, 'OP / Powerhouses (版本答案)', fontsize=12, color='red', fontweight='bold')
plt.text(0.01, 0.54, 'Niche Experts (绝活英雄)', fontsize=12, color='darkgreen')
plt.text(0.01, 0.46, 'Strugglers (下水道)', fontsize=12, color='black')
plt.text(df['Pick_Rate'].max()*0.7, 0.46, 'Popular but Weak (陷阱英雄)', fontsize=12, color='orange')

plt.title('Quadrant Analysis of Hero Performance', fontsize=15)
plt.savefig("Quadrant_Analysis.png", dpi=300)

# --- 案例三：极端强度英雄排行 (直方图) ---
plt.figure(figsize=(10, 8))
# 取最高 10 名和最低 10 名
extreme_heroes = pd.concat([df.nlargest(10, 'S_Index'), df.nsmallest(10, 'S_Index')])
extreme_heroes = extreme_heroes.sort_values('S_Index')
colors = ['#FF4444' if x < 0 else '#44BB44' for x in extreme_heroes['S_Index']]
plt.barh(extreme_heroes['Hero_Name'], extreme_heroes['S_Index'], color=colors)
plt.title('Top 10 and Bottom 10 Heroes by Intensity Index (S)', fontsize=15)
plt.xlabel('Intensity Index (S)')
plt.grid(axis='x', alpha=0.3)
plt.savefig("Ranked_Index_Chart.png", dpi=300)