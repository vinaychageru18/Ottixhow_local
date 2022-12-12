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
        parser.add_argument('--field', type=str)
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
        EDIT_FIELD = options['field']
        print(CSV_FILE_NAME)
        csv_file = open(CSV_FILE_NAME)
        product_objects = csv.DictReader(csv_file)
        edited_products = set()
        for _obj in product_objects:
            if _obj['vendor'] not in ['Sprouts', 'Wegmans']:
                continue
            name = _obj['name']
            vendor = _obj['vendor']
            brands = _obj['brands']
            print(name, vendor)
            product = Product.objects.get(name=name, vendor_name=vendor, brands=brands)
            if product.id in edited_products:
                print('Error - Might be wrong product')
                continue
            else:
                edited_products.add(product.id)
            product.product_image = _obj['product_image']
            product.save()
