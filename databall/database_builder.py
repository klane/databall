from nba_py.league import GameLog, PlayerStats, TeamStats
from nba_py.team import TeamDetails, TeamList
import pandas as pd
import sqlite3
import time
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams as TEAMS
from nba_api.stats.static import players as PLAYERS
from nba_api.stats.static.teams import find_team_name_by_id
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import teamgamelogs
from nba_api.stats.endpoints import leaguedashteamstats
import json


def add_player_game_stats(conn, start_season, end_season, if_exists='append', sleep=0):
    table_name = 'player_game_stats'

    if if_exists == 'replace':
        conn.execute('DROP TABLE IF EXISTS ' + table_name)
        conn.execute('DROP TABLE IF EXISTS players')

    conn.execute('''CREATE TABLE IF NOT EXISTS {} (PLAYER_ID INTEGER, TEAM_ID INTEGER, GAME_ID TEXT, MIN INTEGER,
        FGM INTEGER, FGA INTEGER, FG3M INTEGER, FG3A INTEGER, FTM INTEGER, FTA INTEGER, OREB INTEGER, DREB INTEGER,
        REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER, TOV INTEGER, PF INTEGER, PTS INTEGER, PLUS_MINUS INTEGER)'''
                 .format(table_name))

    conn.execute('CREATE TABLE IF NOT EXISTS players (ID INTEGER, NAME TEXT)')

    for season in range(start_season, end_season):
        print('Reading ' + season_str(season) + ' player game stats')
        #table = leaguegamefinder.LeagueGameFinder(season_nullable='2019-20').get_data_frames()[0]
        #table = leaguedashplayerstats.LeagueDashPlayerStats(season='2019-20').get_data_frames()[0]
        labels = ['ABBREV', 'DATE', 'MATCHUP', 'PCT', 'SEASON', 'VIDEO', 'WL']
        playerlist = PLAYERS.get_active_players()
        # use the below if you are not querying the current season, using active players cuts down on the API queries
        #playerlist = PLAYERS.get_players()
        playersjson = json.dumps(playerlist)
        players = pd.read_json(playersjson)
        print(players.columns.tolist())
        for playerid in players['id']:
        #table.to_sql('temp', conn, if_exists='append', index=False)
            #print(playergamelog.PlayerGameLog(player_id=playerid).get_request_url())
            #print(playerid)
            if playergamelog.PlayerGameLog(player_id=playerid, timeout=90).get_data_frames()[0].empty == True:
                time.sleep(sleep)
                continue
            else:
                table = playergamelog.PlayerGameLog(player_id=playerid, timeout=90).get_data_frames()[0]
                #players.loc[.id == id, ['full_name']] = TeamDetails(ID).background()[['CITY', 'NICKNAME']].values
                #print(table.columns.tolist())
                table.to_sql('temp', conn, if_exists='append', index=False)
                table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
                #table.dropna(axis=0, how='any', subset=['GAME_ID', 'PLAYER_ID', 'TEAM_ID'], inplace=True)
                table.dropna(axis=0, how='any', subset=['Game_ID', 'Player_ID'], inplace=True)
                table.to_sql(table_name, conn, if_exists='append', index=False)
                time.sleep(sleep)
            time.sleep(sleep)

    query = 'SELECT DISTINCT PLAYER_ID AS ID, PLAYER_NAME AS NAMEFROM temp ORDER BY ID'
    pd.read_sql(query, conn).to_sql('players', conn, if_exists='append', index=False)
    conn.execute('DROP TABLE temp')
    conn.execute('VACUUM')


def add_player_season_stats(conn, start_season, end_season, if_exists='append', sleep=1):
    table_name = 'player_season_stats'

    if if_exists == 'replace':
        conn.execute('DROP TABLE IF EXISTS ' + table_name)
        conn.execute('VACUUM')

    conn.execute('''CREATE TABLE IF NOT EXISTS {} (SEASON INTEGER, PLAYER_ID INTEGER, TEAM_ID INTEGER, AGE REAL,
        GP INTEGER, W INTEGER, L INTEGER, W_PCT REAL, MIN REAL, FGM REAL, FGA REAL, FG_PCT REAL, FG3M REAL, FG3A REAL,
        FG3_PCT REAL, FTM REAL, FTA REAL, FT_PCT REAL, OREB REAL, DREB REAL, REB REAL, AST REAL, TOV REAL, STL REAL,
        BLK REAL, BLKA REAL, PF REAL, PFD REAL, PTS REAL, PLUS_MINUS REAL, DD2 INTEGER, TD3 INTEGER)'''
                 .format(table_name))

    for season in range(start_season, end_season):
        print('Reading ' + season_str(season) + ' player season stats')
        table = leaguedashplayerstats.LeagueDashPlayerStats(season='2019-20').get_data_frames()[0]
        table.drop(labels_to_drop(table.columns, ['ABBREV', 'CF', 'NAME', 'RANK', 'NBA_FANTASY_PTS']), axis=1, inplace=True)
        table.dropna(axis=0, how='any', subset=['PLAYER_ID', 'TEAM_ID'], inplace=True)
        table['SEASON'] = season
        table.to_sql(table_name, conn, if_exists='append', index=False)
        time.sleep(sleep)


def add_teams(conn, sleep=0):
    print('Reading team information')
    conn.execute('DROP TABLE IF EXISTS teams')
    conn.execute('VACUUM')
    conn.execute('CREATE TABLE teams (ID INTEGER, ABBREVIATION TEXT, CITY TEXT, MASCOT TEXT, full_name TEXT, nickname)')
    teamslist=TEAMS.get_teams()[0:30]
    teamsjson=json.dumps(teamslist)
    teams = pd.read_json(teamsjson)
    #teams = TEAMS.get_teams()[0:30]
    #teams.drop(labels_to_drop(teams.columns, ['LEAGUE_ID', 'YEAR']), axis=1, inplace=True)
    teams.drop(labels_to_drop(teams.columns, ['LEAGUE_ID', 'year_founded', 'state']), axis=1, inplace=True)
    teams.rename(columns={'TEAM_ID': 'ID'}, inplace=True)
    teams['CITY'] = 'TEMP'
    teams['MASCOT'] = 'TEMP'

    for ID in teams.id:
        #teams.loc[teams.id == ID, ['CITY', 'MASCOT']] = pd.DataFrame.from_dict([find_team_name_by_id(ID)])[['city', 'nickname']]
        teams.rename(columns={'nickname': 'MASCOT'}, inplace=True)
        time.sleep(sleep)

    teams.to_sql('teams', conn, if_exists='append', index=False)


def add_team_game_stats(conn, start_season, end_season, if_exists='append', sleep=0):
    table_name = 'team_game_stats'

    if if_exists == 'replace':
        conn.execute('DROP TABLE IF EXISTS ' + table_name)
        conn.execute('DROP TABLE IF EXISTS games')

    conn.execute('''CREATE TABLE IF NOT EXISTS {} (TEAM_ID INTEGER, GAME_ID TEXT, MIN INTEGER, FGM INTEGER, FGA INTEGER,
        FG3M INTEGER, FG3A INTEGER, FTM INTEGER, FTA INTEGER, OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER,
        STL INTEGER, BLK INTEGER, TOV INTEGER, PF INTEGER, PTS INTEGER, PLUS_MINUS INTEGER)'''.format(table_name))

    conn.execute('''CREATE TABLE IF NOT EXISTS games (SEASON INTEGER, ID TEXT, HOME_TEAM_ID INTEGER,
        AWAY_TEAM_ID INTEGER, GAME_DATE TEXT, MATCHUP TEXT, HOME_WL TEXT)''')

    for season in range(start_season, end_season):
        print('Reading ' + season_str(season) + ' team game stats')
        table = teamgamelogs.TeamGameLogs(season_nullable='2019-20').get_data_frames()[0]
        table['SEASON'] = season
        #print(table.columns.tolist())
        table.to_sql('temp', conn, if_exists='append', index=False)
        labels = ['ABBREV', 'DATE', 'MATCHUP', 'NAME', 'PCT', 'SEASON', 'VIDEO', 'WL', 'BLKA', 'PFD', 'GP_RANK', 'W_RANK', 'L_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK']
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
        table.dropna(axis=0, how='any', subset=['GAME_ID', 'TEAM_ID'], inplace=True)
        table.to_sql(table_name, conn, if_exists='append', index=False)
        time.sleep(sleep)

    query = '''
    SELECT SEASON,
           ID,
           HOME_TEAM_ID,
           AWAY_TEAM_ID,
           GAME_DATE,
           MATCHUP,
           HOME_WL
    FROM
        (SELECT TEAM_ID AS HOME_TEAM_ID,
                GAME_ID AS ID,
                SEASON,
                GAME_DATE,
                MATCHUP,
                WL AS HOME_WL
            FROM temp
            WHERE MATCHUP LIKE '%vs%') AS home,
        (SELECT TEAM_ID AS AWAY_TEAM_ID,
                GAME_ID
            FROM temp
            WHERE MATCHUP LIKE '%@%') AS away
    WHERE home.ID = away.GAME_ID
    '''
    pd.read_sql(query, conn).to_sql('games', conn, if_exists='append', index=False)
    conn.execute('DROP TABLE temp')
    conn.execute('VACUUM')


def add_team_season_stats(conn, start_season, end_season, if_exists='append', sleep=0):
    table_name = 'team_season_stats'

    if if_exists == 'replace':
        conn.execute('DROP TABLE IF EXISTS ' + table_name)
        conn.execute('VACUUM')

    conn.execute('''CREATE TABLE IF NOT EXISTS {} (SEASON INTEGER, TEAM_ID INTEGER, GP INTEGER, W INTEGER, L INTEGER,
        W_PCT REAL, MIN REAL, FGM REAL, FGA REAL, FG_PCT REAL, FG3M REAL, FG3A REAL, FG3_PCT REAL, FTM REAL, FTA REAL,
        FT_PCT REAL, OREB REAL, DREB REAL, REB REAL, AST REAL, TOV REAL, STL REAL, BLK REAL, BLKA REAL, PF REAL,
        PFD REAL, PTS REAL, PLUS_MINUS REAL)'''.format(table_name))

    for season in range(start_season, end_season):
        print('Reading ' + season_str(season) + ' team season stats')
        table = leaguedashteamstats.LeagueDashTeamStats(season='2019-20').get_data_frames()[0]
        table.drop(labels_to_drop(table.columns, ['CF', 'NAME', 'RANK']), axis=1, inplace=True)
        table.dropna(axis=0, how='any', subset=['TEAM_ID'], inplace=True)
        table['SEASON'] = season
        table.to_sql(table_name, conn, if_exists='append', index=False)
        time.sleep(sleep)


def build_database(database, start_season, end_season, if_exists='replace', sleep=0):
    conn = sqlite3.connect(database)

    if if_exists == 'replace':
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
