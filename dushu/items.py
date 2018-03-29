# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DushuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 第一页
    book_image_url = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    # 详细信息
    book_price = scrapy.Field()
    book_info = scrapy.Field()
    # 出版社
    book_publish = scrapy.Field()









