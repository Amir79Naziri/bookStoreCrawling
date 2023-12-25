# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# def serilizer_price(value):
#     value = str(value)
#     return '$ {value}'

class BookItem(scrapy.Item):
    
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    # price = scrapy.Field(serilizer=serilizer_price) first runs serilizer_price and then set it
    
    
    def __repr__(self):
        """only print title after exiting the Pipeline"""
        return repr({"title": self["title"]})