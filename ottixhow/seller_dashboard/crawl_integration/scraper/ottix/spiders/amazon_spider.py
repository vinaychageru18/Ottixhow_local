from collections import defaultdict
from email.policy import default
import os
from unicodedata import category
import scrapy
import requests
from bs4 import BeautifulSoup
from selectorlib import Extractor
from seller_dashboard.crawl_integration.scraper.ottix.settings import MAX_PRODUCT_YIELD


class AmazonProductSpider(scrapy.Spider):
    name = 'AmazonProductSpider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'seller_dashboard.crawl_integration.scraper.ottix.pipelines.OttixPipeline': 400
        }
    }
    vendor_name = 'amazon'
    vendor_url  = 'www.amazon.com'
    HEADERS     = ({'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    def parse_product(self, response_list, keyword, category):
        from seller_dashboard.crawl_integration.scraper.ottix.items import OttixItem
        ref_ink = 'https://www.amazon.com'
        secondary_item = OttixItem()
        max_score = 0.0
        max_products = 0
        for product in response_list:
            product_url = ref_ink + product['url']
            item = self.extract(product_url,keyword,category)
            max_products += 1
            print(item)
            # breakpoint()
            if item['is_best_link']:
                return item
            else:
                if item['score'] >= max_score:
                    secondary_item = item
            if max_products >= MAX_PRODUCT_YIELD:
                return None
        secondary_item['is_best_link'] = True
        return secondary_item

    def extract(self, product_url,keyword,category):
        from seller_dashboard.crawl_integration.scraper.ottix.items import OttixItem
        from seller_dashboard.crawl_integration.models_interface import is_similar
        item = OttixItem()
        req = requests.get(product_url, headers=self.HEADERS)
        html = BeautifulSoup(req.text, "lxml")
        try:
            item['name'] = html.find("span", attrs={
                "id": 'productTitle'}).string.strip().replace(',', '')
        except AttributeError:
            try:
                item['name'] = html.find('span', attrs={
                    "class": 'a-size-large product-title-word-break'}).string.strip().replace(',', '')
            except AttributeError:
                item['name'] = "NA"
        try:
            item['price'] = html.find(
                "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
            item['price'] = item['price'].strip('$')
            # item['price'] = float(item['price'])
        except AttributeError:
            item['price'] = "NA"
    #------------------------------retrieving product rating--------------------------------------#
        try:
            item['rating'] = html.find("i", attrs={
                'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
        except AttributeError:
            try:
                item['rating'] = html.find(
                    "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
            except:
                item['rating'] = "NA"
    # -----------------------------------availablility status----------------------------------------#
        try:
            item['availability_status'] = html.find("div", attrs={'id': 'availability'}).find(
                "span").string.strip().replace(',', '')
        except AttributeError:
            item['availability_status'] = "NA"
    #-----------------------------------Seller Name------------------------------------------------#
        try:
            item['seller_name'] = html.find(
                "div", attrs={"id": 'merchant-info'}).contents[2].string
        except:
            try:
               item['seller_name'] = html.find(
                    "a", attrs={"id": 'sellerProfileTriggerId'}).string
            except AttributeError:
                item['seller_name']  = "default_seller"
                
        item["quantity"]    =   1.0
        item["description"] =   "Default Description"
        item["buy_box"]     =   True
        item["is_active"]   =   True
        item["url"]         =   product_url
        item["department"]  =   "defalt_department"
        item["vendor_name"] =   self.vendor_name
        item["vendor_url"]  =   self.vendor_url
        item["keyword"]     =   keyword
        item["category"]    =   category
        item["brands"]      =   'brand_name'
        item['unit']        =   'oz'
        # item['unit_price']  =   item['price']
        item['product_image']  =   'https://cdn-icons-png.flaticon.com/512/7616/7616872.png'
        item['is_best_link']=   False
        if score := is_similar(keyword, item['name']) == 1.0:
            item['is_best_link'] = True
            item['score'] = score
        else:
            item['score'] = score
            return item
        print(item.keys())
        return item

class AmazonKeywordSpider(AmazonProductSpider):
    name = 'AmazonKeywordSpider'
    extractor = Extractor.from_yaml_file(f'{os.getcwd()}/ottixhow/seller_dashboard/crawl_integration/scraper/scrap_criteria.yml')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = kwargs.get('keyword')
        self.keyword = self.keyword.replace(' ', '+')
        self.category = kwargs.get('category')

    def start_requests(self):
        BASE_URL = 'https://www.amazon.com/s?k='
        # if isinstance(self.keyword, list):
        #     self.keyword = [self.keyword]
        # for keyword in self.keyword:
        #     # url = f'{BASE_URL}{keyword}'
        #     self.keyword = self.keyword.replace(' ', '+')
        #     url = BASE_URL + self.keyword
        #     print(url)
        #     # breakpoint()
        url = BASE_URL + self.keyword
        yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': self.keyword, 'category': self.category})

    def parse(self, response):
        # Extractor logic goes here
        data = self.extractor.extract(response.text)
        # print(data)
        # breakpoint()
        if data:
            return self.parse_product(data['products'], keyword=self.keyword, category=self.category)
