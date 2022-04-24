from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin

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


class PlayerStats(Base, PlayerID, TeamID, GameID, Stats):
    pass


class TeamStats(Base, TeamID, GameID, Stats):
    pass
