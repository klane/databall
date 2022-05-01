import random
import time

from nba_api.stats.library.parameters import Season

import databall.covers.settings as scrapy_settings
import databall.db.settings as settings
from databall.data import SeasonType
from databall.db import Covers, Games, Players, PlayerStats, Teams, TeamStats
from databall.db.base import Base
from databall.db.session import Session

DEFAULT_DELAY = 1.0
DEFAULT_DROP = False
MIN_SEASON = 2006  # earliest season in Covers data


def init():
    with Session() as session, session.connection() as connection:
        if getattr(settings, 'DROP', DEFAULT_DROP):
            Base.metadata.drop_all(connection)
            session.execute('VACUUM')

        Base.metadata.create_all(connection)

    Teams.populate()
    Players.populate()


def populate(start_season=MIN_SEASON, stop_season=Season.current_season_year):
    duration = getattr(scrapy_settings, 'DOWNLOAD_DELAY', DEFAULT_DELAY)

    for season in range(start_season, stop_season + 1):
        for season_type in SeasonType:
            # no need to wait between games and team stats since the data is cached
            Games.populate(season, season_type)
            TeamStats.populate(season, season_type)
            wait(duration)
            PlayerStats.populate(season, season_type)
            wait(duration)

    Covers.populate(start_season, stop_season=stop_season)


def update():
    populate(start_season=Season.current_season_year)


def wait(duration):
    time.sleep(duration * (random.random() + 0.5))
