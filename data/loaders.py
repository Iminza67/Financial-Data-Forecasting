import pandas as pd

def load_financial_ratios():
    df = pd.read_csv("data/raw/financials.csv")

    #cleaning
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")   # <-- IMPORTANT FIX
    )

    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()

    return df

def load_price_data(path="data/raw/sp500_stocks.csv"):
    df = pd.read_csv(path)

    # ✅ Normalize ALL column names
    df.columns = df.columns.str.lower()

    # Ensure correct types
    df['date'] = pd.to_datetime(df['date'])
    df['symbol'] = df['symbol'].str.strip().str.upper()
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # Sort for time-series operations
    df = df.sort_values(by=['symbol', 'date'])

    return df


def load_company_data(path="data/raw/sp500_companies.csv"):
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.lower()

    return df


def merge_datasets(price_df, company_df):
    merged = pd.merge(price_df, company_df, on="symbol", how="left")

    return merged

