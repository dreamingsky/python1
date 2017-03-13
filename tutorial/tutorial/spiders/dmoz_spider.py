import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = "dmoz.org"
    start_urls = []

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename,'wb') as f:
            f.write(response.body)



