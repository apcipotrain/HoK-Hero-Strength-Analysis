import pandas as pd
import numpy as np

# 1. 加载数据 (请确保文件名与您本地一致)
file_name = 'Honor_of_Kings_Peak_Data_2026.csv'
try:
    df = pd.read_csv(file_name, encoding='utf-8-sig')
except FileNotFoundError:
    file_name = 'Honor_of_Kings_Peak_Data_2026.csv'
    df = pd.read_csv(file_name, encoding='utf-8-sig')

# 2. 定义模型参数 (基于问题一的统计基准)
MU_IDEAL = 0.5
SIGMA_IDEAL = 0.0043
LAMBDA = 0.05

# 3. 执行核心计算
# 计算 Z-Score (偏离理想平衡的程度)
df['Z_Score'] = (df['Win_Rate'] - MU_IDEAL) / SIGMA_IDEAL

# 计算 S-Index (综合强度指数)
# S = (WR - 0.5) * ln(PR * 100 + 1) + lambda * BR
df['S_Index'] = (df['Win_Rate'] - MU_IDEAL) * np.log(df['Pick_Rate'] * 100 + 1) + LAMBDA * df['Ban_Rate']

# 4. 建立基于分位数的动态判定准则 (个位数判定逻辑)
# 获取 S 指数的前 5% (P95) 和末 5% (P5) 作为边界
top_threshold = df['S_Index'].quantile(0.95)
bottom_threshold = df['S_Index'].quantile(0.05)

def final_judge(row):
    if row['S_Index'] >= top_threshold and row['Win_Rate'] > 0.5:
        return '超标 (Overpowered)'
    elif row['S_Index'] <= bottom_threshold and row['Win_Rate'] < 0.5:
        return '下水道 (Underpowered)'
    else:
        return '平衡 (Balanced)'

df['Final_Conclusion'] = df.apply(final_judge, axis=1)

# 5. 按照强度得分进行降序排列
df_sorted = df.sort_values(by='S_Index', ascending=False)

# 6. 导出结果表格 (utf-8-sig 编码，Excel 双击即阅)
output_file = "Hero_Strength_Evaluation_Results.csv"
df_sorted.to_csv(output_file, index=False, encoding='utf-8-sig')

# 7. 控制台实时打印结论报告
print("-" * 60)
print(f"【问题二：强度评价模型结果导出报告】")
print(f"文件已保存至: {output_file}")
print("-" * 60)
print(f"动态判别界限 (分位法):")
print(f" - 超标红线 (P95): {top_threshold:.4f}")
print(f" - 下水道蓝线 (P5): {bottom_threshold:.4f}")
print("-" * 60)

print("\n>>> 最终判定为“超标”的英雄名单 (Top 5%):")
op_df = df[df['Final_Conclusion'] == '超标 (Overpowered)'].sort_values('S_Index', ascending=False)
print(op_df[['Hero_Name', 'Win_Rate', 'Ban_Rate', 'S_Index']].to_string(index=False))

print("\n>>> 最终判定为“下水道”的英雄名单 (Bottom 5%):")
bt_df = df[df['Final_Conclusion'] == '下水道 (Underpowered)'].sort_values('S_Index', ascending=True)
print(bt_df[['Hero_Name', 'Win_Rate', 'Pick_Rate', 'S_Index']].to_string(index=False))
print("-" * 60)