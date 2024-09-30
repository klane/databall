import json
import sqlite3
import time

import pandas as pd
from nba_api.stats.endpoints.leaguedashplayerstats import LeagueDashPlayerStats
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats
from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
from nba_api.stats.static import teams as TEAMS


def add_player_game_stats(conn, start_season, end_season, if_exists="append", sleep=1):
    table_name = "player_game_stats"

    if if_exists == "replace":
        conn.execute("DROP TABLE IF EXISTS " + table_name)
        conn.execute("DROP TABLE IF EXISTS players")

    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name} (
            PLAYER_ID INTEGER, TEAM_ID INTEGER, GAME_ID TEXT, MIN INTEGER, FGM INTEGER,
            FGA INTEGER, FG3M INTEGER, FG3A INTEGER, FTM INTEGER, FTA INTEGER,
            OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER,
            BLK INTEGER, TOV INTEGER, PF INTEGER, PTS INTEGER, PLUS_MINUS INTEGER)"""
    )

    conn.execute("CREATE TABLE IF NOT EXISTS players (ID INTEGER, NAME TEXT)")

    for season in range(start_season, end_season + 1):
        print("Reading " + season_str(season) + " player game stats")
        table = LeagueGameLog(
            season=season_str(season), player_or_team_abbreviation="P"
        ).get_data_frames()[0]
        table.to_sql("temp", conn, if_exists="append", index=False)
        labels = ["ABBREV", "DATE", "MATCHUP", "NAME", "PCT", "SEASON", "VIDEO", "WL"]
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
        table.dropna(
            axis=0, how="any", subset=["GAME_ID", "PLAYER_ID", "TEAM_ID"], inplace=True
        )
        table.to_sql(table_name, conn, if_exists="append", index=False)
        time.sleep(sleep)

    query = "SELECT DISTINCT PLAYER_ID AS ID, PLAYER_NAME AS NAME FROM temp ORDER BY ID"
    pd.read_sql(query, conn).to_sql("players", conn, if_exists="append", index=False)
    conn.execute("DROP TABLE temp")
    conn.execute("VACUUM")


def add_player_season_stats(
    conn, start_season, end_season, if_exists="append", sleep=1
):
    table_name = "player_season_stats"

    if if_exists == "replace":
        conn.execute("DROP TABLE IF EXISTS " + table_name)
        conn.execute("VACUUM")

    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name} (
            SEASON INTEGER, PLAYER_ID INTEGER, TEAM_ID INTEGER, AGE REAL, GP INTEGER,
            W INTEGER, L INTEGER, W_PCT REAL, MIN REAL, FGM REAL, FGA REAL, FG_PCT REAL,
            FG3M REAL, FG3A REAL, FG3_PCT REAL, FTM REAL, FTA REAL, FT_PCT REAL,
            OREB REAL, DREB REAL, REB REAL, AST REAL, TOV REAL, STL REAL, BLK REAL,
            BLKA REAL, PF REAL, PFD REAL, PTS REAL, PLUS_MINUS REAL,
            DD2 INTEGER, TD3 INTEGER)"""
    )

    for season in range(start_season, end_season + 1):
        print("Reading " + season_str(season) + " player season stats")
        table = LeagueDashPlayerStats(season=season_str(season)).get_data_frames()[0]
        labels = ["ABBREV", "CF", "NAME", "NBA_FANTASY_PTS", "RANK"]
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
        table.dropna(axis=0, how="any", subset=["PLAYER_ID", "TEAM_ID"], inplace=True)
        table["SEASON"] = season
        table.to_sql(table_name, conn, if_exists="append", index=False)
        time.sleep(sleep)


def add_teams(conn):
    print("Reading team information")
    conn.execute("DROP TABLE IF EXISTS teams")
    conn.execute("VACUUM")
    conn.execute(
        """
        CREATE TABLE teams (
            ID INTEGER, ABBREVIATION TEXT, MASCOT TEXT,
            NAME TEXT, CITY TEXT, STATE TEXT, YEAR INTEGER
        )
        """
    )
    teams = TEAMS.get_teams()
    teams = json.dumps(teams)
    teams = pd.read_json(teams)
    teams.rename(
        columns={"full_name": "NAME", "nickname": "MASCOT", "year_founded": "YEAR"},
        inplace=True,
    )
    teams.to_sql("teams", conn, if_exists="append", index=False)


def add_team_game_stats(conn, start_season, end_season, if_exists="append", sleep=1):
    table_name = "team_game_stats"

    if if_exists == "replace":
        conn.execute("DROP TABLE IF EXISTS " + table_name)
        conn.execute("DROP TABLE IF EXISTS games")

    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            TEAM_ID INTEGER, GAME_ID TEXT, MIN INTEGER, FGM INTEGER, FGA INTEGER,
            FG3M INTEGER, FG3A INTEGER, FTM INTEGER, FTA INTEGER, OREB INTEGER,
            DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER,
            TOV INTEGER, PF INTEGER, PTS INTEGER, PLUS_MINUS INTEGER
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS games (
            SEASON INTEGER, ID TEXT, HOME_TEAM_ID INTEGER, AWAY_TEAM_ID INTEGER,
            GAME_DATE TEXT, MATCHUP TEXT, HOME_WL TEXT
        )
        """
    )

    for season in range(start_season, end_season + 1):
        print("Reading " + season_str(season) + " team game stats")
        table = LeagueGameLog(
            season=season_str(season), player_or_team_abbreviation="T"
        ).get_data_frames()[0]
        table["SEASON"] = season
        table.to_sql("temp", conn, if_exists="append", index=False)
        labels = ["ABBREV", "DATE", "MATCHUP", "NAME", "PCT", "SEASON", "VIDEO", "WL"]
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
        table.dropna(axis=0, how="any", subset=["GAME_ID", "TEAM_ID"], inplace=True)
        table.to_sql(table_name, conn, if_exists="append", index=False)
        time.sleep(sleep)

    query = """
    SELECT
        SEASON,
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
    """
    pd.read_sql(query, conn).to_sql("games", conn, if_exists="append", index=False)
    conn.execute("DROP TABLE temp")
    conn.execute("VACUUM")


def add_team_season_stats(conn, start_season, end_season, if_exists="append", sleep=1):
    table_name = "team_season_stats"

    if if_exists == "replace":
        conn.execute("DROP TABLE IF EXISTS " + table_name)
        conn.execute("VACUUM")

    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            SEASON INTEGER, TEAM_ID INTEGER, GP INTEGER, W INTEGER, L INTEGER,
            W_PCT REAL, MIN REAL, FGM REAL, FGA REAL, FG_PCT REAL, FG3M REAL,
            FG3A REAL, FG3_PCT REAL, FTM REAL, FTA REAL, FT_PCT REAL, OREB REAL,
            DREB REAL, REB REAL, AST REAL, TOV REAL, STL REAL, BLK REAL, BLKA REAL,
            PF REAL, PFD REAL, PTS REAL, PLUS_MINUS REAL
        )
        """
    )

    for season in range(start_season, end_season + 1):
        print("Reading " + season_str(season) + " team season stats")
        table = LeagueDashTeamStats(season=season_str(season)).get_data_frames()[0]
        labels = ["CF", "NAME", "RANK"]
        table.drop(labels_to_drop(table.columns, labels), axis=1, inplace=True)
        table.dropna(axis=0, how="any", subset=["TEAM_ID"], inplace=True)
        table["SEASON"] = season
        table.to_sql(table_name, conn, if_exists="append", index=False)
        time.sleep(sleep)


def build_database(database, start_season, end_season, if_exists="replace", sleep=1):
    conn = sqlite3.connect(database)

    if if_exists == "replace":
        add_teams(conn)

    add_player_game_stats(conn, start_season, end_season, if_exists, sleep)
    add_player_season_stats(conn, start_season, end_season, if_exists, sleep)
    add_team_game_stats(conn, start_season, end_season, if_exists, sleep)
    add_team_season_stats(conn, start_season, end_season, if_exists, sleep)
    conn.close()


def labels_to_drop(column_names, list_of_strings):
    return [
        col for col in column_names if any([x for x in list_of_strings if x in col])
    ]


def season_str(season):
    return str(season) + "-" + str(season + 1)[-2:]
