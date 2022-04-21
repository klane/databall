from sqlalchemy import Column, Float, String

from databall.db import columns
from databall.db.base import Base
from databall.db.tables.game import GameID


class Covers(Base, GameID):
    home_spread = Column(Float(precision=1))
    home_spread_result = Column(String(1))
    over_under = columns.positive_column('over_under', Float(precision=1))
    over_under_result = Column(String(1))
