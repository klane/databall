import re
from collections import deque

import pandas as pd
from scrapy import Request, Spider

from covers.items import Game
from covers.loaders import GameLoader

base_url = 'https://www.covers.com'


class GameSpider(Spider):
    name = 'games'
    allowed_domains = ['covers.com']
    custom_settings = {
        'ITEM_PIPELINES': {'covers.pipelines.GamePipeline': 400},
    }

    def __init__(self, teams, season='2019-2020', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if '.json' in teams:
            teams = pd.read_json(teams)
            teams = [
                re.search(r'main/(?P<name>[^/]+)', url).group('name')
                for url in teams.url
            ]
        else:
            teams = teams.split(',')

        self.start_urls = [
            base_url + f'/sport/basketball/nba/teams/main/{team}/{season}'
            for team in teams
        ]

    def parse(self, response):
        table_class = 'table covers-CoversMatchups-Table covers-CoversResults-Table'

        for row in response.xpath(f'//table[@class="{table_class}"]/tbody/tr'):
            loader = GameLoader(item=Game(), selector=row)
            loader.add_xpath('date', 'td[1]/text()')
            loader.add_xpath('home', 'td[2]/a/text()')
            loader.add_xpath('opponent', 'td[2]/a/text()')
            loader.add_xpath('result', 'td[3]/a/text()')
            loader.add_xpath('score', 'td[3]/text()')
            loader.add_xpath('score', 'td[3]/a/text()')
            loader.add_xpath('opponent_score', 'td[3]/text()')
            loader.add_xpath('opponent_score', 'td[3]/a/text()')
            loader.add_xpath('spread_result', 'td[4]/span/text()')
            loader.add_xpath('spread', 'td[4]/text()')
            loader.add_xpath('over_under_result', 'td[5]/span/text()')
            loader.add_xpath('over_under', 'td[5]/text()')
            loader.add_value('response_url', response._url)

            # add missing fields
            item = loader.load_item()
            fields = ['spread_result', 'spread', 'over_under_result', 'over_under']
            fields = list(filter(lambda f: f not in item, fields))

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
