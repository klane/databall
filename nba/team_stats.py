def ast_pct(data):
    return data.TEAM_AST / data.TEAM_FGM


def blk_pct(data):
    return data.TEAM_BLK / (data.OPP_FGA - data.OPP_FG3A)


def def_rating(data):
    return 100 * data.OPP_PTS / possessions(data)


def dreb_pct(data):
    return data.TEAM_DREB / (data.TEAM_DREB + data.OPP_OREB)


def off_rating(data):
    return 100 * data.TEAM_PTS / possessions(data)


def oreb_pct(data):
    return data.TEAM_OREB / (data.TEAM_OREB + data.OPP_DREB)


def pace(data):
    min_per_game = 240
    min_played = data.TEAM_MIN

    if min_played[0] < min_per_game:
        min_played *= 5

    return possessions(data) / min_played * min_per_game


def possessions(data):
    return (data.TEAM_FGA + 0.4 * data.TEAM_FTA + data.TEAM_TOV -
            1.07 * (data.TEAM_OREB / (data.TEAM_OREB + data.OPP_DREB)) * (data.TEAM_FGA - data.TEAM_FGM) +
            data.OPP_FGA + 0.4 * data.OPP_FTA + data.OPP_TOV -
            1.07 * (data.OPP_OREB / (data.OPP_OREB + data.TEAM_DREB)) * (data.OPP_FGA - data.OPP_FGM)) / 2


def reb_pct(data):
    return data.TEAM_REB / (data.TEAM_REB + data.OPP_REB)


def stl_pct(data):
    return data.TEAM_STL / possessions(data)
