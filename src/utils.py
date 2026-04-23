import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm

def compute_stats(spread):

    p_value = adfuller(spread.dropna())[1]

    spread_lag = spread.shift(1)
    spread_diff = spread.diff()

    spread_df = pd.concat([spread_lag, spread_diff], axis=1).dropna()

    x = sm.add_constant(spread_df.iloc[:, 0])
    model = sm.OLS(spread_df.iloc[:, 1], x).fit()

    lambda_val = model.params.iloc[1]

    if lambda_val >= 0:
        return None, None

    half_life = -np.log(2) / lambda_val

    return p_value, half_life
