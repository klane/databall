from enum import Enum

from nba_api.stats.library.parameters import (
    PlayerOrTeamAbbreviation,
    SeasonTypePlayoffs,
)


class GameResult(str, Enum):
    WIN = 'W'
    LOSS = 'L'


class OverUnderResult(str, Enum):
    OVER = 'O'
    UNDER = 'U'
    PUSH = 'P'


class SeasonType(str, Enum):
    REGULAR = SeasonTypePlayoffs.regular
    PLAYOFFS = SeasonTypePlayoffs.playoffs


class SpreadResult(str, Enum):
    WIN = 'W'
    LOSS = 'L'
    PUSH = 'P'


class StatsType(str, Enum):
    PLAYER = PlayerOrTeamAbbreviation.player
    TEAM = PlayerOrTeamAbbreviation.team
