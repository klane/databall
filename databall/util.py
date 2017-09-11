from IPython.display import display, HTML


def print_df(df):
    display(HTML(df.to_html(index=False)))


def select_columns(df, attributes):
    return df[:, [index for index, column in enumerate(df.columns) if any(name in column for name in attributes)]]
