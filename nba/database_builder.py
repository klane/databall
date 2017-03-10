from nba_py.league import GameLog, PlayerStats, TeamStats
from nba_py.team import TeamDetails, TeamList
import sqlite3
import time


def add_player_games(conn, season, if_exists='append'):
    table = GameLog(season=season_str(season), player_or_team='P').overall()
    table.drop(labels_to_drop(table.columns, ['ABBREV', 'NAME', 'SEASON', 'VIDEO']), axis=1, inplace=True)
    table['SEASON'] = season
    table.to_sql('player_games', conn, if_exists=if_exists, index=False)


def add_player_stats(conn, season, if_exists='append'):
    table = PlayerStats(season=season_str(season)).overall()
    table.drop(labels_to_drop(table.columns, ['ABBREV', 'CF', 'NAME', 'RANK']), axis=1, inplace=True)
    table['SEASON'] = season
    table.to_sql('player_stats', conn, if_exists=if_exists, index=False)


def add_teams(conn):
    teams = TeamList().info()[0:30]
    teams['CITY'] = 'TEMP'
    teams['NICKNAME'] = 'TEMP'
    columns = ['CITY', 'NICKNAME']

    for ID in teams.TEAM_ID:
        teams.loc[teams.TEAM_ID == ID, columns] = TeamDetails(ID).background()[columns].values
        time.sleep(0.5)

    teams.drop(labels_to_drop(teams.columns, ['LEAGUE_ID', 'YEAR']), axis=1, inplace=True)
    teams.to_sql('teams', conn, if_exists='replace')


def add_team_games(conn, season, if_exists='append'):
    table = GameLog(season=season_str(season), player_or_team='T').overall()
    table.drop(labels_to_drop(table.columns, ['ABBREV', 'NAME', 'SEASON', 'VIDEO']), axis=1, inplace=True)
    table['SEASON'] = season
    table.to_sql('team_games', conn, if_exists=if_exists, index=False)


def add_team_stats(conn, season, if_exists='append'):
    table = TeamStats(season=season_str(season)).overall()
    table.drop(labels_to_drop(table.columns, ['CF', 'NAME', 'RANK']), axis=1, inplace=True)
    table['SEASON'] = season
    table.to_sql('team_stats', conn, if_exists=if_exists, index=False)


def build_database(start_season, end_season):
    conn = sqlite3.connect('nba.db')

    for season in range(start_season, end_season+1):
        print 'Reading ' + season_str(season)

        if season == start_season:
            add_player_games(conn, season, 'replace')
            time.sleep(1)
            add_player_stats(conn, season, 'replace')
            time.sleep(1)
            add_team_games(conn, season, 'replace')
            time.sleep(1)
            add_team_stats(conn, season, 'replace')
            time.sleep(1)
        else:
            add_player_games(conn, season)
            time.sleep(1)
            add_player_stats(conn, season)
            time.sleep(1)
            add_team_games(conn, season)
            time.sleep(1)
            add_team_stats(conn, season)
            time.sleep(1)

    conn.close()


def labels_to_drop(column_names, list_of_strings):
    return [col for col in column_names if any([x for x in list_of_strings if x in col])]


def season_str(season):
    return str(season) + '-' + str(season+1)[-2:]
