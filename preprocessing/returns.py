import pandas as pd


def compute_daily_returns(df):
    df = df.copy()

    df['return'] = df.groupby('symbol')['close'].pct_change(fill_method=None)

    return df