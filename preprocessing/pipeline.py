from data.loaders import load_price_data, load_company_data, merge_datasets, load_financial_ratios
from preprocessing.returns import compute_daily_returns
from preprocessing.risk_metrics import compute_volatility, compute_sharpe_ratio
from preprocessing.correlation import compute_correlation_matrix


def run_pipeline():
    # Load
    price_df = load_price_data()
    company_df = load_company_data()
    financial_df = load_financial_ratios()

    # -----------------------------
    # CLEAN COMPANY DATA
    # -----------------------------
    company_df["symbol"] = company_df["symbol"].astype(str).str.strip().str.upper()
    company_df["sector"] = company_df["sector"].astype(str).str.strip()

    # -----------------------------
    # SELECT ONLY NEW COLUMNS (IMPORTANT)
    # -----------------------------
    financial_df = financial_df[[
        "symbol",
        "price_earnings",
        "dividend_yield",
        "price_book",
        "price_sales",
        "52_week_low",
        "52_week_high"
    ]]

    # -----------------------------
    # MERGE COMPANY + FINANCIALS
    # -----------------------------
    company_df = company_df.merge(financial_df, on="symbol", how="left")

    # Merge
    merged_df = merge_datasets(price_df, company_df)

    # Compute metrics
    merged_df = compute_daily_returns(merged_df)
    merged_df = compute_volatility(merged_df)

    # Drop NaNs from rolling calculations
    merged_df = merged_df.dropna()

    # Sharpe (separate aggregated dataset)
    sharpe_df = compute_sharpe_ratio(merged_df)

    # Correlation matrix
    corr_matrix = compute_correlation_matrix(merged_df)

    return merged_df, sharpe_df, corr_matrix, company_df