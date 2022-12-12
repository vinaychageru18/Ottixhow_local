from collections import defaultdict
import csv
from itertools import product
from django.core.management.base import BaseCommand
from seller_dashboard.models import *
from django.contrib.auth.models import User

def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())

class Command(BaseCommand):
    help = "Add stubs for missing links"

    def handle(self, *args, **options):
        from django.conf import settings
        user = User.objects.get(username=settings.DEFAULT_ADMIN)
        my_products = Product.objects.filter(vendor_name='The Fresh Market')
        crawl_map = defaultdict(dict)
        for product in my_products:
            crawl_map[product.crawl.keyword][product.vendor_name] = []
        for product in my_products:
            competitors = list(Product.objects.exclude(user=user).filter(is_best_link__in=[True]).filter(crawl=product.crawl))
            for competitor in competitors:
                crawl_map[product.crawl.keyword][product.vendor_name].append(competitor.id)
        edit_ids = set()
        for crawl, vendor_dict in crawl_map.items():
            for vendor, competitors in vendor_dict.items():
                if len(competitors) > 1:
                    for i in range(1, len(competitors)):
                        edit_ids.add(competitors[i])
        print(crawl_map)
        print(edit_ids)
        # for _id in edit_ids:
        #     prod = Product.objects.get(id=_id)
        #     prod.is_best_link = False
        #     prod.save()