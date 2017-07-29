import re
import sqlite3
from datetime import datetime


class GamePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        db = settings.get('database')
        drop = settings.getbool('drop')
        return cls(db, drop)

    def __init__(self, db, drop):
        self.db = db
        self.drop = drop
        self.con = None
        self.cur = None

    def open_spider(self, spider):
        if spider.name == 'games' and self.db is not None:
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()

            if self.drop:
                self.cur.executescript('''
                    DROP TABLE IF EXISTS betting;
                    CREATE TABLE betting(GAME_ID TEXT, OVER_UNDER REAL, OU_RESULT TEXT,
                                         HOME_SPREAD REAL, HOME_SPREAD_WL TEXT);
                    ''')

    def close_spider(self, spider):
        if spider.name == 'games' and self.db is not None:
            self.cur.execute('VACUUM')
            self.con.close()

    def process_item(self, item, spider):
        if spider.name == 'games' and self.db is not None:
            self.store_item(item)

        return item

    def store_item(self, item):
        opponent = item['opponent']
        date = item['date']
        location = item['location']

        # covers.com has an error and lists a Houston @ Sacramento game as having taken place in Houston
        if opponent == 'Houston' and date == '04/04/95':
            location = 'vs'

        # only store regular season home games to avoid duplicating games
        if item['season_type'] == 'Regular Season' and location == 'vs':
            date = datetime.strptime(date, '%m/%d/%y')

            '''
            Covers.com list old Hornets games as New Orleans, but the database has them as Charlotte. The opponent needs
            to be changed to Charlotte for games prior to the 02-03 season in order to find the game ID.
            '''
            diff = date - datetime(2002, 8, 1)

            if opponent == 'New Orleans' and diff.days < 0:
                opponent = 'Charlotte'

            # find team ID by mascot for the two LA teams and by city for all other teams
            pattern = re.compile('L\.?A\.? ')

            if pattern.match(opponent) is not None:
                opponent = pattern.sub('', opponent)
                self.cur.execute('SELECT ID FROM teams WHERE MASCOT IS "{}"'.format(opponent))
            else:
                self.cur.execute('SELECT ID FROM teams WHERE CITY IS "{}"'.format(opponent))

            self.cur.execute('SELECT ID FROM games WHERE AWAY_TEAM_ID == {} AND GAME_DATE IS "{}"'
                             .format(self.cur.fetchone()[0], date.strftime('%Y-%m-%d')))
            game_id = self.cur.fetchone()

            if game_id is None:
                raise ValueError('No game found')

            self.cur.execute('''INSERT INTO betting(GAME_ID, OVER_UNDER, OU_RESULT, HOME_SPREAD, HOME_SPREAD_WL)
                                VALUES(?, ?, ?, ?, ?)''', (game_id[0], item['over_under'], item['over_under_result'],
                                                           item['spread'], item['spread_result']))
            self.con.commit()
