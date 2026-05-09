import pandas as pd
import plotly.graph_objects as go


def create_candlestick_chart(df: pd.DataFrame, symbol: str, ma_window: int = 20):
    """
    Create a candlestick chart with optional moving average.

    Parameters:
        df (pd.DataFrame): Dataset containing OHLC data
        symbol (str): Stock ticker (e.g., 'AAPL')
        ma_window (int): Moving average window (default = 20)

    Returns:
        fig (go.Figure): Plotly figure
    """

    # --- Safety checks ---
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Normalize column names
    df.columns = df.columns.str.lower()

    required_cols = {"date", "symbol", "open", "high", "low", "close"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    # --- Filter selected stock ---
    stock_df = df[df["symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    # --- Ensure datetime + sorting ---
    stock_df["date"] = pd.to_datetime(stock_df["date"])
    stock_df = stock_df.sort_values("date")

    # --- Create candlestick chart ---
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=stock_df["date"],
            open=stock_df["open"],
            high=stock_df["high"],
            low=stock_df["low"],
            close=stock_df["close"],
            name=f"{symbol} Price"
        )
    )

    # --- Add Moving Average ---
    if ma_window is not None and ma_window > 0:
        stock_df["ma"] = stock_df["close"].rolling(window=ma_window).mean()

        fig.add_trace(
            go.Scatter(
                x=stock_df["date"],
                y=stock_df["ma"],
                mode="lines",
                name=f"{ma_window}-Day MA",
                line=dict(width=2)
            )
        )

    # --- Layout styling ---
    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        template="plotly_white",
        height=500,
        xaxis_title="Date",
        yaxis_title="Price",
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_rangeslider_visible=False,  # cleaner UI
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig