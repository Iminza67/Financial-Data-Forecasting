# Financial-Data-Forecasting

Dashboard-first S&P 500 analysis for quantitative analysts to quickly identify stocks and sectors with the strongest risk-adjusted return profiles.

## Research Question

How can quant analysts efficiently identify which S&P 500 stocks and sectors offer superior risk-adjusted returns, and what volatility/correlation dynamics drive those profiles?

## Datasets

- Primary dataset: [S&P 500 Stocks](https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks)
- Backup dataset: [S&P 500 Companies with Financial Information](https://www.kaggle.com/datasets/paytonfisher/sp-500-companies-with-financial-information)

The analysis joins both datasets by `Symbol` (ticker) to combine historical time-series behavior with company metadata/fundamentals.

## Stage Cast (Target Users)

- **Audience:** Aria Chen and Marcus Webb, junior quant analysts at a long/short equity hedge fund (~$2B AUM)
- **Workflow constraints:** Time-constrained pre-market and between-meeting analysis on desktop dashboards
- **Primary activities:** Screening, comparing, investigating, and validating risk/return and portfolio correlation behavior

## Core Attributes Used

The merged dataset contains the dimensions needed for the dashboard tasks:

1. `Symbol` (join key and stock identity)
2. `Date` (time axis)
3. `Close` (return and Sharpe calculations)
4. `Volume` (liquidity/confirmation behavior)
5. `Sector` (grouping and color encoding)
6. `Market Cap` (scatter bubble size)
7. `Company Name` (details-on-demand)

## Required Dashboard Views

- Risk vs return scatter plot (Sharpe ratio vs return, point size by market cap)
- Candlestick chart for selected stock history
- Rolling volatility line chart
- Return distribution histogram with normal curve overlay
- Correlation heatmap to identify clusters
- Volume bar chart aligned with price movement checks
