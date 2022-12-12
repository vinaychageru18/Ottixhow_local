from copy import deepcopy
from math import prod
from django.contrib.auth.models import User
from seller_dashboard.models import Crawl, Product, RawCrawledData, Vendors, Seller


MATCH_SCORES = {
    'substring': 1.0,
    'word': 0.5,
    'any': 0.4
}


VALID_KEYS = [
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
'seller_name',
'keyword',
'vendor_name',
'category',
]


MANDATORY_KEYS = [
'name',
'unit',
'quantity',
'price',
'is_best_link',
'url',
'brands',
'product_image',
'seller_name',
'keyword',
'vendor_name',
'category',   
]


def remove_numbers(input_string) -> str:
    return ''.join(e for e in input_string if e.isalpha())


def clean_string(input_string) -> str:
    return ''.join(e for e in input_string if e.isalnum())


def decent_match(keyword, product) -> bool:
    keyword = keyword.split(' ')
    product = product.split(' ')
    for key in keyword:
        if key in product:
            return True
    
    for key in product:
        if key in keyword:
            return True
    return False


def is_similar(keyword:str, product_name:str) -> float:
    from difflib import SequenceMatcher
    """
    Returns the similarity ratio between two products
    """
    raw_keyword = keyword
    raw_product_name = product_name
    keyword = clean_string(keyword.lower())
    product_name = clean_string(product_name.lower())

    ## check if keyword is a substring
    if keyword in product_name:
        return MATCH_SCORES['substring']
    elif decent_match(raw_keyword, raw_product_name):
        return MATCH_SCORES['word']
    else:
        return SequenceMatcher(None, keyword, product_name).ratio()


def get_normalized_price(quantity:float, price:float) -> float:
    """
    Returns the normalized price based on quantity.
    TODO
    """
    return price/quantity


def add_product(product_dict) -> Product:
    from django.conf import settings
    """
    Adds a scraped product according to the details. Check VALID_KEYS for list of
    valid keys.
    """
    invalid_keys = []
    for key in product_dict.keys():
        if key not in VALID_KEYS:
            print('Invalid key: ', key)
            invalid_keys.append(key)
    for key in invalid_keys:
        product_dict.pop(key)
    if missing_keys := set(MANDATORY_KEYS).difference(set(product_dict.keys())):
        print('Missing Keys: ', missing_keys)
        return None
    vendor_name = product_dict.get('vendor_name')
    seller_name = product_dict.get('seller_name')
    if not seller_name:
        seller_name = vendor_name + ' Seller'
    vendor = Vendors.objects.get(name=vendor_name)
    seller = Seller.objects.get(name=seller_name)
    keyword = product_dict.get('keyword')
    keyword = keyword.replace('+', ' ')
    product_dict['keyword'] = keyword
    category = product_dict.get('category', keyword)
    category = category.strip('\n')
    product_dict['category'] = category
    crawl = Crawl.objects.get(keyword=keyword)
    if crawl.category != category:  
        crawl.category = category
        crawl.save()
    try:
        user = User.objects.get(username=settings.DEFAULT_ADMIN)
        competitors = Product.objects.exclude(user=user)
        product = competitors.get(crawl=crawl, seller=seller, vendor=vendor)
        # Update price, image link etc
        product.name = product_dict.get('name')
        product.price = product_dict.get('price')
        quantity = float(product_dict.get('quantity'))
        price = float(product_dict.get('price'))
        normalized_price = get_normalized_price(quantity, price)
        product.quantity = product_dict.get('quantity')
        product.normalized_price = normalized_price
        product.storename = seller_name
        product.category = category
        product.product_image = product_dict.get('product_image')
        product.save()
    except Product.DoesNotExist:
        product_data = dict(product_dict)
        product_data['seller'] = seller
        product_data['crawl'] = crawl
        product_data['vendor'] = vendor
        product_data['storename'] = seller_name
        product_data.pop('keyword')
        product_data.pop('seller_name')
        product = Product.objects.create(**product_data)
    return product
