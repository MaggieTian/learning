#coding=utf-8
import re

import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from hospital.items import CommentItem


class CommentSpider(scrapy.spiders.Spider):
    name="comments"
    allowed_domains = ["guahao.com"]
    login_url="http://www.guahao.com/user/login?target=%2Fcommentslist%2Fh-125336070937502000%2F1-0"
    start_urls = ["http://www.guahao.com/commentslist/h-125336070937502000/1-0"]
    verifyCode=''

    # this method is used to remove the \r\n\t character
    def remove_char(self,item):
        if item is not None:
            pattern = re.compile("[\n\r\t]")
            str = pattern.sub("", item.strip())
            return str
        else:
            return item

    # this method is used to jude whether the element with xpath exist or not

    def isExit(self,browser,xpath):
        try:
            browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException as e:
            return False

    def extract_info(self,page,driver):

        # next_page = Selector(page).xpath("//a[@class='next J_pageNext_gh']").extract()
        next_page=self.isExit(driver, "//a[@class='next J_pageNext_gh']")

        if next_page:

            users = Selector(text=page).xpath("//ul[@id='comment-list']/li")
            for user in users:
                item = CommentItem()
                item['photo'] = self.remove_char(user.xpath("div[@class='user']/img/@src").extract_first())
                item['name'] = self.remove_char(user.xpath("div[@class='user']/p/text()").extract_first())
                item['disease'] = self.remove_char(user.xpath("div[@class='row-1']/p[@class='disease']/span/text()").extract_first())
                item['waitTime'] = self.remove_char(user.xpath("div[@class='row-1']/p[@class='attitude']/strong/text()").extract_first())
                item['service'] = self.remove_char(user.xpath("div[@class='row-1']/p[@class='effect']/strong/text()").extract_first())
                item['doctor'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='info']/p//a[@class='name']/text()").extract_first())
                item['time'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='info']/p/span[1]/text()").extract_first())
                item['content'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='text']/span/text()").extract_first())
                yield item
            driver.find_element_by_xpath("//a[@class='next J_pageNext_gh']").click()
            time.sleep(20)  # 设置时延以确保页面加载完
            driver.execute_script("window.scrollBy(0,3000)")  # 滑动滚动条以确保页面加载完
            for i in self.extract_info(driver.page_source,driver):
                yield i
        #最后一页
        else:
            if(self.isExit(driver,"//ul[@id='comment-list']/li")):
                users = Selector(text=page).xpath("//ul[@id='comment-list']/li")
                for user in users:
                    item = CommentItem()
                    item['photo'] = self.remove_char(user.xpath("div[@class='user']/img/@src").extract_first())
                    item['name'] = self.remove_char(user.xpath("div[@class='user']/p/text()").extract_first())
                    item['disease'] = self.remove_char( user.xpath("div[@class='row-1']/p[@class='disease']/span/text()").extract_first())
                    item['waitTime'] = self.remove_char(user.xpath("div[@class='row-1']/p[@class='attitude']/strong/text()").extract_first())
                    item['service'] = self.remove_char(user.xpath("div[@class='row-1']/p[@class='effect']/strong/text()").extract_first())
                    item['doctor'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='info']/p//a[@class='name']/text()").extract_first())
                    item['time'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='info']/p/span[1]/text()").extract_first())
                    item['content'] = self.remove_char(user.xpath("div[@class='row-2']/div[@class='text']/span/text()").extract_first())
                    yield item
            driver.save_screenshot("over.jpg") #截图以查看最后结果是否是正常退出
            return

    def parse(self, response):

        #登录
        driver = webdriver.Chrome()
        driver.get(self.login_url)
        driver.find_element_by_xpath("//input[@id='loginId']").send_keys("13248226806")
        driver.find_element_by_xpath("//input[@id='password' and @class='form-input']").send_keys("tianqi57714670")
        driver.save_screenshot("validate.jpg")#登陆页面截图用以后面的手动输入验证码
        self.verifyCode = str(raw_input("***please input the verify code in the screeshot picture"))
        driver.find_element_by_xpath("//input[@id='validCode']").send_keys(self.verifyCode)
        driver.find_element_by_xpath("//input[@id='validCode']").send_keys(Keys.ENTER)
        try:
            driver.find_element_by_xpath("//a[@class='next J_pageNext_gh']")
            print "*****login success!"

        except NoSuchElementException as e:
            print "******login failed!"

        for i in self.extract_info(driver.page_source, driver):#开始提取登录以后的页面数据
            yield i



















