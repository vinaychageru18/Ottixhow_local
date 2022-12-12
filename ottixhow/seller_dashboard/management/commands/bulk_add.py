from collections import defaultdict
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
        from django.conf import settings
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
        Vendors.objects.all().delete()
        Seller.objects.all().delete()
        Crawl.objects.all().delete()
        Product.objects.all().delete()
        fieldnames = ['department','sub_department','category','name','vendor','price','normalized_price','quantity','unit','keyword','upc','description','seller','brands','is_active','url','product_image','vendor_url','vendor_image']

        CSV_FILE_NAME = options['file']
        print(CSV_FILE_NAME)
        csv_file = open(CSV_FILE_NAME)
        product_objects = csv.DictReader(csv_file, fieldnames=fieldnames)
        count = 1
        names = defaultdict(set)

        for _obj in product_objects:
            product_name = _obj['name']
            if not product_name or product_name == 'name':
                print('Name missing or header!!')
                continue
            print(f'Adding product {count}: {_obj["name"]}')
            keyword = _obj.get('keyword').lower()
            category = _obj.get('category')
            _obj.pop('keyword')
            _obj.pop('category')
            vendor_name = _obj.get('vendor')
            if names.get(vendor_name):
                if product_name in names.get(vendor_name):
                    print(f'Duplicate product found: {product_name}: {vendor_name}')
                    continue
                else:
                    names[vendor_name].add(product_name)
            vendor_url = _obj.get('vendor_url')
            vendor_image = _obj.get('vendor_image')
            seller_name = _obj.get('seller')
            crawl, _ = Crawl.objects.get_or_create(keyword=keyword, category=keyword)
            if vendor_name == 'The Fresh Market':
                user = User.objects.get(username=settings.DEFAULT_ADMIN)
                vendor, _ = Vendors.objects.get_or_create(name=vendor_name, website_url=vendor_url, vendor_image=vendor_image, user=user)
            else:
                vendor, _ = Vendors.objects.get_or_create(name=vendor_name, website_url=vendor_url, vendor_image=vendor_image)
            print('Vendor ID ', vendor.id)
            seller, _ = Seller.objects.get_or_create(name=seller_name, vendor=vendor)
            _obj.pop('vendor_url')
            _obj.pop('vendor_image')
            _obj['vendor'] = vendor
            _obj['seller'] = seller
            _obj['crawl'] = crawl
            # _obj['quantity'] = ''.join([i for i in _obj['quantity'] if not i.isalpha()])
            _obj['quantity'] = float(_obj['quantity'])
            _obj['unit'] = ''.join([i for i in _obj['unit'] if not i.isdigit()])
            _obj['is_active'] = True
            _obj['vendor_name'] = vendor_name
            _obj['url'] = _obj.get('url', '')
            _obj['category'] = category
            _obj['storename'] = seller_name
            if _obj['upc'] == 'NA':
                _obj['upc'] = 0
            _obj['upc'] = int(_obj['upc'])
            if not vendor_name == 'The Fresh Market':
                _obj['is_best_link'] = True
            if vendor_name == 'The Fresh Market':
                _obj['storename'] = 'TFM'
                user = User.objects.get(username=settings.DEFAULT_ADMIN)
                _obj['user'] = user
            Product.objects.create(**_obj)
            print(f'Added product {count}: {_obj["name"]}')
            count += 1
