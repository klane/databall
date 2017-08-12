import re
from functools import partial
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class GameLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    location_in = MapCompose(str.strip, lambda x: x if len(x) > 0 else u'vs')
    result_in = MapCompose(str.strip, str.split)
    score_in = MapCompose(partial(re.findall, u'\d+-\d+'), lambda x: x.split(u'-'), int)
    opponent_score_in = MapCompose(partial(re.findall, u'\d+-\d+'), lambda x: x.split(u'-')[1], int)
    spread_result_in = MapCompose(str.strip, str.split, lambda x: x if x != u'-' else None)
    spread_in = MapCompose(lambda x: x.strip().split()[1], lambda x: 0 if x == u'PK' else x,
                           lambda x: float(x) if x != u'-' else None)
    over_under_result_in = spread_result_in
    over_under_in = spread_in


class TeamLoader(ItemLoader):
    default_output_processor = TakeFirst()
