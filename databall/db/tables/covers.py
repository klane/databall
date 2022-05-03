from enum import Enum

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import Column, Float

from databall.covers import GameSpider
from databall.db.base import Base
from databall.db.columns import PositiveColumn, ValuesEnum
from databall.db.tables.game import GameID


class SpreadResult(str, Enum):
    WIN = 'W'
    LOSS = 'L'
    PUSH = 'P'


class OverUnderResult(str, Enum):
    OVER = 'O'
    UNDER = 'U'
    PUSH = 'P'


class Covers(Base, GameID):
    home_spread = Column(Float(precision=1))
    home_spread_result = Column(ValuesEnum(SpreadResult, create_constraint=True))
    over_under = PositiveColumn(Float(precision=1))
    over_under_result = Column(ValuesEnum(OverUnderResult, create_constraint=True))

    @classmethod
    def populate(cls, season, *args, **kwargs):
        print(f'Scraping {season} covers')
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        crawler = process.create_crawler(GameSpider)
        process.crawl(crawler, season=season, *args, **kwargs)
        process.start()

        games = crawler.stats.get_value('games', 0)
        print(f'Saved {games} rows to {cls.__tablename__}')
