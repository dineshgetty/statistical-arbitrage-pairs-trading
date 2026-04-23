import pandas as pd
from itertools import permutations
from src.model import kalman_filter
from src.strategy import generate_signals
from src.backtest import compute_returns
from src.utils import compute_stats

def scan_pairs(log_prices):

    pair_returns = {}

    train = log_prices[:'2024-01-01']
    test = log_prices['2024-01-02':]

    pairs = list(permutations(log_prices.columns, 2))
    results = []

    for a, b in pairs:

        df_train = kalman_filter(train[a], train[b])

        if df_train is None:
            continue
            
        p_value, half_life = compute_stats(df_train["spread"])

        if p_value is None:
            continue

        df_train = generate_signals(df_train, half_life)
        train_metrics = compute_returns(df_train)

        if train_metrics is None:
            continue

        sharpe_t, dd_t, trades_t, train_returns, trades_df  = train_metrics

        # filters
        if not (p_value < 0.05 and half_life < 20 and trades_t > 20 and sharpe_t > 0.7):
            continue

        # TEST
        df_test = kalman_filter(test[a], test[b])
        if df_test is None:
            continue
        df_test = generate_signals(df_test, half_life)
        test_metrics = compute_returns(df_test)

        if test_metrics is None:
            continue

        sharpe_te, dd_te, trades_te, test_returns, trades_df   = test_metrics

        if not (sharpe_te > 1 and trades_te > 15):
            continue

        pair_returns[f"{a}-{b}"] = test_returns

        results.append({
            "pair": f"{a}-{b}",
            "train_sharpe": sharpe_t,
            "test_sharpe": sharpe_te,
            "test_dd": abs(dd_te),
            "score": sharpe_te / (abs(dd_te) + 1e-6)
        })

        

    df = pd.DataFrame(results)

    if len(df) == 0:
        return df

    return df.sort_values(by="score", ascending=False), pair_returns
    
