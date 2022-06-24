from sqlmodel import Field, SQLModel

from databall.api import get_teams
from databall.db.base import Base
from databall.db.columns import UniqueField

NAME_REGEX = r'^[A-Z][a-z]+( ([A-Z]|\d{2})[a-z]+)+$'


class Teams(Base, table=True):
    id: int = Field(ge=1610612737, le=1610612766, primary_key=True)
    name: str = UniqueField(regex=NAME_REGEX, max_length=50, nullable=False)
    abbreviation: str = UniqueField(regex=r'^[A-Z]{3}$', max_length=3, nullable=False)

    @classmethod
    def populate(cls):
        teams = get_teams()
        teams.rename(columns={'full_name': 'name'}, inplace=True)
        cls.save_df(teams)


class TeamID(SQLModel):
    team_id: Teams.__annotations__['id'] = Field(foreign_key=Teams.id, primary_key=True)
