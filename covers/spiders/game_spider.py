import re

import pandas as pd
from scrapy import Request, Spider
from scrapy.selector import SelectorList

from covers.items import Game
from covers.loaders import GameLoader


def get_text(response):
    return response.xpath('text()').get().strip()


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
            f'https://www.covers.com/sport/basketball/nba/teams/main/{team}/{season}'
            for team in teams
        ]

    def parse(self, response):
        past_results = '//div[@id="TP_pastResults"]'

        for row in response.xpath(f'{past_results}//table/tbody/tr'):
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
            loader.add_value('response_url', response.url)

            # add missing fields
            item = loader.load_item()
            fields = ['spread_result', 'spread', 'over_under_result', 'over_under']
            fields = [f for f in fields if f not in item]

            for f in fields:
                item[f] = None

            yield item

        # find selected season
        season = response.xpath(f'{past_results}//span[@id="TP-Season-Select"]')
        season = get_text(season)

        # get other seasons for the current team
        history = response.xpath(f'{past_results}//div[@id="TP-Season-Drop"]/li/a')

        # get seasons prior to the selected season
        history = SelectorList(row for row in history if get_text(row) < season)

        # scrape previous season if one exists
        url = history.xpath('@href').get()

        if url is not None:
            yield Request(response.urljoin(url), callback=self.parse)
