import csv
from django.core.management.base import BaseCommand
from seller_dashboard.models import *
from django.contrib.auth.models import User

def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())

class Command(BaseCommand):
    help = "Add stubs for missing links"

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
        """
        product_fields = ['name', 'description', 'unit',
                           'url', 'department', 'brands', 'sub_department', 'product_image',
                           'seller', 'vendor', 'storename', 'category']
        NA_DICT = {k: "NA" for k in product_fields}
        VENDORS_LIST = ['Sprouts', 'Wegmans', 'Amazon']
        user = User.objects.get(username=settings.DEFAULT_ADMIN)
        my_products = Product.objects.filter(user=user)
        for product in my_products:
            competitors = Product.objects.filter(crawl=product.crawl).filter(is_best_link__in=[True])
            available_vendors = [_comp.vendor_name for _comp in competitors]
            diff = set(VENDORS_LIST).difference(set(available_vendors))
            if diff:
                for vendor_name in diff:
                    print(f'No competitor product for {product.name} for vendor {vendor_name}')
                    _obj = NA_DICT
                    vendor = Vendors.objects.get(name=vendor_name)
                    seller = Seller.objects.get(vendor=vendor)
                    _obj['buy_box'] = True
                    _obj['price'] = 0.0
                    _obj['upc'] = 0
                    _obj['is_best_link'] = True
                    _obj['is_active'] = True
                    _obj['quantity'] = 0.0
                    _obj['vendor'] = vendor
                    _obj['vendor_name'] = vendor_name
                    _obj['seller'] = seller
                    _obj['category'] = product.category
                    _obj['crawl'] = product.crawl
                    _obj['storename'] = seller.name
                    _obj['normalized_price'] = 0.0
                    Product.objects.create(**_obj)
