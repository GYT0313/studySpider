# -*- coding: utf-8 -*-
import scrapy

from DomesticWeb.items import DomesticwebItem


class AreaSpider(scrapy.Spider):
    name = 'area'
    allowed_domains = ['https://top.aizhan.com/']
    offset = 1
    start_url = "https://top.aizhan.com/area/p" + str(offset) + ".html"
    start_urls = [start_url]

    def parse(self, response):
        # print response.body
        # 提取每个response的数据
        node_list = response.xpath("//div[@class='list']/ul/li")

        for node in node_list:
            # 构建item对象,用来保存数据
            item = DomesticwebItem()

            # 提取信息
            item['image_link'] = "https:" + node.xpath("./div[@class='thumb']/a/img/@data-original").extract()[0].encode("utf-8")

            item['web_name'] = node.xpath("./div[@class='text']/h2/a/text()").extract()[0].encode("utf-8")

            item['web_link'] = node.xpath("./div[@class='text']/h2/em/text()").extract()[0].encode("utf-8")

            item['introduction'] = node.xpath("./div[@class='text']/p/text()").extract()[0].encode("utf-8")

            item['web_rank'] = node.xpath("./div[@class='rank']/div[@class='top']/text()").extract()[0].encode("utf-8")

            yield item

        # 定义请求页面范围 300*10个网站
        if AreaSpider.offset < 300:
            # 请求下一页
            if len(response.xpath("//div[@class='page']/ul/li[@class='disabled']/span/text()").extract()) == 0 or response.xpath("//div[@class='page']/ul/li[@class='disabled']/span/text()").extract()[0] != '>':
                AreaSpider.offset += 1

                yield scrapy.Request("https://top.aizhan.com/area/p" + str(AreaSpider.offset) + ".html", callback = self.parse, dont_filter = True)
