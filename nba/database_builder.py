from nba_py.league import GameLog, PlayerStats, TeamStats
from nba_py.team import TeamDetails, TeamList
import pandas as pd
import sqlite3
import time


def add_player_game_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' player game stats'
        table = GameLog(season=season_str(season), player_or_team='P').overall()
        table.to_sql('temp', conn, if_exists='append', index=False)
        labels = ['ABBREV', 'DATE', 'MATCHUP', 'NAME', 'SEASON', 'VIDEO', 'WL']
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)

        if season == start_season:
            table.to_sql('player_game_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('player_game_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)

    query = 'SELECT DISTINCT PLAYER_ID, PLAYER_NAME FROM temp'
    pd.read_sql(query, conn).to_sql('players', conn, if_exists=if_exists, index=False)
    conn.execute('DROP TABLE temp')


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
    print 'Reading team information'
    teams = TeamList().info()[0:30]
    teams['CITY'] = 'TEMP'
    teams['NICKNAME'] = 'TEMP'
    columns = ['CITY', 'NICKNAME']

    for ID in teams.TEAM_ID:
        teams.loc[teams.TEAM_ID == ID, columns] = TeamDetails(ID).background()[columns].values
        time.sleep(sleep)

    teams.drop(labels_to_drop(teams.columns, ['LEAGUE_ID', 'YEAR']), axis=1, inplace=True)
    teams.to_sql('teams', conn, if_exists='replace', index=False)


def add_team_game_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    for season in range(start_season, end_season + 1):
        print 'Reading ' + season_str(season) + ' team game stats'
        table = GameLog(season=season_str(season), player_or_team='T').overall()
        table['SEASON'] = season
        table.to_sql('temp', conn, if_exists='append', index=False)
        labels = ['ABBREV', 'DATE', 'MATCHUP', 'NAME', 'SEASON', 'VIDEO', 'WL']
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)

        if season == start_season:
            table.to_sql('team_game_stats', conn, if_exists=if_exists, index=False)
        else:
            table.to_sql('team_game_stats', conn, if_exists='append', index=False)

        time.sleep(sleep)

    query = '''
    SELECT HOME_GAME_ID AS GAME_ID,
           HOME_TEAM_ID,
           AWAY_TEAM_ID,
           SEASON
           GAME_DATE,
           MATCHUP,
           HOME_WL
    FROM
        (SELECT TEAM_ID AS HOME_TEAM_ID,
                GAME_ID AS HOME_GAME_ID,
                SEASON,
                GAME_DATE,
                MATCHUP,
                WL AS HOME_WL
            FROM temp
            WHERE MATCHUP LIKE '%vs%') AS home,
        (SELECT TEAM_ID AS AWAY_TEAM_ID,
                GAME_ID AS AWAY_GAME_ID
            FROM temp
            WHERE MATCHUP LIKE '%@%') AS away
    WHERE home.HOME_GAME_ID = away.AWAY_GAME_ID
    '''
    pd.read_sql(query, conn).to_sql('games', conn, if_exists=if_exists, index=False)
    conn.execute('DROP TABLE temp')


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


def build_database(database, start_season, end_season, if_exists='replace', sleep=1):
    conn = sqlite3.connect(database)
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
