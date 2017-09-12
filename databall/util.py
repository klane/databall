from IPython.display import display, HTML


def print_df(df):
    display(HTML(df.to_html(index=False)))


def select_columns(data, attributes, columns):
    return data[:, [index for index, col in enumerate(columns) if any(name in col for name in attributes)]]


def stat_names():
    basic = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK']
    advanced = ['OFF_RTG', 'DEF_RTG', 'NET_RTG', 'EFG', 'TOV_PCT', 'OREB_PCT', 'DREB_PCT', 'FT_PER_FGA',
                'FOUR_FACTORS', 'FOUR_FACTORS_REB']
    stats = ['TEAM_' + s for s in basic] + ['OPP_' + s for s in basic]
    stats += [s + '_AWAY' for s in stats]
    stats += ['TEAM_' + s for s in advanced] + ['TEAM_' + s + '_AWAY' for s in advanced]
    stats += ['PACE', 'POSSESSIONS', 'PACE_AWAY', 'POSSESSIONS_AWAY', 'HOME_SPREAD']
    return stats
