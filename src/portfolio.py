import pandas as pd
import numpy as np

def build_portfolio(final_df, pair_returns, top_n=10):

    # Select top N pairs
    selected = final_df.head(top_n)["pair"].tolist()

    portfolio_df = pd.DataFrame()

    for pair in selected:
        if pair in pair_returns:
            r = pair_returns[pair]
            portfolio_df[pair] = r

    # Align dates (important)
    portfolio_df = portfolio_df.fillna(0)

    # Equal weight portfolio
    portfolio_df["portfolio_return"] = portfolio_df.mean(axis=1)

    returns = portfolio_df["portfolio_return"]

    # Metrics
    sharpe = returns.mean() / returns.std() * np.sqrt(252)

    rolling_sharpe = (
        returns.rolling(63).mean() / returns.rolling(63).std()
    ) * np.sqrt(252)

    cum = (1 + returns).cumprod()
    drawdown = (cum / cum.cummax()) - 1
    max_dd = drawdown.min()

    return {
        "returns": returns,
        "cum_returns": cum,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "max_dd": max_dd,
        "selected_pairs": selected,
        "rolling_sharpe": rolling_sharpe
    }
