import scrapy

class BaseOttixSpider(scrapy.Spider):
    name = 'BaseOttixSpider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'seller_dashboard.crawl_integration.scraper.ottix.pipelines.OttixPipeline': 400
        }
    }

    def parse_product(self, response):
        # Parsing logic goes here
        from seller_dashboard.crawl_integration.scraper.ottix.items import SampleItem
        item = SampleItem()
        item['name'] = 'iphone'
        item['price'] = 135.0
        item['keyword'] = response.meta['keyword']
        item['category'] = response.meta['category']
        item['seller'] = 'amazonseller'
        item['vendor'] = 'amazon'
        yield item


class TestKeywordSpider(BaseOttixSpider):
    name = 'TestKeywordSpider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = kwargs.get('keyword')
        self.category = kwargs.get('category')

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': self.keyword, 'category': self.category})

    def parse(self, response):
        return self.parse_product(response)
