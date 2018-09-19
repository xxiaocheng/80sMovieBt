# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviebtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    year=scrapy.Field()
    url=scrapy.Field()
    tags=scrapy.Field()
    comments=scrapy.Field()
    score=scrapy.Field()
    bts=scrapy.Field()

