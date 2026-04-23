import numpy as np

def compute_returns(df):

    df["a_ret"] = df["a"].diff()
    df["b_ret"] = df["b"].diff()

    df["spread_return"] = df["a_ret"] - df["beta"].shift(1) * df["b_ret"]
    df["strategy_return"] = df["position_shift"] * df["spread_return"]

    df["position_change"] = df["position"].diff().abs().fillna(0)

    cost = 0.00005
    df["net_return"] = df["strategy_return"] - (df["position_change"] * cost)

    returns = df["net_return"].fillna(0)

    if returns.std() == 0:
        return None

    sharpe = returns.mean() / returns.std() * np.sqrt(252)

    cum = (1 + returns).cumprod()
    drawdown = (cum / cum.cummax()) - 1
    max_dd = drawdown.min()

    trades = (df["position"].diff().abs() > 0).sum() / 2

    trades_df = df[df["position"].diff() != 0][["position", "net_return"]]

    return sharpe, max_dd, trades, returns, trades_df
