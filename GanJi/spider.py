# -*- coding: utf-8 -*-
import requests
import re
from config import *
from mysql import MySQL


# 实例化MySQL类
mysql = MySQL()


def get_page_html(url):
    """
        获取首页HTML源代码
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    return None



def getTypeURL(html):
    """
        提取成都招聘热门职位的URL
    """
    # 提取成都招聘热门职位<div class="f-hot"></div>
    # 正则
    print('-'*100)
    print('-----获取类别-----')
    pattern1 = re.compile('<div class="f-hot">([\s\S]*?)</div>', re.S)
    types_html = re.findall(pattern1, html)
    
    # 提取详细分类URL<a href="xx">xx</a>
    pattern2 = re.compile('<a .*?href="(.*?)".*?>(.*?)</a>', re.S)
    items = re.findall(pattern2, str(types_html))

    #print(items)
    # 添加到MySQL
    for item in items:
        # 遇到其他职位则跳过
        print()
        if item[1].find('其他') >= 0:
            continue
        
        print('得到类别：%s' % item[1])
        # 将类别名和url封装到字典
        data =  {
            'url': BASE_URL + item[0],
            'typename': item[1]
        }
        # 插入数据库
        mysql.insert('types_url', data)

        
def getJobsURL(types_url):
    """
        查询数据库获得类别的URL，根据类别URL获取职位的URL
    """
    print('='*100)

    for row in types_url:
        print('---------- 获取 %s 类工作 ----------' % (row[2]))
        # 获取分类HTML
        type_html = get_page_html(row[1])
        # 获取工作URL
        getJobURL(type_html)

        current_html = type_html
        # 获取类别的下一页，循环次数为NEXT_PAGE_NUM  ----- 如果需要爬取所有子页可以将数值设置为很大，也可以不设置数值，直接获取 "下一页"的url，直到没有
        # 获取类别的下一页，循环次数为NEXT_PAGE_NUM
        for i in range(NEXT_PAGE_NUM):
            #print(current_html)
            current_html = getNextPage(current_html)    # 返回值为当前页的下一页作为下次循环的当前页
            if current_html == None:
                break


def getJobURL(type_html):
    """
        根据类别页获取工作URL，并加入MySQL
    """
    print('获取job地址中...')
    # 正则提取工作URL <dl class="list-noimg job-list clearfix new-dl".*?>([\s\S]*?)</dl>
    pattern1 = re.compile('<dl class="list-noimg job-list clearfix new-dl"[\s\S]*?>[\s\S]*?<dt>([\s\S]*?)<div[\s\S]*?</dt>[\s\S]*?</dl>', re.S)
    jobs_html = re.findall(pattern1, type_html)

    # 提取每个工作的URL <a href="http://[\s\S]*?.ganji.com([\s\S]*?)"[\s\S]*?class="list_title gj_tongji"[\s\S]*?chargeUrl=[\s\S]*?>([\s\S]*?)</a>
    pattern2 = re.compile('href="http://[\s\S]*?.ganji.com([\s\S]*?)"[\s\S]*?post_url[\s\S]*?>([\s\S]*?)<', re.S)
    items = re.findall(pattern2, str(jobs_html))

    if items == None:
        return None
    else:
        # 添加到MySQL
        for item in items:

            # 去除垃圾URL，如公司URL
            other_url = None
            other_url = re.search(r'.*?gongsi.*?', item[0], re.M|re.I)
            
            # 没有匹配到垃圾URL则跳过本次循环
            if other_url != None:
                continue
            
            # 封装到字典
            data = {
                'url': BASE_URL + item[0],
                'jobname': item[1].strip()  # 去除首尾空白
            }
            # 加入数据库
            mysql.insert('jobs_url', data)


def getNextPage(current_html):
    """
        获取该类别的下一页
    """
    if current_html == None:
        return None
    # 提取分页ul <ul class="pageLink clearfix">([\s\S]*?)</ul>
    pattern1 = re.compile('<ul class="pageLink clearfix">([\s\S]*?)</ul>', re.S)
    url_html = re.findall(pattern1, current_html)
    
    # 该类别的分页  href="(.*?)"
    pattern2 = re.compile('href="(.*?)"', re.S)

    # 下页URL
    i = 0
    next_page_url = None
    for url in re.findall(pattern2, str(url_html)):
        next_page_url = str(url)

    # 获取工作URL
    if next_page_url != None:
        
        next_page_url = BASE_URL + next_page_url
        print('---------- 获取子页 %s ----------' % (next_page_url))

        next_page_html = get_page_html(next_page_url)
        getJobURL(next_page_html)
        # 返回下一页的HTML
        return next_page_html



def getJobInfo(jobs_url):
    """
        根据数据库得到的job URL得到相关信息，并存入MySQL
    """
    print('$'*100)
    print('获取工作详细信息中...')
    flag = 0
    for url in jobs_url:

        print(url[1])
        html = str(get_page_html(url[1]))

        #html = get_page_html('http://cd.ganji.com/zpshichangyingxiao/2759567089x.htm')
        if html == None:
            continue
        # 职位
        jobname = re.search(r'<div class="title-line clearfix">[\s\S]*?<p>([\s\S]*?)</p>([\s\S]*?)</div>', html, re.M|re.I)
        if jobname == None:
            jobname = 'null'
        else:
            jobname = jobname.group(1)
        
        # 工资
        salary = re.search(r'<div class="salary-line">[\s\S]*?<b>([\s\S]*?)</b>[\s\S]*?<i>([\s\S]*?)</i>[\s\S]*?</div>', html, re.M|re.I)
        if salary == None:
            salary = 'null'
        else:
            salary = salary.group(1) + salary.group(2)

        # 公司名称
        company = re.search(r'<div class="company-info">[\s\S]*?<h3>[\s\S]*?<a[\s\S]*?>([\s\S]*?)</a>[\s\S]*?</h3>[\s\S]*?</div>', html, re.M|re.I)
        if company == None:
            company = 'null'
        else:
            company = company.group(1)

        # 工作地点
        location = re.search(r'<div class="location-line clearfix">[\s\S]*?<p>([\s\S]*?)<[\s\S]*?</p>[\s\S]*?</div>', html, re.M|re.I)
        if location == None:
            location = 'null'
        else:
            location = location.group(1).strip().replace(' ', '')

            print("^"*20)
            print("需要验证（如果无需验证直接回车）...")
            print("验证后回车继续...", end='')
            input()
            print("/n^"*20)
            continue

        data = {
            'name': jobname,
            'salary': salary,
            'company': company,
            'location': location
        }
        mysql.insert('jobs_info', data)

        # 打印
        flag = flag + 1
        if (flag % 100) == 0:
            print('='*20, end='')
            print(' 已存储: %s ' % (flag), end='')
            print('='*20)





def main():
    """
        主函数
    """
    
    # 1.获取首页HTML源代码
    html = get_page_html(BASE_URL + '/zhaopin')
    if html == None:
        print('获取首页失败!')
        exit(0)
    #print(html)

    # 2.提取HTML代码，获得成都招聘热门职位的URL，并加入MySQL
    getTypeURL(html)

    # 3.从数据库获取类别的URL，提取每个类别下的职位URL
    types_url = mysql.select('types_url', None)
    getJobsURL(types_url)

    # 4.从数据库获取职位的URL，得到HTML获取相关信息并加入MySQL
    jobs_url = mysql.select('jobs_url', None)
    getJobInfo(jobs_url)



if __name__ == '__main__':
    main()
