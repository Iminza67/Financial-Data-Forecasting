import pandas as pd
import plotly.graph_objects as go


def create_volume_chart(df: pd.DataFrame, symbol: str):
    df.columns = df.columns.str.lower()

    stock_df = df[df["symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    stock_df["date"] = pd.to_datetime(stock_df["date"])
    stock_df = stock_df.sort_values("date")

    # IMPORTANT FIXES
    stock_df = stock_df.dropna(subset=["volume"])
    stock_df = stock_df[stock_df["volume"] > 0]
    stock_df = stock_df.tail(300)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=stock_df["date"],
            y=stock_df["volume"],
            name="Volume",
            marker_color="steelblue"
        )
    )

    avg_volume = stock_df["volume"].mean()

    fig.add_hline(
        y=avg_volume,
        line_dash="dash",
        line_color="red",
        annotation_text="Avg Volume"
    )

    fig.update_layout(
        title=f"{symbol} Trading Volume",
        template="plotly_white",
        height=400,
        xaxis_title="Date",
        yaxis_title="Volume",
        yaxis=dict(rangemode="tozero")
    )

    return fig