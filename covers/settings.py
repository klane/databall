BOT_NAME = 'covers'

SPIDER_MODULES = ['covers.spiders']
NEWSPIDER_MODULE = 'covers.spiders'
DATABASE = '/home/mike/databall/nba.db'
DROP = 1
ITEM_PIPELINES = {
    'covers.pipelines.GamePipeline': 1,
}

DOWNLOAD_DELAY = 1.0
