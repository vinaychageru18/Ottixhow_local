from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from seller_dashboard.crawl_integration.scraper.ottix.spiders.sprouts_spider import SproutsKeywordSpider
from seller_dashboard.crawl_integration.scraper.ottix.spiders.wegmans_spider import WegmansKeywordSpider
from seller_dashboard.crawl_integration.scraper.ottix.spiders.amazon_spider import AmazonKeywordSpider

class Command(BaseCommand):
    help = "Crawl all active products"

    def handle(self, *args, **options):
        keyword = 'Dirty Potato Chips'
        category = 'snacks'
        process = CrawlerProcess(get_project_settings())        
        # process.crawl(SproutsKeywordSpider, keyword=keyword, category=category)
        process.crawl(AmazonKeywordSpider, keyword=keyword, category=category)
        # process.crawl(WegmansKeywordSpider, keyword=keyword, category=category)
        process.start()