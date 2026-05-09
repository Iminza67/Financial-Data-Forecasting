import pandas as pd
import numpy as np


def compute_volatility(df, window=30):
    df = df.copy()

    df['volatility'] = (
        df.groupby('symbol')['return']
        .rolling(window)
        .std()
        .reset_index(level=0, drop=True)
    )

    return df


def compute_sharpe_ratio(df, risk_free_rate=0.0):
    sharpe_df = (
        df.groupby('symbol')['return']
        .agg(['mean', 'std'])
        .reset_index()
    )

    sharpe_df['sharpe'] = (
            (sharpe_df['mean'] - risk_free_rate) / sharpe_df['std']
    )

    return sharpe_df