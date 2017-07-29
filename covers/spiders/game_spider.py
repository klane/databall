import re
import pandas as pd
from collections import deque
from scrapy import Spider, Request
from covers.items import Game
from covers.loaders import GameLoader

base_url = 'http://www.covers.com'


class GameSpider(Spider):
    name = 'games'
    allowed_domains = ['covers.com']

    def __init__(self, teams, season='2016-2017', *args, **kwargs):
        super(GameSpider, self).__init__(*args, **kwargs)

        if '.json' in teams:
            teams = pd.read_json(teams)
            teams = [re.search('team\d+', url).group(0) for url in teams.url]
        else:
            teams = teams.split(',')

        self.start_urls = [base_url + '/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/%s/%s.html' %
                           (season, team) for team in teams]

    def parse(self, response):
        for row in response.xpath('//tr[@class="datarow"]'):
            loader = GameLoader(item=Game(), selector=row)
            loader.add_xpath('date', 'td[1]/text()')
            loader.add_xpath('location', 'td[2]/text()')
            loader.add_xpath('opponent', 'td[2]/a/text()')
            loader.add_xpath('result', 'td[3]/text()')
            loader.add_xpath('score', 'td[3]/text()')
            loader.add_xpath('score', 'td[3]/a/text()')
            loader.add_xpath('opponent_score', 'td[3]/text()')
            loader.add_xpath('opponent_score', 'td[3]/a/text()')
            loader.add_xpath('season_type', 'td[4]/text()')
            loader.add_xpath('spread_result', 'td[5]/text()')
            loader.add_xpath('spread', 'td[5]/text()')
            loader.add_xpath('over_under_result', 'td[6]/text()')
            loader.add_xpath('over_under', 'td[6]/text()')

            # add missing fields
            item = loader.load_item()
            fields = [f for f in ['spread_result', 'spread', 'over_under_result', 'over_under'] if f not in item]

            for f in fields:
                item[f] = None

            yield item

        # get list of previous seasons for the current team
        history = deque(response.xpath('//option'))
        season = _get_next_season(history)

        # find selected season
        while season and season.xpath('@selected').extract_first() is None:
            season = _get_next_season(history)

        # find next season to scrape, some pages have duplicate seasons in the drop down
        while season and season.xpath('@value').extract_first() in response.url:
            season = _get_next_season(history)

        # scrape previous season if one exists
        if season:
            url = base_url + season.xpath('@value').extract_first()
            yield Request(response.urljoin(url), callback=self.parse)


def _get_next_season(history):
    try:
        return history.popleft()
    except IndexError:
        return None
