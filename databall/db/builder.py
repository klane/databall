import databall.db.settings as settings
from databall.db import Covers, Games, Players, PlayerStats, Teams, TeamStats
from databall.db.base import Base
from databall.db.session import Session

DEFAULT_DROP = False


def init():
    with Session() as session, session.connection() as connection:
        if getattr(settings, 'DROP', DEFAULT_DROP):
            Base.metadata.drop_all(connection)
            session.execute('VACUUM')

        Base.metadata.create_all(connection)

    Teams.populate()
    Players.populate()


def populate(season):
    Games.populate(season)
    TeamStats.populate(season)
    PlayerStats.populate(season)
    Covers.populate(season)
