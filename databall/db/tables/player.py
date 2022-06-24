from sqlmodel import Field, SQLModel

from databall.api import get_players
from databall.db.base import Base
from databall.db.columns import ConstrainedField

NAME_REGEX = r'^[A-Z][A-Za-z,\'\-\.]+( [A-Za-z,\'\-\.]+)*$'


class Players(Base, table=True):
    id: int = ConstrainedField(name='id', gt=0, primary_key=True)
    name: str = Field(regex=NAME_REGEX, max_length=50, nullable=False)

    @classmethod
    def populate(cls, **kwargs):
        players = get_players(**kwargs)
        players.rename(
            columns={'person_id': 'id', 'display_first_last': 'name'},
            inplace=True,
        )
        cls.save_df(players)


class PlayerID(SQLModel):
    player_id: Players.__annotations__['id'] = Field(
        foreign_key=Players.id, primary_key=True
    )
