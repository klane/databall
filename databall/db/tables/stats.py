from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin

from databall.db import columns
from databall.db.base import Base
from databall.db.tables.game import GameID
from databall.db.tables.player import PlayerID
from databall.db.tables.team import TeamID


@declarative_mixin
class Stats:
    min = columns.positive_column('min', Integer)
    fgm = columns.positive_column('fgm', Integer)
    fga = columns.positive_column('fga', Integer)
    fg3m = columns.positive_column('fg3m', Integer)
    fg3a = columns.positive_column('fg3a', Integer)
    ftm = columns.positive_column('ftm', Integer)
    fta = columns.positive_column('fta', Integer)
    oreb = columns.positive_column('oreb', Integer)
    dreb = columns.positive_column('dreb', Integer)
    reb = columns.positive_column('reb', Integer)
    ast = columns.positive_column('ast', Integer)
    stl = columns.positive_column('stl', Integer)
    blk = columns.positive_column('blk', Integer)
    tov = columns.positive_column('tov', Integer)
    pf = columns.positive_column('pf', Integer)
    pts = columns.positive_column('pts', Integer)
    plus_minus = Column(Integer)


class PlayerStats(Base, PlayerID, TeamID, GameID, Stats):
    pass


class TeamStats(Base, TeamID, GameID, Stats):
    pass
