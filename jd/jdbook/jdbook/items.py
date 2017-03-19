# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    img = scrapy.Field()
    channel = scrapy.Field()
    tag = scrapy.Field()
    sub_tag = scrapy.Field()
    value = scrapy.Field()
    comments = scrapy.Field()
