from IPython.display import display, HTML


def print_df(df):
    display(HTML(df.to_html(index=False)))


def select_columns(data, attributes, columns):
    return data[:, [index for index, col in enumerate(columns) if any(name in col for name in attributes)]]
