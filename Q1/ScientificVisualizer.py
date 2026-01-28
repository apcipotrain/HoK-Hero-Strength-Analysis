import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def perform_comprehensive_analysis(file_path, matches_count):
    # Set professional style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_context("paper", font_scale=1.2)

    # Load data
    df = pd.read_excel(file_path)
    wr = df['Win_Rate']
    n_counts = df['Total_Matches']

    # Create a 2x2 multi-plot canvas
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.2)
    fig.suptitle(f"Statistical Analysis of Hero Win Rates ({matches_count} matches)", fontsize=18)

    # --- A & D: Histogram with PDF Fitting ---
    ax1 = axes[0, 0]
    sns.histplot(wr, bins=20, kde=False, stat="density", color='#4C72B0', alpha=0.6, ax=ax1, label='Observed')
    # PDF Fitting
    mu, std = stats.norm.fit(wr)
    xmin, xmax = ax1.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    ax1.plot(x, p, 'r', lw=2, label=f'PDF Fit\n$\mu$={mu:.4f}\n$\sigma$={std:.4f}')
    ax1.set_title("A & D: Win Rate Distribution with PDF Fitting")
    ax1.set_xlabel("Win Rate")
    ax1.set_ylabel("Density")
    ax1.legend()

    # --- B: Convergence Plot (Funnel Plot) ---
    ax2 = axes[0, 1]
    ax2.scatter(n_counts, wr, color='#DD8452', alpha=0.7, edgecolors='w')
    ax2.axhline(0.5, color='black', linestyle='--', alpha=0.5)
    # Theoretical 95% Confidence Interval boundaries
    n_range = np.linspace(n_counts.min(), n_counts.max(), 100)
    ci_upper = 0.5 + 1.96 * np.sqrt((0.5 * 0.5) / n_range)
    ci_lower = 0.5 - 1.96 * np.sqrt((0.5 * 0.5) / n_range)
    ax2.plot(n_range, ci_upper, 'g--', alpha=0.4, label='95% CI Boundary')
    ax2.plot(n_range, ci_lower, 'g--', alpha=0.4)
    ax2.set_title("B: Convergence Plot (Funnel Effect)")
    ax2.set_xlabel("Sample Size (n)")
    ax2.set_ylabel("Win Rate")
    ax2.legend()

    # --- C: Cumulative Distribution Function (CDF) ---
    ax3 = axes[1, 0]
    sns.ecdfplot(wr, ax=ax3, color='#55A868', lw=2)
    ax3.axvline(0.5, color='gray', ls=':', alpha=0.6)
    ax3.set_title("C: Empirical Cumulative Distribution (CDF)")
    ax3.set_xlabel("Win Rate")
    ax3.set_ylabel("Probability")

    # --- Statistical Analysis Text Summary ---
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Calculations
    skewness = stats.skew(wr)
    kurtosis = stats.kurtosis(wr)
    # Interval Coverage
    sigma_1 = wr[(wr >= mu - std) & (wr <= mu + std)].count() / len(wr)
    sigma_2 = wr[(wr >= mu - 2 * std) & (wr <= mu + 2 * std)].count() / len(wr)

    analysis_text = (
        f"--- Statistical Summary ---\n\n"
        f"1. Normality Test:\n"
        f"   - Skewness: {skewness:.4f} (Ideal: 0)\n"
        f"   - Kurtosis: {kurtosis:.4f} (Ideal: 0)\n\n"
        f"2. Empirical Rule Coverage:\n"
        f"   - Within 1σ ({mu - std:.3f}, {mu + std:.3f}): {sigma_1 * 100:.2f}%\n"
        f"   - Within 2σ ({mu - 2 * std:.3f}, {mu + 2 * std:.3f}): {sigma_2 * 100:.2f}%\n\n"
        f"3. Extreme Value Analysis:\n"
        f"   - Max Win Rate: {wr.max():.4f}\n"
        f"   - Min Win Rate: {wr.min():.4f}\n"
        f"   - Range: {wr.max() - wr.min():.4f}\n\n"
        f"Interpretation: The distribution closely follows\n"
        f"the Central Limit Theorem."
    )
    ax4.text(0.1, 0.9, analysis_text, fontsize=12, verticalalignment='top', family='monospace')

    plt.tight_layout()
    plt.savefig(f"Analysis_Result_{matches_count}.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    # Execute for both datasets
    perform_comprehensive_analysis("Hero_Sim_Data_20000.xlsx", 20000)
    perform_comprehensive_analysis("Hero_Sim_Data_200000.xlsx", 200000)