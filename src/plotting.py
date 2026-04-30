import matplotlib.pyplot as plt

def plot_spread_zscore(df, pair_name):
    """
    Plots spread and z-score for a given pair
    """

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # --- Spread Plot ---
    axes[0].plot(df.index, df["spread"], label="Spread")
    axes[0].axhline(df["spread"].mean(), linestyle="--", label="Mean")
    axes[0].set_title(f"{pair_name} Spread")
    axes[0].legend()

    # --- Z-Score Plot ---
    axes[1].plot(df.index, df["z"], label="Z-Score")
    axes[1].axhline(2, linestyle="--", label="+2")
    axes[1].axhline(-2, linestyle="--", label="-2")
    axes[1].axhline(0, linestyle="--", label="Mean")
    axes[1].set_title(f"{pair_name} Z-Score")
    axes[1].legend()
