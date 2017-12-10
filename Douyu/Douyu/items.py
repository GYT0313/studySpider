# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # 主播昵称
    nickname = scrapy.Field()
    # 图片链接
    imageLink = scrapy.Field()
