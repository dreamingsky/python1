import scrapy
class JDBookItem(scrapy.Item):
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