from dash import Dash, dcc, html, Input, Output
import plotly.io as pio
import plotly.graph_objs as go

from preprocessing.pipeline import run_pipeline
from data.loaders import load_company_data
from functools import lru_cache

from visuals.scatter import create_scatter_plot
from visuals.candlestick import create_candlestick_chart
from visuals.histogram import create_returns_histogram
from visuals.heatmap import create_correlation_heatmap
from visuals.volatility import create_volatility_chart
from visuals.volume import create_volume_chart

pio.renderers.default = "browser"

# -----------------------
# LOAD DATA ONCE
# -----------------------
@lru_cache
def get_data():
    return run_pipeline()

df, sharpe_df, corr_matrix, company_df = get_data()
#company_df = load_company_data()

# --- CLEAN DATA (important for sector filtering) ---
company_df["sector"] = company_df["sector"].astype(str).str.strip()
company_df["symbol"] = company_df["symbol"].astype(str).str.strip()
df["symbol"] = df["symbol"].astype(str).str.strip()
sharpe_df["symbol"] = sharpe_df["symbol"].astype(str).str.strip()

symbols = sorted(df["symbol"].unique())

# -----------------------
# HELPER: CLICK → SYMBOL
# -----------------------
def get_symbol_from_click(clickData, fallback_symbol):
    if clickData and "points" in clickData:
        return clickData["points"][0]["hovertext"]
    return fallback_symbol

# -----------------------
# DASH APP
# -----------------------
app = Dash(__name__)

app.layout = html.Div([

    html.H1("S&P 500 Risk-Return Dashboard", style={
        "textAlign": "center",
        "marginBottom": "20px"
    }),

    html.Div([

        html.Div([
            html.Label("Stock"),
            dcc.Dropdown(
                id="symbol-dropdown",
                options=[{"label": s, "value": s} for s in symbols],
                value=symbols[0]
            )
        ], style={"width": "48%"}),

        html.Div([
            html.Label("Sector"),
            dcc.Dropdown(
                id="sector-dropdown",
                options=[{"label": s, "value": s} for s in company_df["sector"].dropna().unique()],
                value=None,
                placeholder="Select sector"
            )
        ], style={"width": "48%"})

    ], style={"display": "flex", "justifyContent": "space-between"}),

    dcc.Graph(id="scatter"),

    html.Div([
        dcc.Graph(id="candlestick"),
        dcc.Graph(id="volume")
    ], style={"display": "flex"}),

    html.Div([
        dcc.Graph(id="volatility"),
        dcc.Graph(id="histogram")
    ], style={"display": "flex"}),

    dcc.Graph(id="heatmap")
])

# -----------------------
# CALLBACKS
# -----------------------

# 📊 Scatter (with sector filtering)
@app.callback(
    Output("scatter", "figure"),
    Input("sector-dropdown", "value"),
    Input("symbol-dropdown", "value")
)
def update_scatter(sector, selected_symbol):

    df_filtered = df.copy()

    if sector:
        symbols_in_sector = company_df[company_df["sector"] == sector]["symbol"]
        df_filtered = df_filtered[df_filtered["symbol"].isin(symbols_in_sector)]

    # Aggregate returns
    scatter_df = df_filtered.groupby("symbol").agg({
        "return": "mean"
    }).reset_index()

    # Merge Sharpe
    scatter_df = scatter_df.merge(sharpe_df, on="symbol", how="inner")

    if scatter_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available for selected sector")
        return fig

    fig = create_scatter_plot(scatter_df, company_df)

    # Highlight selected stock
    if selected_symbol and selected_symbol in scatter_df["symbol"].values:
        selected = scatter_df[scatter_df["symbol"] == selected_symbol]

        fig.add_scatter(
            x=selected["std"],
            y=selected["mean"],
            mode="markers",
            marker=dict(size=14, color="red"),
            name="Selected Stock"
        )

    return fig


# 📉 Candlestick (CLICK SYNC)
@app.callback(
    Output("candlestick", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_candlestick(clickData, dropdown_symbol):
    symbol = get_symbol_from_click(clickData, dropdown_symbol)

    if not symbol:
        return go.Figure()

    return create_candlestick_chart(df, symbol)


# 📊 Volume (CLICK SYNC)
@app.callback(
    Output("volume", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_volume(clickData, dropdown_symbol):
    symbol = get_symbol_from_click(clickData, dropdown_symbol)

    if not symbol:
        return go.Figure()

    return create_volume_chart(df, symbol)


# 📈 Volatility (CLICK SYNC)
@app.callback(
    Output("volatility", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_volatility(clickData, dropdown_symbol):
    symbol = get_symbol_from_click(clickData, dropdown_symbol)

    if not symbol:
        return go.Figure()

    return create_volatility_chart(df, symbol)


# 📊 Histogram (CLICK SYNC)
@app.callback(
    Output("histogram", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_histogram(clickData, dropdown_symbol):
    symbol = get_symbol_from_click(clickData, dropdown_symbol)

    if not symbol:
        return go.Figure()

    return create_returns_histogram(df, symbol)


# 🔥 Sync dropdown with click (VERY IMPORTANT UX)
@app.callback(
    Output("symbol-dropdown", "value"),
    Input("scatter", "clickData"),
    prevent_initial_call=True
)
def sync_dropdown(clickData):
    if clickData:
        return clickData["points"][0]["hovertext"]


# 📊 Heatmap
def get_top_corr(corr_matrix, n=30):
    avg = corr_matrix.abs().mean()
    top = avg.sort_values(ascending=False).head(n).index
    return corr_matrix.loc[top, top]


@app.callback(
    Output("heatmap", "figure"),
    Input("symbol-dropdown", "value")
)
def update_heatmap(_):
    reduced = get_top_corr(corr_matrix)
    return create_correlation_heatmap(reduced)


# -----------------------
# RUN SERVER
# -----------------------
server = app.server

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)