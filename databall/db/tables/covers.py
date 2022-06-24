from decimal import Decimal

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from databall.covers import GameSpider
from databall.db.base import Base
from databall.db.columns import ConstrainedField, EnumField
from databall.db.tables.game import GameID
from databall.types import OverUnderResult, SpreadResult


class Covers(Base, GameID, table=True):
    home_spread: Decimal = ConstrainedField(
        name='home_spread',
        ge=-30,
        le=30,
        multiple_of=0.5,
        schema_extra={'max_digits': 3, 'decimal_places': 1},
    )
    home_spread_result: SpreadResult = EnumField(SpreadResult, use_values=True)
    over_under: Decimal = ConstrainedField(
        name='over_under',
        ge=100,
        le=300,
        multiple_of=0.5,
        schema_extra={'max_digits': 4, 'decimal_places': 1},
    )
    over_under_result: OverUnderResult = EnumField(OverUnderResult, use_values=True)

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
