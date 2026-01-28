import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# 1. 载入数据并标准化
df_pro = pd.read_csv('KPL_2025_Total_Summary.csv', encoding='utf-8-sig')
df_peak = pd.read_csv('Hero_Strength_Evaluation_Results.csv', encoding='utf-8-sig')

def clean_name(name):
    return str(name).replace('（', '(').replace('）', ')').strip()

df_pro['Hero_Name'] = df_pro['Hero_Name'].apply(clean_name)
df_peak['Hero_Name'] = df_peak['Hero_Name'].apply(clean_name)

# 2. 策略：贝叶斯平滑 (K=10)
K = 10
df_pro['Smoothed_WR'] = (df_pro['Win_Count'] + K * 0.5) / (df_pro['Appearance_Count'] + K)
df_merged = pd.merge(df_pro, df_peak, on='Hero_Name', how='inner')

# 3. 分路映射
def get_lane(row):
    name, occ = row['Hero_Name'], row['Occupation']
    jungle_list = ["大司命", "云缨", "暃", "裴擒虎", "韩信", "澜", "镜", "宫本武藏", "赵云", "曜", "铠", "李白", "露娜", "百里玄策", "影"]
    if name in jungle_list: return "打野"
    if '射手' in occ: return "发育路"
    if '法师' in occ: return "中路"
    if '辅助' in occ: return "游走"
    if '坦克' in occ or '战士' in occ: return "对抗路"
    return "未知"

df_merged['Lane'] = df_merged.apply(get_lane, axis=1)

# ==========================================
# 修正：中文显示配置 & 高级科研配色 (Nature Style)
# ==========================================
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans'] # 自动适配Win/Mac
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_theme(style="white", font='SimHei')
except:
    pass

# 定义你要求的经典高级配色
scientific_palette = {
    "游走": "#CF5C2A",   #
    "中路": "#1663AA",   #
    "打野": "#EDD998",   #
    "发育路": "#77AC30", #
    "对抗路": "#299d8f", #
    "未知": "#8C8C8C"    # 灰
}

# --- 图表 A：散点图美化 ---
plt.figure(figsize=(11, 7))
# 使用 despine 移除不必要的边框，符合现代审美
sns.despine()

# 核心散点绘制
scatter = sns.scatterplot(
    data=df_merged, x='S_Index', y='Appearance_Count',
    hue='Lane', size='Smoothed_WR', sizes=(60, 300),
    palette=scientific_palette, alpha=0.75,
    edgecolor='#333333', linewidth=0
)

# 仅标注最核心的 6 个英雄，避免视觉拥挤
top_list = df_merged.sort_values('Appearance_Count', ascending=False).head(6)
for i, row in top_list.iterrows():
    plt.annotate(row['Hero_Name'],
                 xy=(row['S_Index'], row['Appearance_Count']),
                 xytext=(0, 12), textcoords='offset points',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.axvline(0, color='gray', linestyle=':', alpha=0.5)
plt.title('2025 KPL 战术价值与英雄强度映射矩阵', fontsize=15, pad=20, fontweight='bold')
plt.xlabel('强度指标 (S-Index)', fontsize=12)
plt.ylabel('职业赛总场次 (Games)', fontsize=12)

# 图例优化
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, title='分路定位', frameon=False)
plt.tight_layout()
plt.savefig("Scatter_Professional_Scientific.png", dpi=300)

# --- 图表 B：雷达图美化 ---
lane_group = df_merged.groupby('Lane').agg({
    'Appearance_Count': 'mean',
    'S_Index': 'mean',
    'Ban_Rate': 'mean',
    'Smoothed_WR': 'mean'
}).reset_index()

metrics = ['Appearance_Count', 'S_Index', 'Ban_Rate', 'Smoothed_WR']
lane_norm = lane_group.copy()
for m in metrics:
    lane_norm[m] = (lane_norm[m] - lane_norm[m].min()) / (lane_norm[m].max() - lane_norm[m].min())

categories = ['战术普及', '数值强度', '禁选权重', '胜率表现']
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

for i, row in lane_norm.iterrows():
    lane_name = row['Lane']
    if lane_name == "未知": continue
    values = row[metrics].tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2.5, label=lane_name, color=scientific_palette.get(lane_name))
    ax.fill(angles, values, color=scientific_palette.get(lane_name), alpha=0.1)

plt.xticks(angles[:-1], categories, fontsize=12, fontweight='bold')
plt.title('2025 全年度各分路版本影响力指纹', fontsize=16, y=1.08, fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=False)
plt.tight_layout()
plt.savefig("Radar_Professional_Scientific.png", dpi=300)

print("✅ 图片已生成，采用您要求的经典高级配色！")