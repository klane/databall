from sqlalchemy import Column, Integer

from databall.db.base import Base, PositiveColumn, PriorityColumn
from databall.db.tables.game import GameID
from databall.db.tables.player import PlayerID
from databall.db.tables.team import TeamID


class Stats:
    min = PositiveColumn('min', Integer)
    fgm = PositiveColumn('fgm', Integer)
    fga = PositiveColumn('fga', Integer)
    fg3m = PositiveColumn('fg3m', Integer)
    fg3a = PositiveColumn('fg3a', Integer)
    ftm = PositiveColumn('ftm', Integer)
    fta = PositiveColumn('fta', Integer)
    oreb = PositiveColumn('oreb', Integer)
    dreb = PositiveColumn('dreb', Integer)
    reb = PositiveColumn('reb', Integer)
    ast = PositiveColumn('ast', Integer)
    stl = PositiveColumn('stl', Integer)
    blk = PositiveColumn('blk', Integer)
    tov = PositiveColumn('tov', Integer)
    pf = PositiveColumn('pf', Integer)
    pts = PositiveColumn('pts', Integer)
    plus_minus = Column(Integer)


class PlayerStats(Base, Stats):
    player_id = PlayerID(primary_key=True)
    team_id = TeamID(primary_key=True)
    game_id = GameID(primary_key=True)


class TeamStats(Base, Stats):
    team_id = TeamID(primary_key=True)
    game_id = GameID(primary_key=True)
