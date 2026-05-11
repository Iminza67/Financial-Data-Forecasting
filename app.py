from dash import Dash, dcc, html, Input, Output
import plotly.io as pio
import plotly.graph_objs as go

from preprocessing.pipeline import run_pipeline
from functools import lru_cache

from visuals.scatter import create_scatter_plot
from visuals.candlestick import create_candlestick_chart
from visuals.histogram import create_returns_histogram
from visuals.volatility import create_volatility_chart
from visuals.volume import create_volume_chart

pio.renderers.default = "browser"

# ---------------------------------------------------
# LOAD DATA ONCE
# ---------------------------------------------------
@lru_cache(maxsize=1)
def get_data():
    return run_pipeline()


df, sharpe_df, company_df = get_data()

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------
df["symbol"] = (
    df["symbol"]
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

sharpe_df["symbol"] = (
    sharpe_df["symbol"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ---------------------------------------------------
# KEEP ONLY SYMBOLS WITH FULL DATA
# ---------------------------------------------------
required_cols = [
    "open",
    "high",
    "low",
    "close",
    "volume"
]

valid_symbols = (
    df
    .dropna(subset=required_cols)
    .groupby("symbol")
    .filter(lambda x: len(x) > 20)["symbol"]
    .unique()
)

df = df[df["symbol"].isin(valid_symbols)]
company_df = company_df[
    company_df["symbol"].isin(valid_symbols)
]
sharpe_df = sharpe_df[
    sharpe_df["symbol"].isin(valid_symbols)
]

symbols = sorted(valid_symbols)

# ---------------------------------------------------
# REDUCE MEMORY USAGE
# ---------------------------------------------------
for col in ["open", "high", "low", "close", "volume"]:
    if col in df.columns:
        df[col] = df[col].astype("float32")

df["symbol"] = df["symbol"].astype("category")

# ---------------------------------------------------
# HELPER
# ---------------------------------------------------
def get_symbol_from_click(clickData, fallback_symbol):

    if clickData and "points" in clickData:
        point = clickData["points"][0]

        if "hovertext" in point:
            return point["hovertext"]

        if "text" in point:
            return point["text"]

        if "x" in point:
            return point["x"]

    return fallback_symbol


# ---------------------------------------------------
# DASH APP
# ---------------------------------------------------
app = Dash(__name__)

app.layout = html.Div([

    html.H1(
        "S&P 500 Risk-Return Dashboard",
        style={
            "textAlign": "center",
            "marginBottom": "20px"
        }
    ),

    html.Div([

        html.Div([

            html.Label("Stock"),

            dcc.Dropdown(
                id="symbol-dropdown",
                options=[
                    {"label": s, "value": s}
                    for s in symbols
                ],
                value=symbols[0] if symbols else None,
                clearable=False
            )

        ], style={"width": "48%"}),

        html.Div([

            html.Label("Sector"),

            dcc.Dropdown(
                id="sector-dropdown",
                options=[
                    {"label": s, "value": s}
                    for s in sorted(
                        company_df["sector"]
                        .dropna()
                        .unique()
                    )
                ],
                value=None,
                placeholder="Select sector"
            )

        ], style={"width": "48%"})

    ], style={
        "display": "flex",
        "justifyContent": "space-between"
    }),

    dcc.Graph(id="scatter"),

    html.Div([

        dcc.Graph(id="candlestick"),

        dcc.Graph(id="volume")

    ], style={"display": "flex"}),

    html.Div([

        dcc.Graph(id="volatility"),

        dcc.Graph(id="histogram")

    ], style={"display": "flex"})

])

# ---------------------------------------------------
# SCATTER
# ---------------------------------------------------
@app.callback(
    Output("scatter", "figure"),
    Input("sector-dropdown", "value"),
    Input("symbol-dropdown", "value")
)
def update_scatter(sector, selected_symbol):

    filtered_df = df

    if sector:

        sector_symbols = company_df[
            company_df["sector"] == sector
        ]["symbol"]

        filtered_df = filtered_df[
            filtered_df["symbol"].isin(sector_symbols)
        ]

    scatter_df = (
        filtered_df
        .groupby("symbol")
        .agg({
            "return": "mean"
        })
        .reset_index()
    )

    scatter_df = scatter_df.merge(
        sharpe_df,
        on="symbol",
        how="inner"
    )

    if scatter_df.empty:

        fig = go.Figure()

        fig.update_layout(
            title="No data available"
        )

        return fig

    fig = create_scatter_plot(
        scatter_df,
        company_df
    )

    # Highlight selected stock
    if selected_symbol in scatter_df["symbol"].values:

        selected = scatter_df[
            scatter_df["symbol"] == selected_symbol
        ]

        fig.add_scatter(
            x=selected["std"],
            y=selected["mean"],
            mode="markers",
            marker=dict(
                size=14,
                color="red"
            ),
            name="Selected Stock"
        )

    return fig


# ---------------------------------------------------
# CANDLESTICK
# ---------------------------------------------------
@app.callback(
    Output("candlestick", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_candlestick(clickData, dropdown_symbol):

    symbol = get_symbol_from_click(
        clickData,
        dropdown_symbol
    )

    if symbol not in valid_symbols:
        return go.Figure()

    return create_candlestick_chart(df, symbol)


# ---------------------------------------------------
# VOLUME
# ---------------------------------------------------
@app.callback(
    Output("volume", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_volume(clickData, dropdown_symbol):

    symbol = get_symbol_from_click(
        clickData,
        dropdown_symbol
    )

    if symbol not in valid_symbols:
        return go.Figure()

    return create_volume_chart(df, symbol)


# ---------------------------------------------------
# VOLATILITY
# ---------------------------------------------------
@app.callback(
    Output("volatility", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_volatility(clickData, dropdown_symbol):

    symbol = get_symbol_from_click(
        clickData,
        dropdown_symbol
    )

    if symbol not in valid_symbols:
        return go.Figure()

    return create_volatility_chart(df, symbol)


# ---------------------------------------------------
# HISTOGRAM
# ---------------------------------------------------
@app.callback(
    Output("histogram", "figure"),
    Input("scatter", "clickData"),
    Input("symbol-dropdown", "value")
)
def update_histogram(clickData, dropdown_symbol):

    symbol = get_symbol_from_click(
        clickData,
        dropdown_symbol
    )

    if symbol not in valid_symbols:
        return go.Figure()

    return create_returns_histogram(df, symbol)


# ---------------------------------------------------
# SYNC DROPDOWN
# ---------------------------------------------------
@app.callback(
    Output("symbol-dropdown", "value"),
    Input("scatter", "clickData"),
    prevent_initial_call=True
)
def sync_dropdown(clickData):

    if clickData and "points" in clickData:

        point = clickData["points"][0]

        if "hovertext" in point:
            return point["hovertext"]

        if "text" in point:
            return point["text"]

        if "x" in point:
            return point["x"]

    return symbols[0]


# ---------------------------------------------------
# RUN SERVER
# ---------------------------------------------------
server = app.server

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        port=8050
    )