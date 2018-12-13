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
            row = {
                'URL': 'https://www.target.com' + item['url'],
                'price_min': item['offer_price']['min_price'],
                'price_max': item['offer_price']['max_price'],
                'item_name': item['title'],
                'description': item['bullet_description'],
                'main_image_url': (item['images'][0]['base_url'] + item['images'][0]['primary']) if len(item['images']) > 0 else '',
                'variation_attributes': item.get('variation_attributes') or {},
            }
            if len(item['images']) > 0 and item['images'][0].get('alternate_urls'):
                for i in range(len(item['images'][0]['alternate_urls'])):
                    row['alternate_url_{0}'.format(i)] = item['images'][0]['base_url'] + item['images'][0]['alternate_urls'][i]
            yield row

        self.offset = self.offset + 1
        yield scrapy.Request(
            url=self.search_url.format(self.count, self.offset*self.count, self.keyword),
            callback=self.parse,
        )
