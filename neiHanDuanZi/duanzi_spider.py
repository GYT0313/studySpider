# -*- coding: utf-8 -*-
'''
Created on 2017年12月18日

@author: GuYongtao
'''
#
import urllib2
import re


class Spiser():
    """
        内涵段子爬虫类
    """
    
    def __init__(self, page):
        self.enable = True
        self.page = page
     
    
    def loadpage(self, page):
        """
            @brief 定义一个url请求网页的方法
            @param page 需要请求的第几页
            @return 返回的页面html
        """
        # 请求url地址
        url = "http://www.neihan8.com/article/list_5_" + str(page) + ".html"
        # User-Agent头
        user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
        headers = {'User-Agent': user_agent}
        
        # 创建请求
        req = urllib2.Request(url, headers = headers)
        # 发送请求
        response = urllib2.urlopen(req)
        # 读取内容
        html = response.read()
        # 将gb2312转码为utf-8
#         html = unicode(html, 'gb2312').encode('utf-8')
        gbk_html = html.decode('gbk').encode('utf-8')
        
        #找到所有的段子内容<div class = "f18 mb20"></div>
        #re.S 如果没有re.S 则是只匹配一行有没有符合规则的字符串，如果没有则下一行重新匹配
        # 如果加上re.S 则是将所有的字符串将一个整体进行匹配
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        item_list = pattern.findall(gbk_html)
        # 返回匹配的列表
        return item_list
        
        
    def printOnePage(self, item_list, page):
        """
            @brief 处理得到的段子列表
            @param item_list 得到的段子列表
            @param page 处理第几页
        """
        print "******第  %d 页  爬取完毕...******" %page
        for item in item_list:
            # 替换多于的字符
            item = item.replace("<p>", "").replace("</p>", "").replace("<br />", "").replace("&ldquo;", "").replace("&rdquo;", "").replace("&hellip;", "")
            self.writeTofile(item)
            
    
    def writeTofile(self, text):
        """
            @brief 将数据追加写进文件中
            @param text: 文件内容
        """
        my_file = open("./duanzi.txt", 'a') # 追加形式打开文件
        my_file.write(text)
        my_file.write("--------------------------------------------------")
        my_file.close()
    
    
    def doWork(self):
        """
                        让爬虫开始工作
        """
        while self.enable:
            try:
                item_list = self.loadpage(self.page)
            except urllib2.URLError, e:
                print e.reason
                continue
            
            # 对得到的段子item_list 处理
            self.printOnePage(item_list, self.page)
            self.page += 1 # 此页处理完，处理下一页
            print "按回车继续"
            print "输入 quit 退出"
            command = raw_input()
            if (command == "quit"):
                self.enable = False
                break
    
    
if __name__ == '__main__':
    """
        ========================
                            内涵段子小爬虫
        ========================
    """
    print "请按下回车开始"
    raw_input()
    
    # 定义一个Spider对象，并且从第一页开始爬取
    mySpider = Spiser(1)
    # 调用doWork函数，开始爬取
    mySpider.doWork()

    
    
    
    
    
    
    
    