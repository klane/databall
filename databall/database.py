import sqlite3
import numpy as np
import pandas as pd
from collections import namedtuple
from itertools import product, starmap
from databall import stats, team_stats


class Database:
    def __init__(self, database):
        self.__conn = sqlite3.connect(database)

        select = '''
            SEASON,
            home.GAME_ID as GAME_ID,
            TEAM_ID,
            TEAM_MIN, TEAM_FGM, TEAM_FGA, TEAM_FG3M, TEAM_FG3A, TEAM_FTM, TEAM_FTA, TEAM_OREB, TEAM_DREB, TEAM_REB,
            TEAM_AST, TEAM_TOV, TEAM_STL, TEAM_BLK, TEAM_PTS, TEAM_PLUS_MINUS,
            OPP_ID,
            OPP_MIN, OPP_FGM, OPP_FGA, OPP_FG3M, OPP_FG3A, OPP_FTM, OPP_FTA, OPP_OREB, OPP_DREB, OPP_REB,
            OPP_AST, OPP_TOV, OPP_STL, OPP_BLK, OPP_PTS, OPP_PLUS_MINUS,
            HOME_WL
        '''

        team_stats_str = '''
            games.SEASON,
            GAME_ID,
            TEAM_ID,
            MIN AS TEAM_MIN,
            FGM AS TEAM_FGM,
            FGA AS TEAM_FGA,
            FG3M AS TEAM_FG3M,
            FG3A AS TEAM_FG3A,
            FTM AS TEAM_FTM,
            FTA AS TEAM_FTA,
            OREB AS TEAM_OREB,
            DREB AS TEAM_DREB,
            REB AS TEAM_REB,
            AST AS TEAM_AST,
            TOV AS TEAM_TOV,
            STL AS TEAM_STL,
            BLK AS TEAM_BLK,
            PTS AS TEAM_PTS,
            PLUS_MINUS AS TEAM_PLUS_MINUS,
            HOME_WL
        '''

        opp_stats_str = '''
            GAME_ID,
            TEAM_ID AS OPP_ID,
            MIN AS OPP_MIN,
            FGM AS OPP_FGM,
            FGA AS OPP_FGA,
            FG3M AS OPP_FG3M,
            FG3A AS OPP_FG3A,
            FTM AS OPP_FTM,
            FTA AS OPP_FTA,
            OREB AS OPP_OREB,
            DREB AS OPP_DREB,
            REB AS OPP_REB,
            AST AS OPP_AST,
            TOV AS OPP_TOV,
            STL AS OPP_STL,
            BLK AS OPP_BLK,
            PTS AS OPP_PTS,
            PLUS_MINUS AS OPP_PLUS_MINUS
        '''

        self.__game_query = '''
            SELECT {0}
            FROM
                (SELECT {1}
                    FROM team_game_stats
                    JOIN games
                    ON TEAM_ID = games.HOME_TEAM_ID AND GAME_ID = games.ID) as home,
                (SELECT {2}
                    FROM team_game_stats
                    JOIN games
                    ON OPP_ID = games.AWAY_TEAM_ID AND GAME_ID = games.ID) as away
            WHERE home.GAME_ID = away.GAME_ID
            UNION
            SELECT {0}
            FROM
                (SELECT {1}
                    FROM team_game_stats
                    JOIN games
                    ON TEAM_ID = games.AWAY_TEAM_ID AND GAME_ID = games.ID) as home,
                (SELECT {2}
                    FROM team_game_stats
                    JOIN games
                    ON OPP_ID = games.HOME_TEAM_ID AND GAME_ID = games.ID) as away
            WHERE home.GAME_ID = away.GAME_ID
        '''.format(select, team_stats_str, opp_stats_str)

    def betting_stats(self, stat_names=None, window=None):
        data = self.game_stats()
        data['PACE'] = team_stats.pace(data)
        data['POSSESSIONS'] = team_stats.possessions(data)
        data['TEAM_OFF_RTG'] = team_stats.off_rating(data)
        data['TEAM_DEF_RTG'] = team_stats.def_rating(data)
        data['TEAM_NET_RTG'] = data['TEAM_OFF_RTG'] - data['TEAM_DEF_RTG']
        data['TEAM_EFG'] = stats.eff_fg_pct(data, 'TEAM_')
        data['TEAM_TOV_PCT'] = stats.tov_pct(data, 'TEAM_')
        data['TEAM_OREB_PCT'] = team_stats.oreb_pct(data)
        data['TEAM_DREB_PCT'] = team_stats.dreb_pct(data)
        data['TEAM_FT_PER_FGA'] = stats.ft_per_fga(data, 'TEAM_')

        efg = data.TEAM_EFG
        oreb = data.TEAM_OREB_PCT
        dreb = data.TEAM_DREB_PCT
        ftr = data.TEAM_FT_PER_FGA
        tov = data.TEAM_TOV_PCT

        data['TEAM_FOUR_FACTORS'] = 0.4 * efg + 0.2 * oreb + 0.15 * ftr - 0.25 * tov
        data['TEAM_FOUR_FACTORS_REB'] = 0.4 * efg + 0.1 * oreb + 0.1 * dreb + 0.15 * ftr - 0.25 * tov

        if stat_names is None:
            stat_names = ['FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK']
            stat_names = ['TEAM_' + s for s in stat_names] + ['OPP_' + s for s in stat_names] +\
                         ['TEAM_OFF_RTG', 'TEAM_DEF_RTG', 'TEAM_NET_RTG', 'TEAM_EFG', 'TEAM_TOV_PCT',
                          'TEAM_OREB_PCT', 'TEAM_DREB_PCT', 'TEAM_FT_PER_FGA', 'TEAM_FOUR_FACTORS',
                          'TEAM_FOUR_FACTORS_REB', 'PACE', 'POSSESSIONS']

        data = data[['SEASON', 'GAME_ID', 'TEAM_ID'] + stat_names]
        data = self.windowed_stats(data, stat_names, window=window)

        games = pd.read_sql('SELECT * FROM games JOIN betting ON games.ID is betting.GAME_ID', self.__conn)
        games = games.merge(data, left_on=['SEASON', 'ID', 'HOME_TEAM_ID'], right_on=['SEASON', 'GAME_ID', 'TEAM_ID'])
        games = games.merge(data, left_on=['SEASON', 'ID', 'AWAY_TEAM_ID'], right_on=['SEASON', 'GAME_ID', 'TEAM_ID'],
                            suffixes=('', '_AWAY'))
        games = games[games.HOME_SPREAD_WL != 'P']

        return games

    def game_stats(self):
        return pd.read_sql(self.__game_query, self.__conn)

    def season_stats(self):
        query = '''
            SELECT SEASON,
                   TEAM_ID,
                   AVG(TEAM_MIN) AS TEAM_MIN,
                   AVG(TEAM_FGM) AS TEAM_FGM,
                   AVG(TEAM_FGA) AS TEAM_FGA,
                   AVG(TEAM_FG3M) AS TEAM_FG3M,
                   AVG(TEAM_FG3A) AS TEAM_FG3A,
                   AVG(TEAM_FTM) AS TEAM_FTM,
                   AVG(TEAM_FTA) AS TEAM_FTA,
                   AVG(TEAM_OREB) AS TEAM_OREB,
                   AVG(TEAM_DREB) AS TEAM_DREB,
                   AVG(TEAM_REB) AS TEAM_REB,
                   AVG(TEAM_AST) AS TEAM_AST,
                   AVG(TEAM_TOV) AS TEAM_TOV,
                   AVG(TEAM_STL) AS TEAM_STL,
                   AVG(TEAM_BLK) AS TEAM_BLK,
                   AVG(TEAM_PTS) AS TEAM_PTS,
                   AVG(TEAM_PLUS_MINUS) AS TEAM_PLUS_MINUS,
                   AVG(OPP_MIN) AS OPP_MIN,
                   AVG(OPP_FGM) AS OPP_FGM,
                   AVG(OPP_FGA) AS OPP_FGA,
                   AVG(OPP_FG3M) AS OPP_FG3M,
                   AVG(OPP_FG3A) AS OPP_FG3A,
                   AVG(OPP_FTM) AS OPP_FTM,
                   AVG(OPP_FTA) AS OPP_FTA,
                   AVG(OPP_OREB) AS OPP_OREB,
                   AVG(OPP_DREB) AS OPP_DREB,
                   AVG(OPP_REB) AS OPP_REB,
                   AVG(OPP_AST) AS OPP_AST,
                   AVG(OPP_TOV) AS OPP_TOV,
                   AVG(OPP_STL) AS OPP_STL,
                   AVG(OPP_BLK) AS OPP_BLK,
                   AVG(OPP_PTS) AS OPP_PTS,
                   AVG(OPP_PLUS_MINUS) AS OPP_PLUS_MINUS
            FROM
                ({})
            GROUP BY SEASON, TEAM_ID
        '''.format(self.__game_query)

        data = pd.read_sql(query, self.__conn)
        data['PACE'] = team_stats.pace(data)
        data['POSSESSIONS'] = team_stats.possessions(data)
        data['TEAM_OFF_RTG'] = team_stats.off_rating(data)
        data['TEAM_DEF_RTG'] = team_stats.def_rating(data)
        data['TEAM_NET_RTG'] = data['TEAM_OFF_RTG'] - data['TEAM_DEF_RTG']
        data['TEAM_EFG'] = stats.eff_fg_pct(data, 'TEAM_')
        data['TEAM_TOV_PCT'] = stats.tov_pct(data, 'TEAM_')
        data['TEAM_OREB_PCT'] = team_stats.oreb_pct(data)
        data['TEAM_DREB_PCT'] = team_stats.dreb_pct(data)
        data['TEAM_FT_PER_FGA'] = stats.ft_per_fga(data, 'TEAM_')

        efg = data.TEAM_EFG
        oreb = data.TEAM_OREB_PCT
        dreb = data.TEAM_DREB_PCT
        ftr = data.TEAM_FT_PER_FGA
        tov = data.TEAM_TOV_PCT

        data['TEAM_FOUR_FACTORS'] = 0.4 * efg + 0.2 * oreb + 0.15 * ftr - 0.25 * tov
        data['TEAM_FOUR_FACTORS_REB'] = 0.4 * efg + 0.1 * oreb + 0.1 * dreb + 0.15 * ftr - 0.25 * tov

        query = '''
            SELECT SEASON, TEAM_ID, OPP_ID, COUNT(OPP_ID) AS GAMES_PLAYED
            FROM
                ({})
            GROUP BY SEASON, TEAM_ID, OPP_ID
        '''.format(self.__game_query)

        opponents = pd.read_sql(query, self.__conn)

        for season in pd.unique(data.SEASON):
            season_opponents = opponents[opponents.SEASON == season]
            teams = pd.unique(season_opponents.TEAM_ID)
            schedule = np.zeros([len(teams), len(teams)])

            for team in teams:
                index = np.array([x in season_opponents[season_opponents.TEAM_ID == team].OPP_ID.values for x in teams])
                schedule[team == teams, index] = season_opponents[season_opponents.TEAM_ID == team].GAMES_PLAYED

            schedule /= sum(season_opponents.GAMES_PLAYED) / len(teams)
            point_diff = data[data.SEASON == season].TEAM_PLUS_MINUS.values
            srs = point_diff

            for i in range(10):
                srs = point_diff + schedule.dot(srs)

            data.loc[data.SEASON == season, 'TEAM_SRS'] = srs

        return data

    # data = DataFrame to average over
    # stat_names = list of stats that should be averaged and shifted
    # window = number of games to average, None indicates all games are used
    # weighted = whether or not recent games are weighted more heavily
    def windowed_stats(self, data, stat_names, window=None, weighted=False):
        data = data.copy()
        seasons = data.SEASON.unique()[1:]
        teams = data.TEAM_ID.unique()
        grouped = data.groupby(['SEASON', 'TEAM_ID'])
        keys = grouped.groups.keys()
        team_season = namedtuple('team_season', ['season', 'team'])

        for group in starmap(team_season, [x for x in product(seasons, teams) if x in keys]):
            g = grouped.get_group(group)
            sub = g[stat_names].expanding().mean()

            if window is not None:
                roll = g[stat_names].rolling(window=window).mean()
                sub = sub[:window - 1].append(roll[window - 1:])

            # Shift stats down one game so only previous information is used
            sub = sub.shift(1)

            # Fill in first game with average of previous season
            previous = (group.season - 1, group.team)

            if previous in keys:
                sub.iloc[0] = grouped.get_group(previous)[stat_names].mean()

            # Store subset in full DataFrame
            data.loc[sub.index, stat_names] = sub

        return data
