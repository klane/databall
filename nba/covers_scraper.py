import scrapy
from collections import deque

base_url = 'http://www.covers.com'
results_url = '/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/%s/%s.html'


class GameSpider(scrapy.Spider):
    name = 'game_spider'
    allowed_domains = ['covers.com']

    def __init__(self, teams='', season='2016-2017', *args, **kwargs):
        super(GameSpider, self).__init__(*args, **kwargs)
        self.start_urls = [base_url + results_url % (season, team) for team in teams.split(',')]

    def parse(self, response):
        for row in response.xpath('//tr[@class="datarow"]'):
            game = Game()
            game['date'] = row.xpath('td[1]/text()').extract_first().strip()

            location = row.xpath('td[2]/text()').extract_first().strip()
            game['location'] = location if len(location) > 0 else 'vs'
            game['opponent'] = row.xpath('td[2]/a/text()').extract_first()

            score = row.xpath('td[3]/a/text()').extract_first()

            if score is not None:
                game['score'], game['opponent_score'] = [int(x) for x in score.strip().split('-')]
                game['result'] = row.xpath('td[3]/text()').extract_first().strip()
            else:
                score = row.xpath('td[3]/text()').extract_first().strip().rstrip('(OT)')
                game['score'], game['opponent_score'] = [int(x) for x in score[2:].split('-')]
                game['result'] = score[0]

            game['season_type'] = row.xpath('td[4]/text()').extract_first().strip()
            spread = row.xpath('td[5]/text()').extract_first().strip()
            game['spread_result'] = spread[0]

            try:
                game['spread'] = float(spread[2:])
            except ValueError:
                game['spread'] = 0

            over_under = row.xpath('td[6]/text()').extract_first().strip()

            try:
                game['over_under'] = float(over_under[2:])
                game['over_under_result'] = over_under[0]
            except ValueError:
                game['over_under'] = None
                game['over_under_result'] = None

            yield game

        history = deque(response.xpath('//option'))
        season = _get_next_season(history)

        while season and season.xpath('@selected').extract_first() is None:
            season = _get_next_season(history)

        season = _get_next_season(history)

        if season:
            url = base_url + season.xpath('@value').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse)


class TeamSpider(scrapy.Spider):
    name = 'team_spider'
    allowed_domains = [base_url]
    start_urls = [base_url + '/pageLoader/pageLoader.aspx?page=/data/nba/teams/teams.html']

    def parse(self, response):
        for row in response.xpath('//td[@class="datacell"]/a'):
            yield {row.xpath('text()').extract(): row.xpath('@href').extract()}


class Game(scrapy.Item):
    date = scrapy.Field()
    location = scrapy.Field()
    opponent = scrapy.Field()
    score = scrapy.Field()
    opponent_score = scrapy.Field()
    result = scrapy.Field()
    season_type = scrapy.Field()
    spread = scrapy.Field()
    spread_result = scrapy.Field()
    over_under = scrapy.Field()
    over_under_result = scrapy.Field()


def _get_next_season(history):
    try:
        return history.popleft()
    except IndexError:
        return None
