from sqlalchemy import select

from databall.db import Covers, Games, Teams
from databall.db.session import Session


class GamePipeline:
    def __init__(self):
        self.session = None

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
        self.session = None

    def process_item(self, item, spider):
        # only store home games to avoid duplicating data
        if item['home']:
            self.store_item(item)
            spider.crawler.stats.inc_value('games')

        return item

    def store_item(self, item):
        # find game by opponent and date or raise exception if not found
        query = (
            select(Games.id)
            .join(Teams, Teams.id == Games.away_team_id)
            .where(
                (Teams.abbreviation == item['opponent'])
                & (Games.game_date == item['date'])
            )
        )
        game_id = self.session.execute(query).scalars().one()

        # insert row into database
        row = Covers(
            game_id=game_id,
            home_spread=item['spread'],
            home_spread_result=item['spread_result'],
            over_under=item['over_under'],
            over_under_result=item['over_under_result'],
        )
        self.session.add(row)
