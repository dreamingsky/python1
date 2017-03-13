from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Spider

from jdbook.jdbook import JDBookItem


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
        try:
            item['_id'] = response.url.split('/')[3].split('.')[0]
            item['url'] = response.url
            item['title'] = selector.xpath('/html/head/title/text()').extract()[0]
            item['keywords'] = selector.xpath('/html/head/meta[2]/@content').extract()[0]
            item['description'] = selector.xpath('/html/head/meta[3]/@content').extract()[0]
            item['img'] = 'http:' + selector.xpath('//*[@id="spec-n1"]/img/@src').extract()[0]
            item['channel'] = selector.xpath('//*[@id="root-nav"]/div/div/strong/a/text()').extract()[0]
            item['tag'] = selector.xpath('//*[@id="root-nav"]/div/div/span[1]/a[1]/text()').extract()[0]
            item['sub_tag'] = selector.xpath('//*[@id="root-nav"]/div/div/span[1]/a[2]/text()').extract()[0]
            item['value'] = selector.xpath('//*[@id="root-nav"]/div/div/span[1]/a[2]/text()').extract()[0]
            comments = list()
            node_comments = selector.xpath('//*[@id="hidcomment"]/div')
            for node_comment in node_comments:
                comment = dict()
                node_comment_attrs = node_comment.xpath('.//div[contains(@class, "i-item")]')
                for attr in node_comment_attrs:
                    url = attr.xpath('.//div/strong/a/@href').extract()[0]
                    comment['url'] = 'http:' + url
                    content = attr.xpath('.//div/strong/a/text()').extract()[0]
                    comment['content'] = content
                    time = attr.xpath('.//div/span[2]/text()').extract()[0]
                    comment['time'] = time
                comments.append(comment)
            item['comments'] = comments
        except Exception as ex:
            print ('something wrong', str(ex))
        print ('success, go for next')
        yield item
        next_url = self.get_next_url(response.url)  # response.url就是原请求的url
        if next_url != None:  # 如果返回了新的url
            yield Request(next_url, callback=self.parse, headers=self.headers, cookies=self.cookies, meta=self.meta)