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
    docTitle = scrapy.Field()
    docDec = scrapy.Field()
    docScore = scrapy.Field()
    docImage= scrapy.Field()
    docType=scrapy.Field()

class CommentItem(scrapy.Item):

    photo=scrapy.Field()
    name=scrapy.Field()
    disease=scrapy.Field()
    waitTime=scrapy.Field()
    service=scrapy.Field()
    doctor=scrapy.Field()
    time=scrapy.Field()
    content=scrapy.Field()




