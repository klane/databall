from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr

from databall.api import get_team_stats
from databall.db.base import Base
from databall.db.columns import PriorityColumn, ValuesEnum
from databall.db.tables.team import Teams
from databall.types import GameResult, SeasonType


class Games(Base):
    id = Column(String(10), primary_key=True)
    home_team_id = Column(ForeignKey(Teams.id), nullable=False)
    away_team_id = Column(ForeignKey(Teams.id), nullable=False)
    season = Column(Integer)
    season_type = Column(Enum(SeasonType, create_constraint=True))
    game_date = Column(String(10))
    matchup = Column(String(11))
    home_wl = Column(ValuesEnum(GameResult, create_constraint=True))

    @classmethod
    def populate(cls, season, season_type, **kwargs):
        team_stats = get_team_stats(season, season_type, **kwargs)
        away_index = team_stats.matchup.str.contains('@')

        home = team_stats[~away_index].copy()
        home.rename(
            columns={'game_id': 'id', 'team_id': 'home_team_id', 'wl': 'home_wl'},
            inplace=True,
        )

        away = team_stats[away_index].copy()
        away.rename(columns={'game_id': 'id', 'team_id': 'away_team_id'}, inplace=True)

        games = home.merge(away[['id', 'away_team_id']], on='id')
        games['season'] = games.season_id.apply(lambda season_id: int(season_id[1:]))
        games['season_type'] = season_type.name

        cls.save_df(games)


@declarative_mixin
class GameID:
    @declared_attr
    def game_id(cls):
        return PriorityColumn(ForeignKey(Games.id), primary_key=True)
