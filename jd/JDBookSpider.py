from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import JDBookItem
class JDBookSpider(Spider):
    name = "jdbook"
    allowed_domains = ["jd.com"]
    start_urls = ["http://item.jd.com/11678007.html"]
    cookies = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    meta = {"dont_redirect":True,'handle_httpstatus_list': [301, 302]}
    def get_next_url(self,old_url):
        list = old_url.split('/')
        old_item_id = int(list[3].split('.')[0])
        new_item_id = old_item_id-1
        if new_item_id == 0:
            return
        new_url = '/'.join([list[0],list[1],list[2],str(new_item_id)+'.html'])
        return str(new_url)
    def start_requests(self):
        yield Request(self.start_urls[0],callback=self.parse,headers=self.headers,cookies=self.cookies,meta=self.meta)
    def parse(self, response):
        selector = Selector(response)
        item = JDBookItem()
        extractor = LxmlLinkExtractor(allow=r'http://item.jd.com/\d.*html')
        link = extractor.extract_links(response)