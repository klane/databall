from scrapy import Spider
from covers.items import Team
from covers.loaders import TeamLoader


class TeamSpider(Spider):
    name = 'teams'
    allowed_domains = ['covers.com']
    start_urls = ['http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/teams.html']

    def parse(self, response):
        for row in response.xpath('//td[@class="datacell"]/a'):
            loader = TeamLoader(item=Team(), selector=row)
            loader.add_xpath('city', 'text()')
            loader.add_xpath('url', '@href')
            yield loader.load_item()
