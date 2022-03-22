import re
import sqlite3
from datetime import datetime


class GamePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('DATABASE')
        drop = settings.getbool('DROP')
        return cls(db, drop)

    def __init__(self, db, drop):
        self.db = db
        self.drop = drop
        self.con = None
        self.cur = None

    def open_spider(self, spider):
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()

        if self.drop:
            self.cur.executescript(
                '''
                DROP TABLE IF EXISTS betting;
                CREATE TABLE betting(
                    GAME_ID TEXT,
                    HOME_SPREAD REAL,
                    HOME_SPREAD_WL TEXT,
                    OVER_UNDER REAL,
                    OU_RESULT TEXT
                );
                '''
            )

    def close_spider(self, spider):
        self.cur.execute('VACUUM')
        self.con.close()

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
        # only store home games to avoid duplicating data
        if item['home']:
            # map team abbreviations to those in the database
            team_abbr = {
                'BK': 'BKN',
                'CHAR': 'CHA',
                'GS': 'GSW',
                'NETS': 'BKN',
                'NJ': 'BKN',
                'NO': 'NOP',
                'NY': 'NYK',
                'PHO': 'PHX',
                'SA': 'SAS',
            }

            opponent = item['opponent'].upper()

            if opponent in team_abbr:
                opponent = team_abbr[opponent]

            # find opponent ID by abbreviation
            self.cur.execute(f'SELECT ID FROM teams WHERE ABBREVIATION IS "{opponent}"')
            opp_id = self.cur.fetchone()[0]

            # format game date to match games table
            response = item['response_url']
            start_year, end_year = re.search(r'(\d+)-(\d+)', response).group(1, 2)
            start_months = ['Oct', 'Nov', 'Dec']

            date = item['date']
            year = start_year if date.split()[0] in start_months else end_year
            date = datetime.strptime(f'{date} {year}', '%b %d %Y')
            date = date.strftime('%Y-%m-%d')

            # find game by opponent and date
            self.cur.execute(
                f'''
                SELECT ID FROM games
                WHERE AWAY_TEAM_ID == {opp_id} AND GAME_DATE IS "{date}"
                '''
            )
            game_id = self.cur.fetchone()

            # raise exception if no matching game found
            if game_id is None:
                raise ValueError('No game found')

            # insert row into database
            values = (
                game_id[0],
                item['spread'],
                item['spread_result'],
                item['over_under'],
                item['over_under_result'],
            )
            self.cur.execute(
                '''
                INSERT INTO betting(
                    GAME_ID, HOME_SPREAD, HOME_SPREAD_WL, OVER_UNDER, OU_RESULT
                )
                VALUES(?, ?, ?, ?, ?)
                ''',
                values,
            )
            self.con.commit()
