import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr

from databall.data import SeasonType, get_games
from databall.db.base import Base
from databall.db.columns import PriorityColumn
from databall.db.tables.team import Teams

WL = enum.Enum('WL', 'W L')


class Games(Base):
    id = Column(String(10), primary_key=True)
    home_team_id = Column(ForeignKey(Teams.id), nullable=False)
    away_team_id = Column(ForeignKey(Teams.id), nullable=False)
    season = Column(Integer)
    season_type = Column(Enum(SeasonType, create_constraint=True))
    game_date = Column(String(10))
    matchup = Column(String(11))
    home_wl = Column(Enum(WL, create_constraint=True))

    @classmethod
    def populate(cls, season, season_type, **kwargs):
        games = get_games(season, season_type, **kwargs)
        cls.save_df(games)


@declarative_mixin
class GameID:
    @declared_attr
    def game_id(cls):
        return PriorityColumn(ForeignKey(Games.id), primary_key=True)
