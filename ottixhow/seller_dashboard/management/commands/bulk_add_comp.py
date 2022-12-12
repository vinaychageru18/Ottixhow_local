import csv
from django.core.management.base import BaseCommand
from seller_dashboard.models import *
from django.contrib.auth.models import User

def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())

class Command(BaseCommand):
    help = "Bulk add scraped products"

    def add_arguments(self, parser) -> None:
        parser.add_argument('--file', type=str)
        return

    def handle(self, *args, **options):
        """
        Required fields in CSV
            name
            description
            unit 
            quantity 
            price 
            normalized_price 
            buy_box 
            is_best_link
            is_active 
            url 
            department 
            brands 
            product_image
            seller
            keyword
            category 
            vendor
            vendor_url
            usage: python manage.py --file csv_file_name.csv
        """
        CSV_FILE_NAME = options['file']
        print(CSV_FILE_NAME)
        csv_file = open(CSV_FILE_NAME)
        product_objects = csv.DictReader(csv_file)

        for _obj in product_objects:
            count = 1
            keyword = _obj.get('keyword')
            category = _obj.get('category')
            _obj.pop('keyword')
            _obj.pop('category')
            vendor_name = _obj.get('vendor')
            vendor_url = _obj.get('vendor_url')
            vendor_image = _obj.get('vendor_image')
            seller_name = _obj.get('seller')
            crawl = Crawl.objects.get(keyword=keyword)
            vendor = Vendors.objects.get(name=vendor_name)
            seller = Seller.objects.get(name=seller_name)
            _obj.pop('vendor_url')
            _obj.pop('vendor_image')
            _obj['vendor'] = vendor
            _obj['seller'] = seller
            _obj['crawl'] = crawl
            _obj['quantity'] = ''.join([i for i in _obj['quantity'] if not i.isalpha()])
            _obj['quantity'] = float(_obj['quantity'])
            _obj['unit'] = ''.join([i for i in _obj['unit'] if not i.isdigit()])
            _obj['is_active'] = True                
            if not vendor_name == 'The Fresh Market':
                print(crawl)
                product = SelfProducts.objects.get(crawl=crawl)
                _obj['product'] = product
                print(_obj )
                print(f'Adding product {count}: {_obj["name"]}')
                Competitors.objects.create(**_obj)
            count += 1
