import csv
from seller_dashboard.models import Vendors
from seller_dashboard.models import Seller
from seller_dashboard.models import Crawl
from seller_dashboard.models import Product

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
CSV_FILE_NAME = ''
csv_file = open(CSV_FILE_NAME)
reader = csv.DictReader(csv_file)
objects = list[reader]

for _obj in objects:
    keyword = _obj.get('keyword')
    category = _obj.get('category')
    _obj.pop('keyword')
    _obj.pop('category')
    vendor_name = _obj.get('vendor')
    vendor_url = _obj.get('vendor_url')
    seller_name = _obj.get('seller')
    crawl, _ = Crawl.objects.get_or_create(keyword=keyword, category=category)
    vendor, _ = Vendors.objects.get_or_create(name=vendor_name, website_url=vendor_url)
    seller = Seller.objects.get_or_create(name=seller_name, vendor=vendor)
    _obj.pop('vendor_url')
    _obj['vendor'] = Vendors
    _obj['seller'] = Seller
    _obj['crawl'] = Crawl
    _obj['is_best_link'] = True
    Product.objects.create(**_obj)
