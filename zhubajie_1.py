# -*- coding: utf-8 -*-
import re
import time
import random
import requests
import traceback
from lxml import etree
import urlparse
import urllib
import lxml.html
import pymysql.cursors
from lxml.cssselect import CSSSelector
import sys
defaultencode = 'utf-8'
reload(sys)
sys.setdefaultencoding(defaultencode)


connection = pymysql.connect(host='localhost', user='root', password='123456', db='spider_data',charset='utf8mb4')

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_uq=4946d13dcb8b4085b76ac84cf7789bc4; _ga=GA1.3.83826392.1548929770; _gid=GA1.3.499324826.1548929770; AGENT20180731jssdkcross=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22uniqueId%22%3A%22168a368a261c9c-0a40e39085ae5e-b781636-1fa400-168a368a2623f%22%2C%22domain%22%3A%22zbj.com%22%7D; AGENT20170621jssdkcross=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22uniqueId%22%3A%22168a368a0c383-0287cc133aec1a-b781636-1fa400-168a368a0c47f2%22%2C%22domain%22%3A%22zbj.com%22%7D; local_city_id=3673; local_city_path=suzhou; local_city_name=%E8%8B%8F%E5%B7%9E; stt_pmcode=; uniqid=d01n3incohmpo; __utma=168466538.83826392.1548929770.1548929770.1548987990.2; __utmc=168466538; __utmz=168466538.1548987990.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_a470338ce4acadcbff35fd90b013898f=1548929770,1548987990; zmId_1=%7B%22id%22%3A%22M5l7d%252BKsPfapK1lyGukjDwzGyx7T8ymC%252BiuWoXFd05OShyDoKUrlIR2Gs%252FTD4qmxw4U%252FDL%252F%252FezNKK7HC90GdfzASY%252FeNlsbSnzM581kKqjp8QbWFs3xAlxFRq9kWJhgttZ9LT6EMNis%252FImkiNt23ziR6%252F2VUSfsvLNgvy3b55pGvpKGFid13og%253D%253D%22%2C%22productId%22%3A1%2C%22clickTime%22%3A1548988125076%7D; _uv=2; stt_outreferer=; stt_firstpage=https%3A//suzhou.zbj.com/search/p/%3Ftype%3Dnew%26kw%3D%25E7%25BD%2591%25E7%25AB%2599%25E4%25BB%258B%25E7%25BB%258D; _gat=1; __utmt=1; zhaoshang-title-last-time=1548950400000; __utmb=168466538.19.10.1548987990; Hm_lpvt_a470338ce4acadcbff35fd90b013898f=1548988665; AGENT20180731session=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22sessionId%22%3A%22168a6e1021e112-0c1409f3850a18-b781636-1fa400-168a6e1021f66c%22%2C%22CURRENT_EVENT_ID%22%3A%22168a6eb4f8ac55-07f753246a6a64-b781636-1fa400-168a6eb4f8b42e%22%2C%22token%22%3A%22168a6e1021e112-0c1409f3850a18-b781636-1fa400-168a6e1021f66c%22%2C%22monitor_auth%22%3Atrue%2C%22monitor_authing%22%3Afalse%2C%22monitor_sending%22%3Afalse%7D; AGENT20170621session=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22sessionId%22%3A%22168a6e0ffd2876-0b0dc142baca8f-b781636-1fa400-168a6e0ffd3269%22%2C%22CURRENT_EVENT_ID%22%3A%22168a6eb95d7857-06d9bb78945ad3-b781636-1fa400-168a6eb95d8637%22%2C%22monitor_authing%22%3Afalse%2C%22monitor_auth%22%3Atrue%2C%22token%22%3A%22NRHD4NWHD6D524H4GGSSR59656G56WH5%22%2C%22monitor_sending%22%3Afalse%7D',
    'Host': 'suzhou.zbj.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


class Zhubajie(object):


    def __init__(self):
        self.headers = headers
        self.start_url = 'https://suzhou.zbj.com/search/p/{}?type=new&kw={}'
        self.kw = '网站介绍'


    def set_page(self):
        '''设置页数'''
        page_1 = ''
        page_list = []
        page_list.append(page_1)
        kw = 'k{}.html'
        for i in range(2,101):
            page =kw.format((i-2)*40+34)
            page_list.append(page)
        return page_list


    def get_page_url(self, href):
        '''
        获取每一页上所有公司的url
        return ：list列表，存放此页所有公司的url
        '''
        response = requests.get(href, headers=headers, timeout=5, allow_redirects=False)
        status_code = response.status_code
        if status_code in [301,302]:
            print('get page url happen redirects, before url:' + href, 'redirects url:' + response.headers['Location'])
            return href
        tree = lxml.html.fromstring(response.text)
        try:
            com_obj = tree.cssselect("div.item-wrap")
            page_com_url = []  # 用于存放此页公司的url
            for obj in com_obj:
                item=obj.cssselect('h4 a.name')
                if len(item) == 0:  # 无效的跳过
                    continue
                com_url = item[0].attrib['href']  # 公司url
                page_com_url.append('https:'+com_url)
            return page_com_url
        except Exception as e:
            print('get page url error', traceback.print_exc())


    def extractor_html(self, com_url):
        '''
        解析公司的url
        return:  标题信息/公司名/公司地址/公司简介/公司标签
        '''
        headers['Host'] = 'shop.zbj.com'
        headers['Cookie'] = '_uq=4946d13dcb8b4085b76ac84cf7789bc4; AGENT20180731jssdkcross=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22uniqueId%22%3A%22168a368a261c9c-0a40e39085ae5e-b781636-1fa400-168a368a2623f%22%2C%22domain%22%3A%22zbj.com%22%7D; AGENT20170621jssdkcross=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22uniqueId%22%3A%22168a368a0c383-0287cc133aec1a-b781636-1fa400-168a368a0c47f2%22%2C%22domain%22%3A%22zbj.com%22%7D; local_city_id=3673; local_city_path=suzhou; local_city_name=%E8%8B%8F%E5%B7%9E; uniqid=d01n3incohmpo; __utmc=168466538; shop-im-tip=true; _ga=GA1.3.83826392.1548929770; _gid=GA1.3.1945140788.1548988122; zhaoshang-title-last-time=1548950400000; stt_pmcode=; Hm_lvt_a470338ce4acadcbff35fd90b013898f=1548929770,1548987990,1548989394; zmId_1=%7B%22id%22%3A%22M5l7d%252BKsPfapK1lyGukjDwzGyx7T8ymCdFH1K8eIeo3Ly9wxhQlHykavDrQ9eLkrffzQEfPsIf9KK7HC90GdfzASY%252FeNlsbSKitgDo6oAa%252BzTCsENnWLS7tMhVSgJJInpJeCJefjHW5M7WjVR7yBV8rPXQGfVvgrMaV3DECQdIZSQlJW9lU20w%253D%253D%22%2C%22productId%22%3A1%2C%22clickTime%22%3A1548990607569%7D; stt_outreferer=; __utmz=168466538.1549004935.5.3.utmcsr=suzhou.zbj.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/p/; __utma=168466538.83826392.1548929770.1549004935.1549008448.6; __utmt=1; _uv=11; stt_firstpage=https%3A//shop.zbj.com/18105392/%3Ffr%3Ddjwy; AGENT20170621session=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22sessionId%22%3A%22168a6e0ffd2876-0b0dc142baca8f-b781636-1fa400-168a6e0ffd3269%22%2C%22CURRENT_EVENT_ID%22%3A%22168a8214c5e986-0f12c2fcab7a92-b781636-1fa400-168a8214c5f6b7%22%2C%22monitor_authing%22%3Afalse%2C%22monitor_auth%22%3Atrue%2C%22token%22%3A%22NRHD4NWHD6D524H4GGSSR59656G56WH5%22%2C%22monitor_sending%22%3Afalse%7D; _gat=1; __utmb=168466538.2.10.1549008448; Hm_lpvt_a470338ce4acadcbff35fd90b013898f=1549008982; AGENT20180731session=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22sessionId%22%3A%22168a6e1021e112-0c1409f3850a18-b781636-1fa400-168a6e1021f66c%22%2C%22CURRENT_EVENT_ID%22%3A%22168a82150291af-00112b8e039479-b781636-1fa400-168a821502a178%22%2C%22token%22%3A%22168a6e1021e112-0c1409f3850a18-b781636-1fa400-168a6e1021f66c%22%2C%22monitor_auth%22%3Atrue%2C%22monitor_authing%22%3Afalse%2C%22monitor_sending%22%3Afalse%7D'
        response = requests.get(com_url, headers=headers, timeout=5, allow_redirects=False)
        if response.status_code == 404:
            return
        if response.status_code in [301,302]:
            print('extractor html happen redirects, before url:' + com_url, 'redirects url:' + response.headers['Location'])
            # com_url = response.headers['Location']
            # response = requests.get(com_url, headers=headers, timeout=5, allow_redirects=False)
            self.insert(com_url, ' ', ' ', ' ', ' ')
            return com_url

        try:
            tree = lxml.html.fromstring(response.text)
            #---------获取公司标题---------#
            com_title_obj = tree.cssselect('h1.title')
            if com_title_obj != []:
                com_title = com_title_obj[0].text.strip()  # 公司的title
            else:  # 如果匹配不到公司标题，说明是另一种网页结构, 直接将网址插入数据库
                self.insert(com_url, ' ', ' ', ' ', ' ')
                return com_url

            #---------获取公司名---------#
            com_name_obj = tree.cssselect('div.content-item > div')
            if com_name_obj != []:
                com_name = com_name_obj[1].text.strip()
            else:
                com_name = ' '
            # for obj in com_name_obj:
            #     # if obj.text == u'\n公司名称：\n':
            # print(com_name)

            #---------获取公司标签---------#
            com_label_obj_1 = tree.cssselect('div.right-wrap div.tag-wrap > div')
            com_label_obj_2 = tree.cssselect('div.right-wrap div.tag-wrap > div.new-tag > span')
            if com_label_obj_1 != [] and com_label_obj_2 != []:
                labels = ''
                for label in com_label_obj_1[0:-1]:  # 最后一项脏数据
                    if label.text == None:
                        continue
                    if label.text != '\n':
                        labels += label.text.strip() + ' '
                for label in com_label_obj_2:
                    if label.text == None:
                        continue
                    labels += label.text + ' '
            else:
                labels = ' '

            #---------获取公司地址---------#
            com_addr_obj = tree.cssselect('div.address-wrap')
            if len(com_addr_obj) != 0:  # 判断是不是有地址
                print com_addr_obj[0].text
                if com_addr_obj != []:
                    first_city = com_addr_obj[0].cssselect('span.city-text')[0].tail  # "一级城市"
                    sec_city = com_addr_obj[0].cssselect('span.city-text')[0].text  # “二级城市”
                else:
                    first_city = ' '
                    sec_city = ' '
                com_city = sec_city + ' ' + first_city
            else:  # 若没有地址则为空
                com_city = ' '

            #---------获取公司介绍---------#
            com_introduce_obj = tree.cssselect('pre.content-item')
            if com_introduce_obj != []:
                com_introduce = com_introduce_obj[0].text.strip()  # 公司介绍
            else:
                com_introduce = ' '

            self.insert(com_title, com_name, com_city, labels, com_introduce)
        except Exception as e:
            print('extractor html error', traceback.print_exc())

    def insert(self, com_title, com_name, com_city, labels, com_introduce):
        '''
        向mysql数据库插入数据
        '''
        print(com_title.strip().encode('utf8'), com_name.strip().encode('utf8'), com_city.strip().encode('utf8'), labels.strip().encode('utf8'), com_introduce.strip().encode('utf8'))
        try:
            with connection.cursor() as c:
                c.execute("insert into zhubajie_data(com_title, com_name, com_city, labels, com_introduce) values('{}', '{}', '{}', '{}', '{}')".format(com_title.strip().encode('utf8'), com_name.strip().encode('utf8'), com_city.strip().encode('utf8'), labels.strip().encode('utf8'), com_introduce.strip().encode('utf8')))
            connection.commit()
        except Exception as e:
            print('insert into mysql error', traceback.print_exc())


    def run(self):
        kw = urllib.quote(self.kw)  # url编码
        page_list = self.set_page()  # 获取页码列表
        for page in page_list[-1]:
            href = self.start_url.format(page, kw)
            print('--href--', href)
            url_list = self.get_page_url(href)
            for url in url_list:
                print(url)
                self.extractor_html(url)
                time.sleep(random.randint(1, 3))

        # self.extractor_html(com_url= 'https://shop.zbj.com/16634237/')


spider = Zhubajie()
spider.run()
