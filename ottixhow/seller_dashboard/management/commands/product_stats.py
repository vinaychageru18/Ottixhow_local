import csv
from collections import defaultdict
from django.core.management.base import BaseCommand
from seller_dashboard.models import *

def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())

class Command(BaseCommand):
    help = "Generates product stats csv"

    def handle(self, *args, **options):
        from datetime import datetime
        date = datetime.strftime(datetime.now(), format='%d%b').strip('/')
        product_fields = ['product_id', 'name', 'competitor_id', 'tfmprice+10%', 'competitor_price', 'less']
        with open(f'product_stats_{date}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=product_fields)
            writer.writeheader()
            my_products = Product.objects.filter(vendor_name__icontains='fresh')
            for product in my_products:
                competitors = Product.objects.filter(crawl=product.crawl).filter(is_best_link__in=[True])
                for competitor in competitors:
                    row = defaultdict()
                    less = None
                    tfm_price = product.normalized_price + 0.1 * product.normalized_price
                    if tfm_price < competitor.normalized_price:
                        less = True
                    else:
                        less = False
                    row['product_id'] = product.id
                    row['name'] = product.name
                    row['competitor_id'] = competitor.id
                    row['tfmprice+10%'] = tfm_price
                    row['competitor_price'] = competitor.normalized_price
                    row['less'] = less
                    writer.writerow(row)
                
