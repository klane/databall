from sqlalchemy import Column, Integer, String

from databall.db.base import Base, ForeignID
from databall.db.tables.team import TeamID


class Games(Base):
    id = Column(String(10), primary_key=True)
    home_team_id = TeamID(nullable=False)
    away_team_id = TeamID(nullable=False)
    season = Column(Integer)
    game_date = Column(String(10))
    matchup = Column(String(11))
    home_wl = Column(String(1))


class GameID(ForeignID):
    __table__ = Games
    inherit_cache = True
