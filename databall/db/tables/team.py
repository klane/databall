from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr

from databall.data import get_teams
from databall.db.base import Base
from databall.db.columns import PriorityColumn


class Teams(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(3), nullable=False, unique=True)

    @classmethod
    def populate(cls):
        teams = get_teams()
        cls.save_df(teams)


@declarative_mixin
class TeamID:
    @declared_attr
    def team_id(cls):
        return PriorityColumn(ForeignKey(Teams.id), primary_key=True)
