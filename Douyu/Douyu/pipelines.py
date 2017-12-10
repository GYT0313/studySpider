# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline

class DouyuPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        image_link = item['imageLink']
        # 返回一个图片链接请求
        yield scrapy.Request(image_link)


    def item_completed(self, results, item, info):
        # 取出results里图片的路径的值
        image_path = [x["path"] for ok, x in results if ok]

        # 修改图片名称为主播昵称
        os.rename(images_store + image_path[0], images_store + item["nickname"] + ".jpg")
        return item