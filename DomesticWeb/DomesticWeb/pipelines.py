# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline


class DomesticwebPipeline(object):

    def __init__(self):
        self.f = open("domesticWeb.html", "w")
        self.f.write("<html>\n")
        self.f.write("<head>\n")
        self.f.write("<meta http-equiv='content-type' content='text/html;charset=utf-8'>\n")
        self.f.write("<link href='style.css' rel='stylesheet' type='text/css' />\n")
        self.f.write("<head>\n")
        self.f.write("<body>\n")
        self.f.write("<div class='boss' text-align='center'>\n")
        self.f.write("<strong><h1>2017年中国地区网站排名</h1></strong>\n")
        self.f.write("<ul summary='记录中国地区网站排行和其简介'>\n")
        

    def process_item(self, item, spider):
        self.f.write("<li>\n")
        self.f.write("<div class='thumb'>\n")
        self.f.write("<img src='Images/%s.jpg' />\n"%item['web_name'])
        self.f.write("</div>\n")

        self.f.write("<div class='text'>\n")
        self.f.write("<a href='https://%s' target='_blank'>%s</a>\n"%(item['web_link'], item['web_name']))
        self.f.write("<p>%s</p>\n"%item['introduction'])
        self.f.write("</div>\n")
        
        self.f.write("<div class='rank'>\n")
        self.f.write("<div class='top'><h2>&nbsp;&nbsp;%s&nbsp;&nbsp;</h2></div>\n"%item['web_rank'])
        self.f.write("<div class='bot'>总排名：%s</div>"%item['web_rank'])
        self.f.write("</div>\n")
        self.f.write("</li>\n")

        return item


    def __del__(self):
        self.f.write("</ul>\n")
        self.f.write("</div>\n")
        self.f.write("</body>\n")
        self.f.write("</html>\n")
        self.f.close()


class DomesticwebPicturePipeline(ImagesPipeline):
            
    def get_media_requests(self, item, info):
        image_link = item['image_link']
        yield scrapy.Request(image_link)


    def item_completed(self, results, item, info):
        # print results
        # 
        # 取出results里图片的路径的值
        image_path = [x["path"] for ok, x in results if ok]

        os.rename(images_store + image_path[0], images_store + item["web_name"] + ".jpg")
        return item