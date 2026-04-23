import numpy as np

def generate_signals(df, half_life):

    window = int(max(30, round(half_life * 10)))

    df["mean"] = df["spread"].rolling(window).mean().shift(1)
    df["std"] = df["spread"].rolling(window).std().shift(1)

    df["z"] = (df["spread"] - df["mean"]) / df["std"]
    df = df.dropna()

    entry_z, exit_z, stop_z = 2, 0.5, 3
    max_holding = 10

    position, holding_days = 0, 0
    positions = []

    for z in df["z"]:
        if position == 0:
            holding_days = 0
            if z > entry_z:
                position = -1
            elif z < -entry_z:
                position = 1
        else:
            holding_days += 1
            if ((position == -1 and (z < exit_z or z > stop_z)) or
                (position == 1 and (z > -exit_z or z < -stop_z)) or
                (holding_days > max_holding)):
                position = 0
                holding_days = 0

        positions.append(position)

    df = df.copy()

    df.loc[:, "position"] = positions
    df.loc[:, "position_shift"] = df["position"].shift(1).fillna(0)

    

    return df

def latest_signal(df):

    latest = df.iloc[-1]

    return {
        "zscore": float(latest["z"]),
        "position": int(latest["position"])
    }
