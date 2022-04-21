from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin

from databall.db.base import Base
from databall.db.columns import priority_column


class Teams(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(3), nullable=False, unique=True)


@declarative_mixin
class TeamID:
    @priority_column
    def team_id(cls):
        return Column(ForeignKey(Teams.id), primary_key=True)
