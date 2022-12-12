# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OttixItem(scrapy.Item):
    name                =   scrapy.Field()
    price               =   scrapy.Field()
    vendor_name         =   scrapy.Field()
    vendor_url          =   scrapy.Field()
    seller_name         =   scrapy.Field()
    keyword             =   scrapy.Field()
    category            =   scrapy.Field()
    quantity            =   scrapy.Field()
    description         =   scrapy.Field()
    buy_box             =   scrapy.Field()
    is_best_link        =   scrapy.Field()
    product_image       =   scrapy.Field()
    is_active           =   scrapy.Field()
    url                 =   scrapy.Field()
    department          =   scrapy.Field()
    brands              =   scrapy.Field()
    rating              =   scrapy.Field()
    score               =   scrapy.Field()
    unit                =   scrapy.Field()
    availability_status =   scrapy.Field()
    # unit_price          =   scrapy.Field()