from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr

from databall.db.base import Base
from databall.db.columns import PriorityColumn


class Players(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


@declarative_mixin
class PlayerID:
    @declared_attr
    def player_id(cls):
        return PriorityColumn(ForeignKey(Players.id), primary_key=True)
