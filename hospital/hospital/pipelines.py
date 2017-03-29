# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
import pymongo
from scrapy.conf import settings

# write data into related file
class HospitalPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # self.file = open('items.json', 'wb')
        # self.file = codecs.open('items.json', 'w', encoding='utf-8')
        self.commentfile=codecs.open('comments.json','w',encoding='utf-8')
        self.docfile=codecs.open('doctor.json','w',encoding='utf-8')
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL1']]  # 获得collection的句柄


    def spider_opened(self, spider):
        print "i am opened"
        # 链接数据库
        if(spider.name=="comments"):
            self.coll = self.db[settings['MONGO_COLL']]
        #
        # if(spider.name=="dept"):
        #     self.col = self.db[settings['MONGO_COLL1']]



    def process_item(self, item, spider):

        if(spider.name=="comments"):

            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.commentfile.write(line)


        if(spider.name=="dept"):
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.docfile.write(line)
            postItem = dict(item)
            self.coll.insert(postItem)
            return item

        # postItem = dict(item)
        # self.col.insert(postItem)
        # return item

    def spider_closed(self, spider):

        print "i am closed"
        if (spider.name == "comments"):

            self.commentfile.close()

        if (spider.name == "dept"):
            self.docfile.close()
            self.db.close()


# handle the item data,remove the duplicated item and remove the \n\r\t characters
class DoctorPipeline(object):
    def __init__(self):

        self.collection=set()

    def process_item(self, item, spider):

        if(spider.name=="comments"):
            if item['time'] in self.collection:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.collection.add(item['time'])
                return item

        if(spider.name=="dept"):
            if item['docName'] in self.collection:
                raise DropItem("Duplicate item found: %s" % item)
            else:

                self.collection.add(item['docName'])
                return item

