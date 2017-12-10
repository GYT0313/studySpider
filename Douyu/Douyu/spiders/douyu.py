# -*- coding: utf-8 -*-

from Douyu.items import DouyuItem
import scrapy
import json

class DouyuSpider(scrapy.Spider):
    # 爬虫名
    name = 'douyu'
    # 爬虫域范围
    allowed_domains = ['douyucdn.cn']
    # 基础url
    baseURL = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    offset = 0
    # 爬取url入口
    start_urls = [baseURL + str(offset)]



    def parse(self, response):
        data_list = json.loads(response.body)['data']
        
        # 判断是否还有待爬取url
        if not len(data_list):
            return 

        for data in data_list:
            # 创建管道文件
            item = DouyuItem()
            item['nickname'] = data["nickname"]
            item['imageLink'] = data["vertical_src"]

            yield item

        # 偏移量增加20
        self.offset += 20
        yield scrapy.Request(self.baseURL + str(self.offset), callback = self.parse)
