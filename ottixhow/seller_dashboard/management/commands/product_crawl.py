from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from seller_dashboard.models import Product
from seller_dashboard.crawl_integration.scraper.scraper.spiders.base import BaseVendorSpider

class Command(BaseCommand):
    help = "Crawl all active products"

    def handle(self, *args, **options):
        products = Product.objects.filter(is_best_link__in=[True])
        product_urls = [product.url for product in products]
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaseVendorSpider, start_urls=product_urls)
        process.start()