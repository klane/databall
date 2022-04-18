from sqlalchemy import Column, ForeignKey, Integer, String

from databall.db.base import Base
from databall.db.tables.team import TEAM_ID

GAME_ID = String(10)


class Games(Base):
    id = Column(GAME_ID, primary_key=True)
    home_team_id = Column(TEAM_ID, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(TEAM_ID, ForeignKey('teams.id'), nullable=False)
    season = Column(Integer)
    game_date = Column(String(10))
    matchup = Column(String(11))
    home_wl = Column(String(1))
