def eff_fg_pct(data, group=''):
    return (data[group + 'FGM'] + 0.5 * data[group + 'FG3M']) / data[group + 'FGA']


def fg_pct(data, group=''):
    return data[group + 'FGM'] / data[group + 'FGA']


def fg2a(data, group=''):
    return data[group + 'FGA'] - data[group + 'FG3A']


def fg2m(data, group=''):
    return data[group + 'FGM'] - data[group + 'FG3M']


def fg2_pct(data, group=''):
    return fg2m(data, group) / fg2a(data, group)


def fg3_pct(data, group=''):
    return data[group + 'FG3M'] / data[group + 'FG3A']


def fg3a_rate(data, group=''):
    return data[group + 'FG3A'] / data[group + 'FGA']


def ft_pct(data, group=''):
    return data[group + 'FTM'] / data[group + 'FTA']


def ft_per_fga(data, group=''):
    return data[group + 'FTM'] / data[group + 'FGA']


def ft_rate(data, group=''):
    return data[group + 'FTA'] / data[group + 'FGA']


def tov_pct(data, group=''):
    return data[group + 'TOV'] / (
        data[group + 'FGA'] + 0.44 * data[group + 'FTA'] + data[group + 'TOV']
    )


def ts_pct(data, group=''):
    return data[group + 'PTS'] / (
        2 * (data[group + 'FGA'] + 0.44 * data[group + 'FTA'])
    )
