import plotly.io as pio
from preprocessing.pipeline import run_pipeline
from visuals.scatter import create_scatter_plot
from visuals.candlestick import create_candlestick_chart
from visuals.histogram import create_returns_histogram
from visuals.heatmap import create_correlation_heatmap
from visuals.volatility import create_volatility_chart
from visuals.volume import create_volume_chart
from data.loaders import load_company_data

pio.renderers.default = "browser"

# Run pipeline
df, sharpe_df, corr_matrix = run_pipeline()

# Load company metadata
company_df = load_company_data()

# --- TEST SCATTER ---
scatter_fig = create_scatter_plot(sharpe_df, company_df)
scatter_fig.show()
print("Sample symbols:", df["symbol"].unique()[:50])
# --- TEST CANDLESTICK ---

candlestick_fig = create_candlestick_chart(df, "AMZN")
candlestick_fig.show()

# --- TEST HISTOGRAM ---
print(df["symbol"].unique()[:20])
hist_fig = create_returns_histogram(df, "AMZN")
hist_fig.show()

# --- TEST HEATMAP ---
heatmap_fig = create_correlation_heatmap(corr_matrix)
heatmap_fig.show()

#TEST VOLATILITY CHART
vol_fig = create_volatility_chart(df, "AMZN")
vol_fig.show()

#TEST VOLUME CHART
vol_fig = create_volume_chart(df, "AMZN")
vol_fig.show()
print(df[["symbol", "volume"]].dropna().head(20))