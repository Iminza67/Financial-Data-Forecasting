import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm


def create_returns_histogram(df: pd.DataFrame, symbol: str, bins: int = 50):
    """
    Creates a histogram of returns with a normal distribution overlay.

    Parameters:
        df (pd.DataFrame): Dataset containing 'symbol' and 'return'
        symbol (str): Stock ticker (e.g., 'AAPL')
        bins (int): Number of histogram bins

    Returns:
        fig (go.Figure): Plotly figure
    """

    # --- Safety checks ---
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    df.columns = df.columns.str.lower()

    if "return" not in df.columns or "symbol" not in df.columns:
        raise ValueError("DataFrame must contain 'symbol' and 'return' columns.")

    # --- Filter stock ---
    stock_df = df[df["symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    returns = stock_df["return"].dropna()

    # --- Compute stats ---
    mean = returns.mean()
    std = returns.std()

    # --- Histogram ---
    hist = go.Histogram(
        x=returns,
        nbinsx=bins,
        name="Returns",
        opacity=0.75
    )

    # --- Normal distribution overlay ---
    x_vals = np.linspace(returns.min(), returns.max(), 200)
    y_vals = norm.pdf(x_vals, mean, std)

    # Scale normal curve to histogram
    y_vals_scaled = y_vals * len(returns) * (returns.max() - returns.min()) / bins

    normal_curve = go.Scatter(
        x=x_vals,
        y=y_vals_scaled,
        mode="lines",
        name="Normal Distribution"
    )

    # --- Mean & Std lines ---
    mean_line = go.Scatter(
        x=[mean, mean],
        y=[0, max(y_vals_scaled)],
        mode="lines",
        name="Mean",
        line=dict(dash="dash")
    )

    std_line_plus = go.Scatter(
        x=[mean + std, mean + std],
        y=[0, max(y_vals_scaled)],
        mode="lines",
        name="+1 Std",
        line=dict(dash="dot")
    )

    std_line_minus = go.Scatter(
        x=[mean - std, mean - std],
        y=[0, max(y_vals_scaled)],
        mode="lines",
        name="-1 Std",
        line=dict(dash="dot")
    )

    # --- Build figure ---
    fig = go.Figure(data=[hist, normal_curve, mean_line, std_line_plus, std_line_minus])

    # --- Layout ---
    fig.update_layout(
        title=f"{symbol} Return Distribution",
        template="plotly_white",
        height=500,
        xaxis_title="Returns",
        yaxis_title="Frequency",
        margin=dict(l=40, r=40, t=60, b=40),
        bargap=0.1
    )

    return fig