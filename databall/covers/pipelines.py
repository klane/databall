from sqlalchemy import select

from databall.db import Covers, Games, Teams, TeamStats
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
            self.store_item(item, spider)

        return item

    def store_item(self, item, spider):
        # find game by opponent and date or raise exception if not found
        query = (
            select(Games)
            .join(Teams, Teams.id == Games.away_team_id)
            .where(
                (Teams.abbreviation == item['opponent'])
                & (Games.game_date == item['date'])
            )
        )
        game = self.session.execute(query).scalars().one()

        # check that scraped score matches database
        for team, score in zip(['home', 'away'], ['score', 'opponent_score']):
            query = select(TeamStats.pts).where(
                (TeamStats.game_id == game.id)
                & (TeamStats.team_id == getattr(game, f'{team}_team_id'))
            )
            pts = self.session.execute(query).scalars().one()

            if item[score] != pts:
                raise ValueError(f'Scraped {team} team score does not match database')

        # check that scraped result matches database
        if item['result'] != game.home_wl:
            raise ValueError('Scraped result does not match database')

        # insert row into database if not present
        if game.id not in Covers.primary_keys.values:
            row = Covers(
                game_id=game.id,
                home_spread=item['spread'],
                home_spread_result=item['spread_result'],
                over_under=item['over_under'],
                over_under_result=item['over_under_result'],
            )
            self.session.add(row)
            spider.crawler.stats.inc_value('games')
