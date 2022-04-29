import enum

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import Column, Enum, Float

from databall.covers import GameSpider
from databall.db.base import Base
from databall.db.columns import PositiveColumn
from databall.db.tables.game import GameID

SpreadResult = enum.Enum('SpreadResult', 'W L P')
OverUnderResult = enum.Enum('OverUnderResult', 'O U P')


class Covers(Base, GameID):
    home_spread = Column(Float(precision=1))
    home_spread_result = Column(Enum(SpreadResult, create_constraint=True))
    over_under = PositiveColumn(Float(precision=1))
    over_under_result = Column(Enum(OverUnderResult, create_constraint=True))

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
