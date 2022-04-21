from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin

from databall.db.base import Base
from databall.db.columns import priority_column


class Players(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


@declarative_mixin
class PlayerID:
    @priority_column
    def player_id(cls):
        return Column(ForeignKey(Players.id), primary_key=True)
