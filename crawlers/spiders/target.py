import scrapy, json
from scrapy_splash import SplashRequest

class TargetSpider(scrapy.Spider):
    name = 'target'
    count = 24
    offset = 0
    base_url = 'https://www.target.com'
    search_url = 'https://redsky.target.com/v1/plp/search/?count={0}&offset={1}&keyword={2}&default_purchasability_filter=true&include_sponsored_search=false&ppatok=AOxT33a&platform=desktop&useragent=Mozilla/5.0+(X11;+Linux+x86_64)+AppleWebKit/602.1+(KHTML,+like+Gecko)+splash+Version/9.0+Safari/602.1&store_ids=905,1821,1945,1944,1943,2448&pageId=/s/lamp&channel=web&visitorId=01677364AACA0201A673BCD1095CF074'

    def start_requests(self):
        yield scrapy.Request(
            url=self.search_url.format(self.count, self.offset*self.count, self.keyword),
            callback=self.parse,
        )

    def parse(self, response):
        data = json.loads(response.text)
        if not data or \
           not data['search_response'] or \
           not data['search_response']['items'] or \
           not data['search_response']['items']['Item']:
            return

        for item in data['search_response']['items']['Item']:
            yield item

        self.offset = self.offset + 1
        yield scrapy.Request(
            url=self.search_url.format(self.count, self.offset*self.count, self.keyword),
            callback=self.parse,
        )
