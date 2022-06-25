import re
from datetime import datetime

import pandas as pd
from scrapy import Request, Spider

from databall.api import get_teams
from databall.covers.items import Game
from databall.covers.loaders import GameLoader


class GameSpider(Spider):
    name = 'games'
    allowed_domains = ['covers.com']
    custom_settings = {
        'ITEM_PIPELINES': {'databall.covers.pipelines.GamePipeline': 400},
    }

    def __init__(self, teams=None, season='', stop_season=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if teams is None:
            teams = get_teams()['full_name']
        elif '.json' in teams:
            teams = pd.read_json(teams)
            teams = [
                re.search(r'main/(?P<name>[^/]+)', url).group('name')
                for url in teams.url
            ]
        else:
            teams = teams.split(',')

        teams = [team.strip().replace(' ', '-').lower() for team in teams]

        if isinstance(season, int):
            season = f'{season}-{season+1}'

        if isinstance(stop_season, int):
            self.stop_season = f'{stop_season}-{stop_season+1}'
        else:
            self.stop_season = stop_season

        self.start_urls = [
            f'https://www.covers.com/sport/basketball/nba/teams/main/{team}/{season}'
            for team in teams
        ]

    def parse(self, response):
        past_results = '//div[@id="TP_pastResults"]'
        start_year, year = re.search(r'(\d+)-(\d+)', response.url).groups()
        date = ''

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

            # add missing fields
            item = loader.load_item()
            fields = ['spread_result', 'spread', 'over_under_result', 'over_under']
            fields = [f for f in fields if f not in item]

            for f in fields:
                item[f] = None

            # format game date to match games table
            if 'Jan' in date and 'Jan' not in item['date']:
                year = start_year

            date = item['date']
            item['date'] = datetime.strptime(f'{date} {year}', '%b %d %Y').date()

            yield item

        if self.stop_season is not None:
            # find selected season
            xpath = f'{past_results}//span[@id="TP-Season-Select"]/text()'
            selected_season = response.xpath(xpath).get().strip()

            # get other seasons for the current team
            xpath = f'{past_results}//div[@id="TP-Season-Drop"]/li/a/text()'
            seasons = [s.strip() for s in response.xpath(xpath).getall()]

            # get next season between the selected and stop seasons
            seasons = [s for s in seasons if selected_season < s <= self.stop_season]
            next_season = min(seasons, default=None)

            # scrape next season if one exists
            if next_season is not None:
                url = response.url.replace(selected_season, next_season)
                yield Request(url, callback=self.parse)
