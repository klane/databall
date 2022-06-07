from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin

from databall.api import get_player_stats, get_team_stats
from databall.db.base import Base
from databall.db.columns import PositiveColumn
from databall.db.tables.game import GameID
from databall.db.tables.player import PlayerID
from databall.db.tables.team import TeamID


@declarative_mixin
class Stats:
    min = PositiveColumn(Integer)
    fgm = PositiveColumn(Integer)
    fga = PositiveColumn(Integer)
    fg3m = PositiveColumn(Integer)
    fg3a = PositiveColumn(Integer)
    ftm = PositiveColumn(Integer)
    fta = PositiveColumn(Integer)
    oreb = PositiveColumn(Integer)
    dreb = PositiveColumn(Integer)
    reb = PositiveColumn(Integer)
    ast = PositiveColumn(Integer)
    stl = PositiveColumn(Integer)
    blk = PositiveColumn(Integer)
    tov = PositiveColumn(Integer)
    pf = PositiveColumn(Integer)
    pts = PositiveColumn(Integer)
    plus_minus = Column(Integer)

    @classmethod
    def populate(cls, season, season_type, **kwargs):
        stats = cls.get_stats(season, season_type, **kwargs)
        cls.save_df(stats)


class PlayerStats(PlayerID, TeamID, GameID, Stats, Base):
    get_stats = get_player_stats


class TeamStats(TeamID, GameID, Stats, Base):
    get_stats = get_team_stats
