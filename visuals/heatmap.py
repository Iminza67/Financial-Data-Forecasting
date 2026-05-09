import pandas as pd
import plotly.graph_objects as go


def create_correlation_heatmap(corr_matrix: pd.DataFrame):
    """
    Creates a correlation heatmap for stock returns

    Parameters:
        corr_matrix (pd.DataFrame): Correlation matrix (symbol x symbol)

    Returns:
        fig (go.Figure): Plotly heatmap figure
    """

    # --- Safety checks ---
    if corr_matrix is None or corr_matrix.empty:
        raise ValueError("Correlation matrix is empty.")

    # --- Ensure correct format ---
    if not isinstance(corr_matrix, pd.DataFrame):
        raise TypeError("corr_matrix must be a pandas DataFrame.")

    # --- Create heatmap ---
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation"),
            hovertemplate=(
                "Stock 1: %{y}<br>"
                "Stock 2: %{x}<br>"
                "Correlation: %{z:.2f}<extra></extra>"
            )
        )
    )

    # --- Layout improvements ---
    fig.update_layout(
        title="Correlation Heatmap (Stock Returns)",
        template="plotly_white",
        height=700,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Stocks",
        yaxis_title="Stocks"
    )

    return fig