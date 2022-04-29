import databall.db.settings as settings
from databall.data import SeasonType
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
    for season_type in SeasonType:
        Games.populate(season, season_type)
        TeamStats.populate(season, season_type)
        PlayerStats.populate(season, season_type)

    Covers.populate(season)
