from datetime import date

from pydantic import validator
from sqlmodel import Field, SQLModel

from databall.api import get_team_stats
from databall.constants import CURRENT_SEASON, MIN_SEASON
from databall.db.base import Base
from databall.db.columns import EnumField
from databall.db.tables.team import Teams
from databall.types import GameResult, SeasonType

TEAM_ID = Teams.__annotations__['id']


class Games(Base, table=True):
    id: str = Field(regex=r'^\d{10}$', max_length=10, primary_key=True)
    home_team_id: TEAM_ID = Field(foreign_key=Teams.id, nullable=False)
    away_team_id: TEAM_ID = Field(foreign_key=Teams.id, nullable=False)
    season: int = Field(ge=MIN_SEASON, le=CURRENT_SEASON)
    season_type: SeasonType = EnumField(SeasonType)
    game_date: date = Field(nullable=False)
    matchup: str = Field(regex=r'^[A-Z]{3} vs. [A-Z]{3}$', max_length=11)
    home_wl: GameResult = EnumField(GameResult, use_values=True)

    @validator('season_type', pre=True)
    def check_season_type(cls, name):
        season_types = SeasonType._member_names_

        if name not in season_types:
            raise ValueError(f'Season type should be one of: {season_types}')

        return SeasonType[name]

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


class GameID(SQLModel):
    game_id: Games.__annotations__['id'] = Field(foreign_key=Games.id, primary_key=True)
