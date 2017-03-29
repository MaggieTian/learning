#coding=utf-8
import codecs
import json
import pymongo
import scrapy
from parsel import Selector
from selenium.common.exceptions import NoSuchElementException
from hospital.items import HospitalItem
from hospital.items import DoctorItem
from selenium import webdriver
import re
from scrapy.conf import settings


class DeptSpider(scrapy.spiders.Spider):
    name="type"
    allowed_domains = ["guahao.com"]
    start_urls=["http://www.guahao.com/hospital/125336070937502000"]


    def remove_char(self, item):
        if item is not None:
            pattern = re.compile("[\n\r\t]")
            str = pattern.sub("", item.strip())
            return str
        else:
            return item
    def __init__(self):
        self.file = codecs.open('dept.json', 'w', encoding='utf-8')
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL2']]  # 获得collection的句柄

    def parse(self,response):



        # extract the classfy dept
        for sel in response.xpath('//li[@class="g-clear"]'):
            items = [];
            item = HospitalItem()
            item['type']=self.remove_char(sel.xpath("label/text()").extract_first())
            for i in sel.xpath('p/span/a[@class="ishao"]/text()').extract():
                items.append(self.remove_char(i))
            item['name']=items
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            postItem = dict(item)  # 把item转化成字典形式
            self.coll.insert(postItem)  # 向数据库插入一条记录

        self.file.close()
        # self.db.close()







