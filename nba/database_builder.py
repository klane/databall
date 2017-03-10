from nba_py.league import GameLog, PlayerStats, TeamStats
from nba_py.team import TeamDetails, TeamList
import sqlite3
import time


def add_player_game_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' player game stats'
        table = GameLog(season=season_str(season), player_or_team='P').overall()
        table.drop(labels_to_drop(table.columns, ['ABBREV', 'NAME', 'SEASON', 'VIDEO']), axis=1, inplace=True)
        table['SEASON'] = season

        if season == start_season:
            table.to_sql('player_game_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('player_game_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)


def add_player_season_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' player season stats'
        table = PlayerStats(season=season_str(season)).overall()
        table.drop(labels_to_drop(table.columns, ['ABBREV', 'CF', 'NAME', 'RANK']), axis=1, inplace=True)
        table['SEASON'] = season

        if season == start_season:
            table.to_sql('player_season_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('player_season_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)


def add_teams(conn, sleep=1):
    teams = TeamList().info()[0:30]
    teams['CITY'] = 'TEMP'
    teams['NICKNAME'] = 'TEMP'
    columns = ['CITY', 'NICKNAME']

    for ID in teams.TEAM_ID:
        teams.loc[teams.TEAM_ID == ID, columns] = TeamDetails(ID).background()[columns].values
        time.sleep(sleep)

    teams.drop(labels_to_drop(teams.columns, ['LEAGUE_ID', 'YEAR']), axis=1, inplace=True)
    teams.to_sql('teams', conn, if_exists='replace')


def add_team_game_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' team game stats'
        table = GameLog(season=season_str(season), player_or_team='T').overall()
        table.drop(labels_to_drop(table.columns, ['ABBREV', 'NAME', 'SEASON', 'VIDEO']), axis=1, inplace=True)
        table['SEASON'] = season

        if season == start_season:
            table.to_sql('team_game_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('team_game_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)


def add_team_season_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' team season stats'
        table = TeamStats(season=season_str(season)).overall()
        table.drop(labels_to_drop(table.columns, ['CF', 'NAME', 'RANK']), axis=1, inplace=True)
        table['SEASON'] = season

        if season == start_season:
            table.to_sql('team_season_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('team_season_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)


def build_database(start_season, end_season, if_exists='replace', sleep=1):
    conn = sqlite3.connect('nba.db')
    add_teams(conn, sleep)
    add_player_game_stats(conn, start_season, end_season, if_exists, sleep)
    add_player_season_stats(conn, start_season, end_season, if_exists, sleep)
    add_team_game_stats(conn, start_season, end_season, if_exists, sleep)
    add_team_season_stats(conn, start_season, end_season, if_exists, sleep)
    conn.close()


def labels_to_drop(column_names, list_of_strings):
    return [col for col in column_names if any([x for x in list_of_strings if x in col])]


def season_str(season):
    return str(season) + '-' + str(season+1)[-2:]
