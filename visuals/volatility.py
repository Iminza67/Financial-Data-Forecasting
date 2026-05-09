import pandas as pd
import plotly.graph_objects as go


def create_volatility_chart(df: pd.DataFrame, symbol: str, window: int = 30):
    """
    Rolling volatility chart for a selected stock

    Parameters:
        df (pd.DataFrame): Dataset with returns
        symbol (str): Stock ticker
        window (int): Rolling window size (default 30)

    Returns:
        fig (go.Figure)
    """

    # --- Safety checks ---
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    df.columns = df.columns.str.lower()

    required_cols = {"symbol", "date", "return"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    # --- Filter stock ---
    stock_df = df[df["symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    # --- Ensure proper format ---
    stock_df["date"] = pd.to_datetime(stock_df["date"])
    stock_df = stock_df.sort_values("date")

    # --- Compute rolling volatility ---
    stock_df["volatility"] = (
        stock_df["return"]
        .rolling(window=window)
        .std()
    )

    # --- Create figure ---
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_df["date"],
            y=stock_df["volatility"],
            mode="lines",
            name=f"{window}-Day Rolling Volatility",
            line=dict(width=2)
        )
    )

    # --- Highlight high volatility periods ---
    mean_vol = stock_df["volatility"].mean()

    fig.add_hline(
        y=mean_vol,
        line_dash="dash",
        line_color="red",
        annotation_text="Avg Volatility",
        annotation_position="top left"
    )

    # --- Layout ---
    fig.update_layout(
        title=f"{symbol} Rolling Volatility ({window}-Day)",
        template="plotly_white",
        height=500,
        xaxis_title="Date",
        yaxis_title="Volatility",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig