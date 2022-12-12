# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from seller_dashboard.crawl_integration.models_interface import add_product

class OttixPipeline:
    def process_item(self, item, spider):
        add_product(item)
        return item
