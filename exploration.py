import pandas as pd

financial_df = pd.read_csv("data/raw/financials.csv")

print(financial_df.head())
print(financial_df.columns)
print(financial_df.dtypes)