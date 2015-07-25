from datetime import datetime
#from hotelsupply.conf import settings
import os.path

BOT_NAME = 'scrape_tripadvisor'
SPIDER_MODULES = ['scrape_tripadvisor.spiders']
NEWSPIDER_MODULE = 'scrape_tripadvisor.spiders'


USER_AGENT = 'Chrome/6.0.472.63'

"""
FEED_FORMAT = 'json'

FEED_URI = os.path.join(
    settings.DATA_DIR,
    'tripadvisor',
    '%(name)s%(time)s.json'
)
LOG_FILE = os.path.join(
    settings.LOG_DIR,
    'tripadvisor',
    datetime.now().isoformat()+'.log'
)
"""

ITEM_PIPELINES = {'scrape_tripadvisor.pipelines.HotelItemPipeline': 500}
