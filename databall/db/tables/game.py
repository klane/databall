from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin

from databall.db.base import Base
from databall.db.columns import priority_column
from databall.db.tables.team import Teams


class Games(Base):
    id = Column(String(10), primary_key=True)
    home_team_id = Column(ForeignKey(Teams.id), nullable=False)
    away_team_id = Column(ForeignKey(Teams.id), nullable=False)
    season = Column(Integer)
    game_date = Column(String(10))
    matchup = Column(String(11))
    home_wl = Column(String(1))


@declarative_mixin
class GameID:
    @priority_column
    def game_id(cls):
        return Column(ForeignKey(Games.id), primary_key=True)
