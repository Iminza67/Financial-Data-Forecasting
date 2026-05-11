from data.loaders import (
    load_price_data,
    load_company_data,
    merge_datasets,
    load_financial_ratios
)

from preprocessing.returns import compute_daily_returns
from preprocessing.risk_metrics import (
    compute_volatility,
    compute_sharpe_ratio
)

from preprocessing.correlation import compute_correlation_matrix


def run_pipeline():

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    price_df = load_price_data()
    company_df = load_company_data()
    financial_df = load_financial_ratios()

    # -----------------------------
    # CLEAN SYMBOLS
    # -----------------------------
    price_df["symbol"] = (
        price_df["symbol"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    company_df["symbol"] = (
        company_df["symbol"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    company_df["sector"] = (
        company_df["sector"]
        .astype(str)
        .str.strip()
    )

    financial_df["symbol"] = (
        financial_df["symbol"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -----------------------------
    # KEEP ONLY REQUIRED PRICE COLS
    # HUGE RAM SAVER
    # -----------------------------
    price_df = price_df[[
        "date",
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]]

    # -----------------------------
    # REMOVE STOCKS WITH
    # MISSING CHART DATA
    # -----------------------------
    required_chart_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    valid_symbols = (
        price_df
        .dropna(subset=required_chart_cols)
        .groupby("symbol")
        .filter(lambda x: len(x) > 30)["symbol"]
        .unique()
    )

    price_df = price_df[
        price_df["symbol"].isin(valid_symbols)
    ]

    company_df = company_df[
        company_df["symbol"].isin(valid_symbols)
    ]

    financial_df = financial_df[
        financial_df["symbol"].isin(valid_symbols)
    ]

    # -----------------------------
    # REDUCE MEMORY
    # -----------------------------
    price_df["symbol"] = price_df["symbol"].astype("category")
    company_df["symbol"] = company_df["symbol"].astype("category")

    # -----------------------------
    # FINANCIAL COLUMNS
    # -----------------------------
    financial_cols = [
        "symbol",
        "price_earnings",
        "dividend_yield",
        "price_book",
        "price_sales",
        "52_week_low",
        "52_week_high"
    ]

    financial_cols = [
        c for c in financial_cols
        if c in financial_df.columns
    ]

    financial_df = financial_df[financial_cols]

    # -----------------------------
    # MERGE
    # -----------------------------
    company_df = company_df.merge(
        financial_df,
        on="symbol",
        how="left"
    )

    merged_df = merge_datasets(
        price_df,
        company_df
    )

    # -----------------------------
    # COMPUTE METRICS
    # -----------------------------
    merged_df = compute_daily_returns(merged_df)

    merged_df = compute_volatility(merged_df)

    merged_df = merged_df.dropna()

    # -----------------------------
    # SHARPE
    # -----------------------------
    sharpe_df = compute_sharpe_ratio(merged_df)

    # -----------------------------
    # SMALLER CORRELATION MATRIX
    # HUGE RAM SAVER
    # -----------------------------
    top_symbols = (
        merged_df["symbol"]
        .value_counts()
        .head(25)
        .index
    )

    corr_df = merged_df[
        merged_df["symbol"].isin(top_symbols)
    ]

    return (
        merged_df,
        sharpe_df,
        company_df
    )