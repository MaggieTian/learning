import scrapy
from parsel import Selector
import re
from hospital.items import HospitalItem
from hospital.items import DoctorItem
from selenium import webdriver


class DeptSpider(scrapy.spiders.Spider):
    name="dept"
    allowed_domains = ["guahao.com"]
    start_urls=["http://www.guahao.com/hospital/125336070937502000"]


    def parse(self,response):

        # extract the classfy dept
        for sel in response.xpath('//li[@class="g-clear"]'):
            # item = HospitalItem()
            yield {

                'type':sel.xpath(".//label/text()").extract()[0],
                'name':sel.xpath('.//p/span/a[@class="ishao"]/text()').extract()

               }

        links=response.xpath("//a[@class='ishao']/@href").extract()
        browser=webdriver.Firefox()

        for link in links:
            browser.get(link)



    def parse_middle(self,res):

        link=res.xpath('//div[@class="more"]//a/@href')
        items=[]

        for i in link:
            item=DoctorItem()
            item['docName']=i.extract()
            items.append(item)
            return items
        # return scrapy.Request(link, callback=self.parse_doctor)

    def parse_doctor(self,res):

        docs=res.xpath("")





