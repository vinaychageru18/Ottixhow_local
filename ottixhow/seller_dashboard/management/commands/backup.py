import csv
from django.core.management.base import BaseCommand
from seller_dashboard.models import *
from django.contrib.auth.models import User
from datetime import datetime

def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())

class Command(BaseCommand):
    help = "Add stubs for missing links"

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
        """
        products = Product.objects.all()
        date = datetime.strftime(datetime.now(), format='%d%b').strip('/')
        with open(f'products_backup_{date}.csv', 'w') as csvfile:
            fieldnames = ['id',
                'created_date',
                'modified_date',
                'name',
                'description',
                'unit',
                'quantity',
                'price',
                'normalized_price',
                'buy_box',
                'is_best_link',
                'is_active',
                'url',
                'department',
                'brands',
                'sub_department',
                'upc',
                'product_image',
                'seller_id',
                'crawl_id',
                'vendor_id',
                'vendor_name',
                'storename',
                'category',
                'user_id'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in products.values():
                writer.writerow(product)
