import scrapy
from parsel import Selector
from selenium.common.exceptions import NoSuchElementException
from hospital.items import HospitalItem
from hospital.items import DoctorItem
from selenium import webdriver


class DeptSpider(scrapy.spiders.Spider):
    name="dept"
    allowed_domains = ["guahao.com"]
    start_urls=["http://www.guahao.com/hospital/125336070937502000"]


    def isExit(self,browser,xpath):
        try :
            browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException as e:
            return False



    def searchDoc(self,page,browser):
        doctors=Selector(page).xpath("//div[@class='g-doctor-item2 g-clear to-margin']")
        for sel in doctors:
            item=DoctorItem()
            item['docImage']=sel.xpath("div[@class='g-doc-baseinfo g-left']/a/img/@src").extract_first()
            item['docName']=sel.xpath("div[@class='g-doc-baseinfo g-left']/dl/dt/text()[2]").extract_first()
            item['docTitle']=sel.xpath("div[@class='g-doc-baseinfo g-left']/a/img/@alt").extract_first()
            item['docType']=Selector(page).xpath("//a[@monitor='fastorder_head,fastorder_head,div']/text()").extract_first()
            item['docScore']=sel.xpath("div[@class='num-info g-left']/div[@class='stars']/em/text()").extract_first()
            item['docDec']=sel.xpath("div[@class='skill g-left']/text()[2]").extract_first()
            # print item
            yield item


        if(self.isExit(browser,"//a[@class='J_pageNum_gh']")):

            next_page=browser.find_elements_by_xpath("//a[@class='J_pageNum_gh']")
            for page in next_page:
                page.click()
                self.searchDoc(browser.page_source, browser)
        else:
            return


    def searchDoc2(self,page,browser):

        doctors=Selector(page).xpath("//div[@class='g-hddoctor-list g-clear js-tab-content']/div[@class='g-clear g-doc-info']")
        for sel in doctors:
            item = DoctorItem()
            item['docImage'] = sel.xpath("a/img/@src").extract_first()
            item['docName'] = sel.xpath("a/img/@alt").extract_first()
            item['docTitle'] = sel.xpath("dl/dt/span/text()").extract_first()
            item['docType'] = Selector(page).xpath("//div[@id='g-breadcrumb']/span/text()").extract_first()
            item['docScore'] = sel.xpath("dl/dd/a/span[6]/text()").extract_first()
            item['docDec'] = sel.xpath("dl/dd/p/text()").extract_first()
            yield item
            # items.append(item)



    def parse(self,response):

        # extract the classfy dept
        for sel in response.xpath('//li[@class="g-clear"]'):
            item = HospitalItem()
            # item['type']=sel.xpath(".//label/text()").extract()[0]
            # item['name']=sel.xpath('.//p/span/a[@class="ishao"]/text()').extract()[0]
            # yield item

        links=response.xpath("//a[@class='ishao']/@href").extract()
        browser=webdriver.Chrome()
        for link in links:
            print "*****"+link
            browser.get(link)
            more= self.isExit(browser, "//div[@class='more']/a")
            if(more):

                browser.find_element_by_xpath("//div[@class='more']/a").click()
                content = browser.page_source
                for i in self.searchDoc(content, browser):
                    yield i

            else:
                self.searchDoc2(browser.page_source,browser)






