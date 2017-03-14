# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class HospitalPipeline(object):
    def __init__(self):
        # self.file = open('items.json', 'wb')
        self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):

        if (spider.name=="comments"):

            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.file.write(line)
            return item

    def spider_closed(self, spider):
        self.file.close()



class DoctorPipeline(object):
    def __init__(self):
        # self.file = open('doctor.json', 'wb')
        self.file = codecs.open('doctor.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):

        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()