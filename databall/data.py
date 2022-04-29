from enum import Enum
from functools import cache

import pandas as pd
from nba_api.stats.endpoints import CommonAllPlayers, LeagueGameLog
from nba_api.stats.library.parameters import PlayerOrTeamAbbreviation
from nba_api.stats.static.teams import get_teams as get_teams_static


class StatsType(Enum):
    PLAYER = PlayerOrTeamAbbreviation.player
    TEAM = PlayerOrTeamAbbreviation.team


def get_games(season, **kwargs):
    team_stats = get_team_stats(season, **kwargs)
    away_index = team_stats.MATCHUP.str.contains('@')

    home = team_stats[~away_index].copy()
    home.rename(
        columns={'GAME_ID': 'ID', 'TEAM_ID': 'HOME_TEAM_ID', 'WL': 'HOME_WL'},
        inplace=True,
    )

    away = team_stats[away_index].copy()
    away.rename(columns={'GAME_ID': 'ID', 'TEAM_ID': 'AWAY_TEAM_ID'}, inplace=True)

    games = home.merge(away[['ID', 'AWAY_TEAM_ID']], on='ID')
    games['SEASON'] = games.SEASON_ID.apply(lambda season: int(season[1:]))

    return games


def get_players(**kwargs):
    print('Downloading players')
    players = CommonAllPlayers(**kwargs).get_data_frames()[0]
    players.rename(
        columns={'PERSON_ID': 'ID', 'DISPLAY_FIRST_LAST': 'NAME'},
        inplace=True,
    )
    return players


def get_player_stats(season, **kwargs):
    return get_stats(season, StatsType.PLAYER, **kwargs)


@cache
def get_stats(season, stats_type, **kwargs):
    print(f'Downloading {season} {stats_type.name.lower()} stats')
    stats = LeagueGameLog(
        season=season, player_or_team_abbreviation=stats_type.value, **kwargs
    )
    return stats.get_data_frames()[0]


def get_teams():
    print('Downloading teams')
    teams = pd.DataFrame(get_teams_static())
    teams.rename(columns={'full_name': 'name'}, inplace=True)
    teams.columns = teams.columns.str.upper()
    return teams


def get_team_stats(season, **kwargs):
    return get_stats(season, StatsType.TEAM, **kwargs)
