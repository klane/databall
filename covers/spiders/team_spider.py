from scrapy import Spider
from covers.items import Team
from covers.loaders import TeamLoader


class TeamSpider(Spider):
    name = 'teams'
    allowed_domains = ['covers.com']
    start_urls = ['https://www.covers.com/sport/basketball/nba/teams']

    def parse(self, response):
        for row in response.xpath('//td/a'):
            loader = TeamLoader(item=Team(), selector=row)
            loader.add_xpath('city', 'text()')
            loader.add_xpath('url', '@href')
            yield loader.load_item()
