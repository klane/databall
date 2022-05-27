from pydantic import BaseModel, conint, constr, validator

from databall.constants import CURRENT_SEASON, MIN_SEASON
from databall.db.schemas.team import Teams
from databall.types import GameResult, SeasonType


class Games(BaseModel):
    id: constr(regex=r'^\d{10}$', strict=True)
    home_team_id: Teams.__annotations__['id']
    away_team_id: Teams.__annotations__['id']
    season: conint(ge=MIN_SEASON, le=CURRENT_SEASON, strict=True)
    season_type: SeasonType
    game_date: constr(regex=r'^\d{4}-\d{2}-\d{2}$', strict=True)
    matchup: constr(regex=r'^[A-Z]{3} vs. [A-Z]{3}$', strict=True)
    home_wl: GameResult

    @validator('season_type', pre=True)
    def check_season_type(cls, name):
        season_types = SeasonType._member_names_

        if name not in season_types:
            raise ValueError(f'Season type should be one of: {season_types}')

        return SeasonType[name]


class GameID(BaseModel):
    game_id: Games.__annotations__['id']
