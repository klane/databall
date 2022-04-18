from sqlalchemy import Column, ForeignKey, Integer

from databall.db.base import Base, PositiveColumn, PriorityColumn
from databall.db.tables.game import GAME_ID
from databall.db.tables.player import PLAYER_ID
from databall.db.tables.team import TEAM_ID


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
    player_id = PriorityColumn(1, PLAYER_ID, ForeignKey('players.id'), primary_key=True)
    team_id = PriorityColumn(2, TEAM_ID, ForeignKey('teams.id'), primary_key=True)
    game_id = PriorityColumn(3, GAME_ID, ForeignKey('games.id'), primary_key=True)


class TeamStats(Base, Stats):
    team_id = PriorityColumn(1, TEAM_ID, ForeignKey('teams.id'), primary_key=True)
    game_id = PriorityColumn(2, GAME_ID, ForeignKey('games.id'), primary_key=True)
