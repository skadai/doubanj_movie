# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
from datetime import datetime
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join, Compose


def filter_runtime(runtime):
    try:
        rel = int(re.match('^\d+', runtime).group())
    except Exception as e:
        rel = -1
    return rel


def filter_releasetime(release_time):
    return release_time.split('(')[0]

def filter_rate(rate):
    try:
        rate = float(rate)
    except:
        pass
    return rate


class DoubanjItem(scrapy.Item):
    directors = scrapy.Field()
    rate = scrapy.Field()
    title = scrapy.Field()
    casts =scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    id = scrapy.Field()
    genre = scrapy.Field()
    release_time = scrapy.Field()
    runtime = scrapy.Field()


class MovieLoader(ItemLoader):

    default_output_processor = TakeFirst()

    genre_out = Join('-')
    casts_out = Join('-')
    rate_in = MapCompose(filter_rate)
    release_time_out = TakeFirst()
    release_time_in = MapCompose(unicode.strip, filter_releasetime)
    runtime_out = TakeFirst()
    runtime_in = MapCompose(unicode.strip, filter_runtime)


