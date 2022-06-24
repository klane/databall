from sqlmodel import Field

from databall.api import get_player_stats, get_team_stats
from databall.db.base import Base
from databall.db.columns import PositiveField
from databall.db.tables.game import GameID
from databall.db.tables.player import PlayerID
from databall.db.tables.team import TeamID


class Stats(Base):
    min: int = PositiveField('min')
    fgm: int = PositiveField('fgm')
    fga: int = PositiveField('fga')
    fg3m: int = PositiveField('fg3m')
    fg3a: int = PositiveField('fg3a')
    ftm: int = PositiveField('ftm')
    fta: int = PositiveField('fta')
    oreb: int = PositiveField('oreb')
    dreb: int = PositiveField('dreb')
    reb: int = PositiveField('reb')
    ast: int = PositiveField('ast')
    stl: int = PositiveField('stl')
    blk: int = PositiveField('blk')
    tov: int = PositiveField('tov')
    pf: int = PositiveField('pf')
    pts: int = PositiveField('pts')
    plus_minus: int = Field(nullable=False)

    @classmethod
    def populate(cls, season, season_type, **kwargs):
        stats = cls.get_stats(season, season_type, **kwargs)
        cls.save_df(stats)


class PlayerStats(Stats, GameID, TeamID, PlayerID, table=True):
    get_stats = get_player_stats


class TeamStats(Stats, GameID, TeamID, table=True):
    get_stats = get_team_stats
