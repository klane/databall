from enum import Enum
from functools import cache

import pandas as pd
from nba_api.stats.endpoints import CommonAllPlayers, LeagueGameLog
from nba_api.stats.library.parameters import (
    PlayerOrTeamAbbreviation,
    SeasonTypePlayoffs,
)
from nba_api.stats.static.teams import get_teams as get_teams_static


class SeasonType(str, Enum):
    REGULAR = SeasonTypePlayoffs.regular
    PLAYOFFS = SeasonTypePlayoffs.playoffs


class StatsType(str, Enum):
    PLAYER = PlayerOrTeamAbbreviation.player
    TEAM = PlayerOrTeamAbbreviation.team


@cache
def _get_stats(season, season_type, stats_type, **kwargs):
    season_str = f'{season} {season_type.value.lower()}'
    print(f'Downloading {season_str} {stats_type.name.lower()} stats')
    stats = LeagueGameLog(
        season=season,
        season_type_all_star=season_type.value,
        player_or_team_abbreviation=stats_type.value,
        **kwargs,
    )
    stats = stats.get_data_frames()[0]
    stats.columns = stats.columns.str.lower()
    return stats


def get_players(**kwargs):
    print('Downloading players')
    players = CommonAllPlayers(**kwargs).get_data_frames()[0]
    players.columns = players.columns.str.lower()
    return players


def get_player_stats(season, season_type=SeasonType.REGULAR, **kwargs):
    return _get_stats(season, season_type, StatsType.PLAYER, **kwargs)


def get_teams():
    print('Downloading teams')
    return pd.DataFrame(get_teams_static())


def get_team_stats(season, season_type=SeasonType.REGULAR, **kwargs):
    return _get_stats(season, season_type, StatsType.TEAM, **kwargs)
