from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from databall.db import Covers, Games, Teams


class GamePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('DATABASE', ':memory:')
        drop = settings.getbool('DROP', False)
        return cls(db, drop)

    def __init__(self, db, drop):
        self.db = db
        self.drop = drop
        self.session = None

    def open_spider(self, spider):
        engine = create_engine(f'sqlite:///{self.db}')
        self.session = Session(bind=engine, future=True)

        if self.drop:
            Covers.__table__.drop(engine)
            Covers.__table__.create(engine)

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # only store home games to avoid duplicating data
        if item['home']:
            self.store_item(item)

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
