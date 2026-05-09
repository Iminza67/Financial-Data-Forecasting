import plotly.express as px
import pandas as pd


def create_scatter_plot(sharpe_df: pd.DataFrame, company_df: pd.DataFrame):

    # --- Clean column names ---
    sharpe_df.columns = sharpe_df.columns.str.lower()
    company_df.columns = company_df.columns.str.lower()

    # --- Merge datasets ---
    df = sharpe_df.merge(company_df, on="symbol", how="left")

    # --- Drop missing ---
    df = df.dropna(subset=["mean", "std", "sharpe"])

    # =========================================================
    # 🚀 SCALE DATA (fix clustering issue)
    # =========================================================
    df["mean"] = df["mean"] * 252 * 100
    df["std"] = df["std"] * (252 ** 0.5) * 100

    # --- Scatter plot ---
    fig = px.scatter(
        df,
        x="std",                  # risk
        y="mean",                 # return
        size="marketcap",
        color="sector",
        hover_name="symbol",      # 🔥 REQUIRED FOR CLICK SYNC
        hover_data={
            "mean": ":.2f",
            "std": ":.2f",
            "sharpe": ":.2f",
            "sector": True
        },
        title="Risk vs Return (Annualized)",
        size_max=45
    )

    # --- Reference lines ---
    fig.add_hline(
        y=df["mean"].mean(),
        line_dash="dash",
        line_color="gray",
        annotation_text="Avg Return"
    )

    fig.add_vline(
        x=df["std"].mean(),
        line_dash="dash",
        line_color="gray",
        annotation_text="Avg Risk"
    )

    # --- Style ---
    fig.update_traces(
        marker=dict(
            line=dict(width=0.7, color="black"),
            opacity=0.75
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=650,
        xaxis_title="Volatility (%)",
        yaxis_title="Return (%)",
        legend_title="Sector",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig