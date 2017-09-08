from IPython.display import display, HTML


def print_df(df):
    display(HTML(df.to_html(index=False)))
