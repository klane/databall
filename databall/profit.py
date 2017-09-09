import numpy as np


def profit(data, var_predict='HOME_SPREAD_WL', bet_amount=100):
    grouped = data.groupby('GAME_DATE')
    num_games = 0
    days = []
    cumulative_correct = []
    cumulative_percent = []
    cumulative_profit = []
    cumulative_investment = []

    for day in grouped.groups:
        games = grouped.get_group(day)
        num = len(games)
        num_games += num
        days += [day]
        num_correct = sum(games[var_predict] == games[var_predict + '_PRED'])
        daily_profit = bet_amount * num_correct - bet_amount * (num - num_correct)

        if len(cumulative_correct) == 0:
            cumulative_correct += [num_correct]
            cumulative_profit += [daily_profit]
            cumulative_investment += [bet_amount * num]
        else:
            cumulative_correct += [num_correct + cumulative_correct[-1]]
            cumulative_profit += [daily_profit + cumulative_profit[-1]]
            cumulative_investment += [bet_amount * num + cumulative_investment[-1]]

        cumulative_percent += [cumulative_correct[-1] / num_games]

    return days, np.array(cumulative_percent), np.array(cumulative_profit)
