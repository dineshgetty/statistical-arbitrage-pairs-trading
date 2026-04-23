import numpy as np
import pandas as pd
from pykalman import KalmanFilter

def kalman_filter(series_a, series_b):
    df = pd.DataFrame({"a": series_a, "b": series_b}).dropna()

    if len(df) < 30:
        return None

    obs_mat = np.vstack([df["b"], np.ones(len(df))]).T[:, np.newaxis]

    kf = KalmanFilter(
        transition_matrices=np.eye(2),
        observation_matrices=obs_mat,
        initial_state_mean=[0, 0],
        initial_state_covariance=np.ones((2, 2)),
        observation_covariance=1,
        transition_covariance=0.001 * np.eye(2)
    )

    state_means, _ = kf.filter(df["a"].values)

    df["beta"] = state_means[:, 0]
    df["alpha"] = state_means[:, 1]

    df["spread"] = df["a"] - (df["beta"] * df["b"] + df["alpha"])

    return df
