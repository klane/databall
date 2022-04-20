from sqlalchemy import Column, Float, String

from databall.db.base import Base, PositiveColumn
from databall.db.tables.game import GameID


class Covers(Base):
    game_id = GameID(primary_key=True)
    home_spread = Column(Float(precision=1))
    home_spread_result = Column(String(1))
    over_under = PositiveColumn('over_under', Float(precision=1))
    over_under_result = Column(String(1))
