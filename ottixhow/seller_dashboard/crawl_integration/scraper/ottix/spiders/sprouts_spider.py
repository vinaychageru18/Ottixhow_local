import scrapy
from seller_dashboard.crawl_integration.scraper.ottix.settings import MAX_PRODUCT_YIELD


class SproutsKeywordSpider(scrapy.Spider):
    name = 'SproutsKeywordSpider'
    handle_httpstatus_list = [401]
    custom_settings = {
        'ITEM_PIPELINES': {
            'seller_dashboard.crawl_integration.scraper.ottix.pipelines.OttixPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None
        }
    }
    cookies = '_gcl_au=1.1.1761880801.1662127441; _fbp=fb.1.1662127445336.198864170; BVBRANDID=4982d711-709a-442f-acea-bd18df9b8bd0; _pin_unauth=dWlkPU1EaGhOakkxTURNdE0yVXpNaTAwTVRJeExXRXlZMkV0T0dFM01EQTNNbUV5TURjeg; ajs_anonymous_id=0b3fc69d-f628-4bcb-9670-641d72ea7d8b; _pin_unauth=dWlkPU1EaGhOakkxTURNdE0yVXpNaTAwTVRJeExXRXlZMkV0T0dFM01EQTNNbUV5TURjeg; __stripe_mid=cec5f183-e70a-4d46-a472-d8d32a4e8aff6753fd; ajs_anonymous_id=0b3fc69d-f628-4bcb-9670-641d72ea7d8b; ab.storage.sessionId.aeab3310-682f-4e08-9c9d-07d176b1452b={"g":"9906154f-2864-c593-d7b0-a8cd38ac618e","e":1664788928973,"c":1664787128977,"l":1664787128977}; ab.storage.deviceId.aeab3310-682f-4e08-9c9d-07d176b1452b={"g":"6986dca4-8580-0ea4-ae05-a68490f57376","c":1663880644625,"l":1664787128980}; _gid=GA1.2.1865627037.1665736028; _uetsid=fda06e404b9911edb5390dad472879e1; _uetvid=1a4402502ac811ed82df57cd3d52c45d; _gat_UA-47434162-1=1; BVBRANDSID=fb834862-5440-4157-8ace-d5a95a52509d; _derived_epik=dj0yJnU9UHBKdWk4YWpzeXhQcVoyeGU3TG1fU2QzcDdJdm9pSG4mbj1VVmd2SE1hYm8wN1J5LU01RnljMnNRJm09MSZ0PUFBQUFBR05KU1FNJnJtPTEmcnQ9QUFBQUFHTkpTUU0; dotcomSearchId=acd904fa-fdfa-4fbb-b30d-e6cc560e12c8; session-sprouts=.eJwtjVFvgjAYRf9Ln42BGnXwtolsJfo5ECrshVioUqiFWERg2X8fyfZwX07uufcbpZc71wWyL2ep-QylDb_fzoqrFtnt_TERzbUWtUrbuuIK2YgPXsHeM3EQHolGYoLwrPkEzQzTYcqYYdkxaTVfG7ICx8fgRMPeyYzd5q8TY1mRsu6hJAsIqxHGRJObW7GTfOQxyOzfZYpqtnmK5LTsmJItW9CRlI2RKSqnrSaJfXEotxjKyDw4yQBhpomCLsGyYK7VJTE1zq5VJzHU058ITv2RuWAklSyj8A2oA-DHNAAMQU4pPoYR5lHwIMqYv7T757WiRaNfiecXpuH3lb_7vMJ2sczFXoTZmo2N23cfPpqhh-b3VOTINld4vbQW69XPL7JOdRU.Firakw.C6QgD_v40ZDpv1OEKJxmr9x8QBc; _ga_LPZ816BHL5=GS1.1.1665747202.45.1.1665747219.43.0.0; _ga=GA1.2.20930352.1662127444; _derived_epik=dj0yJnU9M3BlSVEzckotUjdlZ0JnbUtlMzZnbHRVOTFrbmMyRlQmbj1WXzFtSmFEck1raGhrQmtyYkJhNktnJm09MSZ0PUFBQUFBR05KU1JRJnJtPTEmcnQ9QUFBQUFHTkpTUlE; __stripe_sid=ebcf89b5-610b-477a-b33f-e86f07d2276dd43040; _dd_s=rum=1&id=baaf1c95-5358-4fcd-891b-c8cd1ec6a157&created=1665747224185&expire=1665748124185'
    HEADERS = {
        'Accept-Language': "en-US,en;q=0.9",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        'cookie': cookies
    }
    seller_name = 'Sprouts Seller'
    vendor_name = 'Sprouts'
    vendor_url = 'www.Sprouts.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = kwargs.get('keyword')
        self.keyword = self.keyword.replace(' ', '+')
        self.category = kwargs.get('category')

    def start_requests(self):
        BASE_URL = 'https://shop.sprouts.com/api/v2/store_products?search_term='
        url = BASE_URL + self.keyword
        yield scrapy.Request(url=url, callback=self.parse, headers=self.HEADERS,meta={'keyword': self.keyword, 'category': self.category})

    def parse(self, response):
        from seller_dashboard.crawl_integration.scraper.ottix.items import OttixItem
        secondary_item=OttixItem()
        data = response.json()
        item_count = int(data['item_count'])
        max_score = 0.0
        if item_count > MAX_PRODUCT_YIELD:
            item_count = MAX_PRODUCT_YIELD
        if item_count != 0:
            for item_number in range(item_count):
                item = self.extract(data['items'], item_number)
                if item['is_best_link']:
                    return item
                else:
                    if item['score'] >= max_score:
                        secondary_item = item
                        max_score = item['score']
            secondary_item['is_best_link'] = True
            return secondary_item                
        return None


    def extract(self, data, item_number):
        from seller_dashboard.crawl_integration.scraper.ottix.items import OttixItem
        from seller_dashboard.crawl_integration.models_interface import is_similar
        item = OttixItem()
        item['description']         =   'Default Description'
        item['buy_box']             =   True
        item['is_best_link']        =   False
        item['is_active']           =   True
        item['seller_name']         =   self.seller_name
        item['department']          =   "default_department"
        item['vendor_name']         =   self.vendor_name
        item['vendor_url']          =   self.vendor_url 
        item['keyword']             =   self.keyword
        item['rating']              =   '4.0'
        item['name']                =   str(data[item_number]['name']).split(',')[0]
        item['price']               =   str(data[item_number]['base_price'])
        item['category']            =   str(data[item_number]['categories'][0]['name'])+'\n'
        item['quantity']            =   str(data[item_number]['base_quantity'])
        # item['product_image']        =   str(data['items'][0]['images']['tile']['small'])
        item['product_image']          =   'https://cdn-icons-png.flaticon.com/512/7616/7616872.png'
        item['url']                 =   'https://shop.sprouts.com/product/'+str(data[item_number]['href'].split('/')[2])
        item['brands']          =   str(data[item_number]['brand_name']).split(',')[0]
        item['unit']                =   str(data[item_number]['uom_price']['uom'])
        # item['unit_price']          =   str(data[item_number]['uom_price']['price'])
        item['availability_status'] =   str(data[item_number]['availability_status'])
        score                       =   is_similar(self.keyword, item['name'])
        if score == 1.0:
            item['is_best_link'] = True
        item['score'] = score
        return item