from scrapy import Field, Item


class Game(Item):
    date = Field()
    home = Field()
    opponent = Field()
    score = Field()
    opponent_score = Field()
    result = Field()
    spread = Field()
    spread_result = Field()
    over_under = Field()
    over_under_result = Field()


class Team(Item):
    city = Field()
    url = Field()
