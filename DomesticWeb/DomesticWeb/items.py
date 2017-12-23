# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DomesticwebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 图片url
    image_link = scrapy.Field()

    # 网站名称
    web_name = scrapy.Field()

    # 网站地址
    web_link = scrapy.Field()

    # 网站简介
    introduction = scrapy.Field()

    # 网站排名
    web_rank = scrapy.Field()


