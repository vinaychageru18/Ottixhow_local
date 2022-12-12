from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from seller_dashboard.models import Crawl
from seller_dashboard.crawl_integration.scraper.ottix.spiders import AmazonKeywordSpider, \
    SproutsKeywordSpider, WegmansKeywordSpider


class Command(BaseCommand):
    help = "Crawl all active products"

    def initiate_crawl(self, keyword, category):
        # SPIDER_CLASS_LIST = [WegmansKeywordSpider, AmazonKeywordSpider, SproutsKeywordSpider]
        SPIDER_CLASS_LIST = [SproutsKeywordSpider]
        process = CrawlerProcess(get_project_settings())
        process.crawl(SproutsKeywordSpider, keyword=keyword, category=category)
        process.start()
        # for cls in SPIDER_CLASS_LIST:
        #     # import sys    
        #     # if "twisted.internet.reactor" in sys.modules:
        #     #     del sys.modules["twisted.internet.reactor"]
        #     process = CrawlerProcess(get_project_settings())
        #     process.crawl(cls, keyword=keyword, category=category)
        #     process.start()
        # return

    def handle(self, *args, **options):
        from datetime import datetime
        qs = Crawl.objects.filter(is_active__in=[True])
        for crawl in qs:
            if not crawl.last_crawl:
                print('First crawl for ', crawl.keyword)
                self.initiate_crawl(keyword=crawl.keyword, category=crawl.category)
                crawl.last_crawl = datetime.now()
                crawl.save()
            else:
                duration = datetime.now() - crawl.last_crawl
                if duration.total_seconds() > 3600:
                    self.initiate_crawl(keyword=crawl.keyword, category=crawl.category)
                    crawl.last_crawl = datetime.now()
                    crawl.save()