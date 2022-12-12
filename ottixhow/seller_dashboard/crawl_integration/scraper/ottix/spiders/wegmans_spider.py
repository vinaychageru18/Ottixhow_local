import scrapy
from seller_dashboard.crawl_integration.scraper.ottix.settings import MAX_PRODUCT_YIELD


class WegmansKeywordSpider(scrapy.Spider):
    name = 'WegmansKeywordSpider'
    handle_httpstatus_list = [401]
    custom_settings = {
        'ITEM_PIPELINES': {
            'seller_dashboard.crawl_integration.scraper.ottix.pipelines.OttixPipeline': 400
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None
        }
    }
    cookies = '_gcl_au=1.1.371659048.1663712086; _fbp=fb.1.1663712087623.464426353; _pin_unauth=dWlkPU1EaGhOakkxTURNdE0yVXpNaTAwTVRJeExXRXlZMkV0T0dFM01EQTNNbUV5TURjeg; ajs_anonymous_id=90c56052-2670-476b-a477-0a196b931db8; __stripe_mid=f5d4e3c6-20d8-4fe3-ba49-c5418958f9a255795a; _pin_unauth=dWlkPU1EaGhOakkxTURNdE0yVXpNaTAwTVRJeExXRXlZMkV0T0dFM01EQTNNbUV5TURjeg; ajs_anonymous_id=90c56052-2670-476b-a477-0a196b931db8; s_fid=7D3127CE3F392905-2968A84B05077BD4; _derived_epik=dj0yJnU9cmU1cHBXVXdkUGw2Mjc3NFdESFQ2NVlWZmt5OEQ4MkUmbj1fSnRmM2xackR3U0hjdDFfWFFiTWhBJm09MSZ0PUFBQUFBR004TlhzJnJtPTEmcnQ9QUFBQUFHTThOWHM; _derived_epik=dj0yJnU9OW5HSDZQNEE3U2lUcUY4LUo0Z0JUdHpWRmQtVUtoRnAmbj14cHZ1SFdHb0JHM1BvZnZHMWUxa3J3Jm09MSZ0PUFBQUFBR05HM1ZNJnJtPTEmcnQ9QUFBQUFHTkczVk0; kndctr_68B620B35350F1650A490D45_AdobeOrg_identity=CiYwMzQ2NzM5NTM0NjI4MDY1NDk0MjI5NzI1MjIwODk5Mjg4ODAyOFIPCOjBmem1MBgBKgRJTkQx8AHUyMLmvDA=; session-prd-weg=.eJwtjEFvgjAARv9Lz84IHXPlirqUWbpFRORCbClQqIVQhMGy_z6S7fAuL-_7vkGad8KUwM1vyogVSFvR3W9a6B64ffdYjBHGyEanfVMLDVwgJr9kb1xS6ePzjK1A-mi9SIvb0bQwc1sNTKE28fALDc-QVMVIwuLr6P01sa1qXDUTDfdOEBInmLnB90PNLuqRxYHi_1umI8O8UV4vzsC06hmMZly1G64jtXy11_hT0mpvBxWBJMQj3ZVo_VwLkfHjx6gSCpG3K55e4Sk_kWGKO2wN72Fy6IyhpAg2YAUeRnSpzIBrIws5EG23P78s91zv.FisVYQ.mcrLN4VjypN3bxMCAby3jsGmjOA; mbox=PC#aa88a3c666164030baf06ecc968de875.31_0#1728833362|session#b588a77ce2c245f19fffb39da91f2231#1665764134; AMCVS_68B620B35350F1650A490D45@AdobeOrg=1; AMCV_68B620B35350F1650A490D45@AdobeOrg=1176715910|MCIDTS|19280|MCMID|03467395346280654942297252208992888028|MCAAMLH-1666367074|12|MCAAMB-1666367074|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1665769474s|NONE|MCCIDH|0|vVersion|5.4.0; _uetsid=19f7d5004bd711ed8216092147711037; _uetvid=a4104b70393111ed9839b5e7d43886cb; wfmStoreId=16; wfm.tracking.sessionStart=1665762274746; _dd_s=rum=1&id=b2253460-2cd9-40e8-adfa-b91082f6ee31&created=1665762276364&expire=1665763176364'
    HEADERS = {
        'Accept-Language': "en-US,en;q=0.9",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        'cookie': cookies
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = kwargs.get('keyword')
        self.keyword = self.keyword.replace(' ', '+')
        self.category = kwargs.get('category')
        self.vendor_name                     =   'Wegmans'
        self.vendor_url                      =   'www.Wegmans.com'

    def start_requests(self):
        BASE_URL = 'https://shop.wegmans.com/api/v2/store_products?&search_term='
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
        item['description']             =   'Default Description'
        item['buy_box']                 =   True
        item['is_best_link']            =   False
        item['is_active']               =   True
        item['seller_name']             =   'seller_name'
        item['department']              =   "default_department"
        item['vendor_name']             =   self.vendor_name
        item['vendor_url']              =   self.vendor_url 
        item['keyword']                 =   self.keyword
        item['rating']                  =   '4.0'
        item['name']                    =   str(data[item_number]['name']).split(',')[0]
        item['price']                   =   str(data[item_number]['base_price'])
        item['category']                =   str(data[item_number]['categories'][0]['name'])+'\n'
        item['quantity']                =   str(data[item_number]['base_quantity'])
        # item['product_image']              =   str(data['items'][0]['images']['tile']['small'])
        item['product_image']           =   'https://cdn-icons-png.flaticon.com/512/7616/7616872.png'
        item['url']                     =   'https://shop.wegmans.com/product/'+str(data[item_number]['href'].split('/')[2])
        item['brands']                  =   str(data[item_number]['brand_name']).split(',')[0]
        item['unit']                    =   str(data[item_number]['uom_price']['uom'])
        # item['unit_price']              =   str(data[item_number]['uom_price']['price'])
        item['availability_status']     =   str(data[item_number]['availability_status'])
        score                           =   is_similar(self.keyword, item['name'])
        if score == 1.0:
            item['is_best_link'] = True
        item['score']                   = score
        return item