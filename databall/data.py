from enum import Enum
from functools import cache

import pandas as pd
from nba_api.stats.endpoints import CommonAllPlayers, LeagueGameLog
from nba_api.stats.library.parameters import (
    PlayerOrTeamAbbreviation,
    SeasonTypePlayoffs,
)
from nba_api.stats.static.teams import get_teams as get_teams_static


class SeasonType(Enum):
    REGULAR = SeasonTypePlayoffs.regular
    PLAYOFFS = SeasonTypePlayoffs.playoffs


class StatsType(Enum):
    PLAYER = PlayerOrTeamAbbreviation.player
    TEAM = PlayerOrTeamAbbreviation.team


def get_games(season, season_type, **kwargs):
    team_stats = get_team_stats(season, season_type, **kwargs)
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


def get_player_stats(season, season_type, **kwargs):
    return get_stats(season, season_type, StatsType.PLAYER, **kwargs)


@cache
def get_stats(season, season_type, stats_type, **kwargs):
    season_str = f'{season} {season_type.value.lower()}'
    print(f'Downloading {season_str} {stats_type.name.lower()} stats')
    stats = LeagueGameLog(
        season=season,
        season_type_all_star=season_type.value,
        player_or_team_abbreviation=stats_type.value,
        **kwargs,
    )
    stats = stats.get_data_frames()[0]
    stats['SEASON_TYPE'] = season_type.name
    return stats


def get_teams():
    print('Downloading teams')
    teams = pd.DataFrame(get_teams_static())
    teams.rename(columns={'full_name': 'name'}, inplace=True)
    teams.columns = teams.columns.str.upper()
    return teams


def get_team_stats(season, season_type, **kwargs):
    return get_stats(season, season_type, StatsType.TEAM, **kwargs)
