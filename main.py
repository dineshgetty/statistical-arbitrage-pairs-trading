import pandas as pd
import matplotlib.pyplot as plt
from src.data import download_data
from src.pair_selection import scan_pairs
from src.portfolio import build_portfolio
from src.model import kalman_filter
from src.strategy import generate_signals, latest_signal
from src.utils import compute_stats

from config import sector_stocks

def normalize(pair):
    a, b = pair.rsplit("-", 1)
    return "-".join(sorted([a, b]))

def run():

    all_results = []
    all_pair_returns = {}

    for sector, stocks in sector_stocks.items():

        print(f"Running: {sector}")

        log_prices = download_data(stocks, "2021-01-01", "2025-12-31")
        res, pair_returns = scan_pairs(log_prices)

        all_pair_returns.update(pair_returns)

        if len(res) == 0:
            continue

        res["sector"] = sector
        all_results.append(res)

    final_df = pd.concat(all_results, ignore_index=True)
    final_df["norm"] = final_df["pair"].apply(normalize)
    final_df = final_df.sort_values(by="score", ascending=False)
    final_df = final_df.drop_duplicates(subset="norm", keep="first")
    final_df = final_df.drop(columns=["norm"])

    print("\nTop Pairs:")
    print(final_df.head(5))

    final_df.to_csv("results/final_pairs.csv", index=False)

    # ✅ Portfolio
    portfolio = build_portfolio(final_df, all_pair_returns, top_n=5)

    print("\nPortfolio Results:")
    print("Sharpe:", portfolio["sharpe"])
    print("Max Drawdown:", portfolio["max_dd"])

    # 🔴 LIVE SIGNAL FOR TOP PAIR

    top_pair = final_df.iloc[0]["pair"]
    a, b = top_pair.split("-")

    # download fresh data for signal
    log_prices = download_data([a, b], "2024-01-01", "2025-12-31")

    df = kalman_filter(log_prices[a], log_prices[b])

    if df is not None:
        _, half_life = compute_stats(df["spread"])
        df = generate_signals(df, half_life)

        plot_spread_zscore(df, f"{a}-{b}")

        signal = latest_signal(df)

        print("\nLive Signal for Top Pair:")
        print(top_pair, signal)

    # ✅ Equity Curve
    plt.figure()
    plt.plot(portfolio["cum_returns"])
    plt.title("Portfolio Equity Curve")
    plt.savefig("results/equity_curve.png")
    plt.close()

    # ✅ Drawdown
    plt.figure()
    plt.plot(portfolio["drawdown"])
    plt.title("Portfolio Drawdown")
    plt.savefig("results/drawdown.png")
    plt.close()

    plt.figure()
    plt.plot(portfolio["rolling_sharpe"])
    plt.title("Rolling Sharpe (3M Window)")
    plt.savefig("results/rolling_sharpe.png")
    plt.close()


if __name__ == "__main__":
    run()
