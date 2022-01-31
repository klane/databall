from databall.team_stats import possessions


def ast_pct(data):
    return data.AST / ((data.MIN / (data.TEAM_MIN / 5) * data.TEAM_FGM) - data.FGM)


def blk_pct(data):
    return data.BLK * (data.TEAM_MIN / 5) / (data.MIN * (data.OPP_FGA - data.OPP_FG3A))


def dreb_pct(data):
    return (
        data.DREB * (data.TEAM_MIN / 5) / (data.MIN * (data.TEAM_DREB + data.OPP_OREB))
    )


def game_score(data):
    return (
        data.PTS
        + 0.4 * data.FGM
        - 0.7 * data.FGA
        - 0.4 * (data.FTA - data.FTM)
        + 0.7 * data.OREB
        + 0.3 * data.DREB
        + data.STL
        + 0.7 * data.AST
        + 0.7 * data.BLK
        - 0.4 * data.PF
        - data.TOV
    )


def oreb_pct(data):
    return (
        data.OREB * (data.TEAM_MIN / 5) / (data.MIN * (data.TEAM_OREB + data.OPP_DREB))
    )


def reb_pct(data):
    return data.REB * (data.TEAM_MIN / 5) / (data.MIN * (data.TEAM_REB + data.OPP_REB))


def stl_pct(data):
    return data.STL * (data.TEAM_MIN / 5) / (data.MIN * possessions(data))


def usg_pct(data):
    return (
        (data.FGA + 0.44 * data.FTA + data.TOV)
        * (data.TEAM_MIN / 5)
        / (data.MIN * (data.TEAM_FGA + 0.44 * data.TEAM_FTA + data.TEAM_TOV))
    )


def def_rating(data):
    poss = possessions(data)
    dor_pct = data.OPP_OREB / (data.OPP_OREB + data.REB)
    dfg_pct = data.OPP_FGM / data.OPP_FGA
    fm_wt = (dfg_pct * (1 - dor_pct)) / (
        dfg_pct * (1 - dor_pct) + (1 - dfg_pct) * dor_pct
    )
    stops1 = (
        data.STL + data.BLK + fm_wt * (1 - 1.07 * dor_pct) + data.DREB * (1 - fm_wt)
    )
    stops2 = (
        ((data.OPP_FGA - data.OPP_FGM - data.BLK) / data.TEAM_MIN)
        * fm_wt
        * (1 - 1.07 * dor_pct)
        + ((data.OPP_TOV - data.STL) / data.TEAM_MIN)
    ) * data.MIN + (data.PF / data.TEAM_PF) * 0.4 * data.OPP_FTA * (
        1 - (data.OPP_FTM / data.OPP_FTA)
    ) ** 2
    stops = stops1 + stops2
    stop_pct = (stops * data.OPP_MIN) / (poss * data.MIN)
    team_def_rating = 100 * (data.OPP_PTS / poss)
    d_pts_per_sc_poss = data.OPP_PTS / (
        data.OPP_FGM
        + (1 - (1 - (data.OPP_FTM / data.OPP_FTA)) ** 2) * 0.4 * data.OPP_FTA
    )
    return team_def_rating + 0.2 * (
        100 * d_pts_per_sc_poss * (1 - stop_pct) - team_def_rating
    )


def off_rating(data):
    q_ast = data.MIN / (data.TEAM_MIN / 5) * 1.14 * (
        data.TEAM_AST - data.AST
    ) / data.TEAM_FGM + (
        ((data.TEAM_AST / data.TEAM_MIN) * data.MIN * 5 - data.AST)
        / ((data.TEAM_FGM / data.TEAM_MIN) * data.MIN * 5 - data.FGM)
    ) * (
        1 - data.MIN / (data.TEAM_MIN / 5)
    )
    team_oreb_pct = data.TEAM_OREB / (data.TEAM_OREB + data.OPP_REB - data.OPP_OREB)
    team_scoring_poss = (
        data.TEAM_FGM
        + (1 - (1 - (data.TEAM_FTM / data.TEAM_FTA)) ** 2) * 0.4 * data.TEAM_FTA
    )
    team_play_pct = team_scoring_poss / (
        data.TEAM_FGA + 0.4 * data.TEAM_FTA + data.TEAM_TOV
    )
    team_oreb_weight = ((1 - team_oreb_pct) * team_play_pct) / (
        (1 - team_oreb_pct) * team_play_pct + team_oreb_pct * (1 - team_play_pct)
    )
    fg_part = data.FGM * (1 - 0.5 * ((data.PTS - data.FTM) / (2 * data.FGA)) * q_ast)
    ast_part = (
        0.5
        * (
            ((data.TEAM_PTS - data.TEAM_FTM) - (data.PTS - data.FTM))
            / (2 * (data.TEAM_FGA - data.FGA))
        )
        * data.AST
    )
    ft_part = (1 - (1 - (data.FTM / data.FTA)) ** 2) * 0.4 * data.FTA
    oreb_part = data.OREB * team_oreb_weight * team_play_pct
    sc_poss = (fg_part + ast_part + ft_part) * (
        1 - (data.TEAM_OREB / team_scoring_poss) * team_oreb_weight * team_play_pct
    ) + oreb_part
    fg_xposs = (data.FGA - data.FGM) * (1 - 1.07 * team_oreb_pct)
    ft_xposs = ((1 - (data.FTM / data.FTA)) ** 2) * 0.4 * data.FTA
    tot_poss = sc_poss + fg_xposs + ft_xposs + data.TOV
    pprod_fg = (
        2
        * (data.FGM + 0.5 * data.FG3M)
        * (1 - 0.5 * ((data.PTS - data.FTM) / (2 * data.FGA)) * q_ast)
    )
    pprod_ast = (
        2
        * (
            (data.TEAM_FGM - data.FGM + 0.5 * (data.TEAM_FG3M - data.FG3M))
            / (data.TEAM_FGM - data.FGM)
        )
        * 0.5
        * (
            (data.TEAM_PTS - data.TEAM_FTM - (data.PTS - data.FTM))
            / (2 * (data.TEAM_FGA - data.FGA))
        )
        * data.AST
    )
    pprod_oreb = (
        data.OREB
        * team_oreb_weight
        * team_play_pct
        * (
            data.TEAM_PTS
            / (
                data.TEAM_FGM
                + (1 - (1 - data.TEAM_FTM / data.TEAM_FTA) ** 2) * 0.4 * data.TEAM_FTA
            )
        )
    )
    pprod = (pprod_fg + pprod_ast + data.FTM) * (
        1 - (data.TEAM_OREB / team_scoring_poss) * team_oreb_weight * team_play_pct
    ) + pprod_oreb
    return 100 * pprod / tot_poss


def pts_produced(data):
    q_ast = data.MIN / (data.TEAM_MIN / 5) * 1.14 * (
        data.TEAM_AST - data.AST
    ) / data.TEAM_FGM + (
        ((data.TEAM_AST / data.TEAM_MIN) * data.MIN * 5 - data.AST)
        / ((data.TEAM_FGM / data.TEAM_MIN) * data.MIN * 5 - data.FGM)
    ) * (
        1 - data.MIN / (data.TEAM_MIN / 5)
    )
    team_oreb_pct = data.TEAM_OREB / (data.TEAM_OREB + data.OPP_REB - data.OPP_OREB)
    team_scoring_poss = (
        data.TEAM_FGM
        + (1 - (1 - (data.TEAM_FTM / data.TEAM_FTA)) ** 2) * 0.4 * data.TEAM_FTA
    )
    team_play_pct = team_scoring_poss / (
        data.TEAM_FGA + 0.4 * data.TEAM_FTA + data.TEAM_TOV
    )
    team_oreb_weight = ((1 - team_oreb_pct) * team_play_pct) / (
        (1 - team_oreb_pct) * team_play_pct + team_oreb_pct * (1 - team_play_pct)
    )
    pprod_fg = (
        2
        * (data.FGM + 0.5 * data.FG3M)
        * (1 - 0.5 * ((data.PTS - data.FTM) / (2 * data.FGA)) * q_ast)
    )
    pprod_ast = (
        2
        * (
            (data.TEAM_FGM - data.FGM + 0.5 * (data.TEAM_FG3M - data.FG3M))
            / (data.TEAM_FGM - data.FGM)
        )
        * 0.5
        * (
            (data.TEAM_PTS - data.TEAM_FTM - (data.PTS - data.FTM))
            / (2 * (data.TEAM_FGA - data.FGA))
        )
        * data.AST
    )
    pprod_oreb = (
        data.OREB
        * team_oreb_weight
        * team_play_pct
        * (
            data.TEAM_PTS
            / (
                data.TEAM_FGM
                + (1 - (1 - data.TEAM_FTM / data.TEAM_FTA) ** 2) * 0.4 * data.TEAM_FTA
            )
        )
    )
    return (pprod_fg + pprod_ast + data.FTM) * (
        1 - (data.TEAM_OREB / team_scoring_poss) * team_oreb_weight * team_play_pct
    ) + pprod_oreb
