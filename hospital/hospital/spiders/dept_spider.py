#coding=utf-8

import codecs
import json

import pymongo
import scrapy
import time
from parsel import Selector
from selenium.common.exceptions import NoSuchElementException
from hospital.items import HospitalItem
from hospital.items import DoctorItem
from selenium import webdriver
import re

from scrapy.conf import settings


class DeptSpider(scrapy.spiders.Spider):
    name="dept"
    allowed_domains = ["guahao.com"]
    start_urls=["http://www.guahao.com/hospital/125336070937502000"]

    # def __init__(self):
        # self.file = codecs.open('doctor.json', 'w', encoding='utf-8')
        # self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL1']]  # 获得collection的句柄


    def isExit(self,browser,xpath):
        try:
            browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException as e:
            return False

            # this method is used to remove the \r\n\t character

    def remove_char(self, item):
        if item is not None:
            pattern = re.compile("[\n\r\t]")
            str = pattern.sub("", item.strip())
            return str
        else:
            return item



    def searchDoc(self,page,browser):
        doctors=Selector(page).xpath("//div[@class='g-doctor-item2 g-clear to-margin']")
        for sel in doctors:
            item=DoctorItem()
            item['docImage']=self.remove_char(sel.xpath("div[@class='g-doc-baseinfo g-left']/a/img/@src").extract_first())
            item['docTitle']=self.remove_char(sel.xpath("div[@class='g-doc-baseinfo g-left']/dl/dt/text()[2]").extract_first())
            item['docName']=self.remove_char(sel.xpath("div[@class='g-doc-baseinfo g-left']/a/img/@alt").extract_first())
            item['docType']=self.remove_char(Selector(page).xpath("//a[@monitor='fastorder_head,fastorder_head,div']/text()").extract_first())
            item['docScore']=self.remove_char(sel.xpath("div[@class='num-info g-left']/div[@class='stars']/em/text()").extract_first())
            item['docDec']=self.remove_char(sel.xpath("div[@class='skill g-left']/text()[2]").extract_first())
            # print item
            yield item


        if(self.isExit(browser,"//a[@class='next J_pageNext_gh']")):

            next_page=browser.find_element_by_xpath("//a[@class='next J_pageNext_gh']")
            next_page.click()
            time.sleep(30)
            browser.execute_script("window.scrollBy(0,3000)")
            for j in self.searchDoc(browser.page_source, browser):
                yield j
        else:
            return


    def searchDoc2(self,page,browser):

        doctors=Selector(page).xpath("//div[@class='g-hddoctor-list g-clear js-tab-content']/div[@class='g-clear g-doc-info']")
        for sel in doctors:
            item = DoctorItem()
            item['docImage'] = self.remove_char(sel.xpath("a/img/@src").extract_first())
            item['docName'] = self.remove_char(sel.xpath("a/img/@alt").extract_first())
            item['docTitle'] = self.remove_char(sel.xpath("dl/dt/span/text()").extract_first())
            item['docType'] = self.remove_char(Selector(page).xpath("//div[@id='g-breadcrumb']/span/text()").extract_first())
            item['docScore'] = self.remove_char(sel.xpath("dl/dd/a/span[6]/text()").extract_first())
            item['docDec'] = self.remove_char(sel.xpath("dl/dd/p/text()").extract_first())
            yield item
            # items.append(item)



    def parse(self,response):

        links=response.xpath("//a[@class='ishao']/@href").extract()
        browser=webdriver.Chrome()
        for link in links:
            print "*****"+link
            browser.get(link)
            time.sleep(30)
            more= self.isExit(browser, "//div[@class='more']/a")
            if(more):

                browser.find_element_by_xpath("//div[@class='more']/a").click()
                time.sleep(30)
                browser.execute_script("window.scrollBy(0,3000)")
                content = browser.page_source
                for i in self.searchDoc(content, browser):
                    yield i
                    # line = json.dumps(dict(i), ensure_ascii=False) + "\n"
                    # self.file.write(line)
                    # postItem = dict(i)  # 把item转化成字典形式
                    # self.coll.insert(postItem)  # 向数据库插入一条记录



            else:
                for sel in self.searchDoc2(browser.page_source,browser):
                    yield sel
                    # line2 = json.dumps(dict(sel), ensure_ascii=False) + "\n"
                    # self.file.write(line2)
                    # postItem = dict(i)  # 把item转化成字典形式
                    # self.coll.insert(postItem)  # 向数据库插入一条记录

        # self.file.close()
        # self.db.close()







