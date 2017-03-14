#coding=utf-8
import cookielib
import urllib
import urllib2
import scrapy
from selenium import webdriver

from hospital.items import CommentItem


class CommentSpider(scrapy.spiders.Spider):
    name="comment"
    allowed_domains = ["guahao.com"]
    login_url="http://www.guahao.com/user/login?target=%2Fcommentslist%2Fh-125336070937502000%2F1-0"
    start_urls = ["http://www.guahao.com/commentslist/h-125336070937502000/1-0"]
    pageNo = 1
    headers={
    "Accept": "text/html, application/xhtml + xml, application/xml;q = 0.9, image/webp, */*;q = 0.8",
    "Accept - Encoding": "gzip, deflat",
    "Accept - Language": "zh - CN,zh;q = 0.8",
    "Cache - Control": "max - age = 0",
    "Content - Length": "143",
    "Content - Type": "application/x-www-form-urlencoded",
    "Host": "www.guahao.com",
    "Proxy - Connection": "keep - alive",
    # "Referer": "http://www.guahao.com/user/login",
    "User - Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    verifyCode=''

    # def start_requests(self):
    #
    #     # 保存有验证码的截图，用以后面的登录
    #     # cap = response.xpath("//a[@class='captcha J_Captcha J_RefreshCaptcha']/img/@src").extract()
    #     # driver = webdriver.Chrome()
    #     # driver.get("http://www.guahao.com" + "/validcode/genimage/1")
    #     # driver.save_screenshot("")
    #     return [scrapy.Request(self.login_url, meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self,response):

        url = "http://www.guahao.com" + "/validcode/genimage/1"
        # 以上是动态生成验证码的网址
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        html = response.read()
        f = open('./validate.jpg', 'wb')
        # 写入本地一个文本，ok
        f.write(html)
        f.close()

        print "please input your verify code from the screenshot"
        value=raw_input()
        self.verifyCode=str(value)

        formdata = {
                       "method": "dologin",
                       "target": "%2Fcommentslist%2Fh-125336070937502000%2F1-0",
                       "loginId": "13248226806",
                       "password": "tianqi57714670",
                       "validCode": self.verifyCode
                   }
        data = urllib.urlencode(formdata)
        PostUrl="http://www.guahao.com"+"/user/login"
        # 生成post数据 ?key1=value1&key2=value2的形式
        request = urllib2.Request(PostUrl, data, self.headers)
        # 构造request请求
        res = opener.open(request)
        print "****response"+res.read()
        return [scrapy.FormRequest.from_response(response,meta={'cookiejar':response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                "method": "dologin",
                "target": "%2Fcommentslist%2Fh-125336070937502000%2F1-0",
                "loginId": "13248226806",
                "password": "a7d857c10490c2cb5967af3d143831c2",
                "validCode": self.verifyCode
                 },
                callback=self.parse,
                dont_filter=True
                )]

    def parse(self, response):

        # print response.body
        next_page = response.xpath("//a[@class='next J_pageNext_gh']").extract()
        if(next_page is not None):
            users=response.xpath("//ul[@id='comment-list']/li")
            for user in users:

                item=CommentItem()
                item['photo']=user.xpath("div[@class='user']/img/@src").extract_first()
                item['name']=user.xpath("div[@class='user']/p/text()").extract_first()
                item['disease'] = user.xpath("div[@class='row-1']/p[@class='disease']/span/text()").extract_first()
                item['waitTime'] = user.xpath("div[@class='row-1']/p[@class='attitude']/strong/text()").extract_first()
                item['service'] = user.xpath("div[@class='row-1']/p[@class='effect']/strong/text()").extract_first()
                item['doctor'] = user.xpath("div[@class='row-2']/div[@class='info']/p//a[@class='name']/text()").extract_first()
                item['time'] = user.xpath("div[@class='row-2']/div[@class='info']/p/span[1]/text()").extract_first()
                item['content'] = user.xpath("div[@class='row-2']/div[@class='text']/span/text()").extract_first()
                yield item

            self.pageNo+=1
            sign = response.xpath("//input[@name='sign']/@value").extract_first()
            timestamp = response.xpath("//input[@name='timestamp']/@value").extract_first()
            print sign
            print timestamp
            yield scrapy.Request(url=self.start_urls[0]+"?pageNo="+str(self.pageNo)+"&sign="+sign+"&timestamp="+timestamp,callback=self.parse)

        else:
            return


















