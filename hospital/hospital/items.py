# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()


class DoctorItem(scrapy.Item):

    docName = scrapy.Field()
    docSex = scrapy.Field()
    docTitle = scrapy.Field()
    docDes = scrapy.Field()
    docDcore = scrapy.Field()
    docImage= scrapy.Field()



