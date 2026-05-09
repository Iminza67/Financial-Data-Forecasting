def compute_correlation_matrix(df):
    pivot = df.pivot(index='date', columns='symbol', values='return')

    corr = pivot.corr()

    return corr