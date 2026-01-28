import numpy as np
import pandas as pd


def run_hero_simulation(total_matches, num_heroes=129):
    """
    核心模拟引擎：基于蒙特卡洛方法的胜率分布生成
    """
    # 初始化统计容器
    wins = np.zeros(num_heroes)
    counts = np.zeros(num_heroes)
    hero_ids = np.arange(num_heroes)

    for _ in range(total_matches):
        # 随机抽取10个不重复英雄
        sampled_heroes = np.random.choice(hero_ids, size=10, replace=False)

        # 理想平衡：随机数决定红蓝胜负
        if np.random.rand() < 0.5:
            wins[sampled_heroes[:5]] += 1  # 前5人为红队
        else:
            wins[sampled_heroes[5:]] += 1  # 后5人为蓝队

        counts[sampled_heroes] += 1

    # 构造结果集
    df = pd.DataFrame({
        'Hero_ID': [i + 1 for i in range(num_heroes)],
        'Total_Matches': counts.astype(int),
        'Win_Matches': wins.astype(int),
        'Win_Rate': wins / counts
    })
    return df


# 工程化执行：生成两个基数的数据集
if __name__ == "__main__":
    for size in [20000, 200000]:
        df_result = run_hero_simulation(size)
        file_name = f"Hero_Sim_Data_{size}.xlsx"
        df_result.to_excel(file_name, index=False)
        print(f"已生成数据集: {file_name}")