# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from scrapy.http import HtmlResponse
from lxml import etree
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice

ua_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
        ]

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 15 
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        print (spider.name)
        driver = webdriver.PhantomJS()
        if spider.name == 'wangyiyun':
            try:
                driver.get(request.url)
                driver.implicitly_wait(3)
                time.sleep(5)
                driver.switch_to_frame('g_iframe')
                driver.find_element_by_xpath('//*[@id="flag_ctrl"]').click()  # 数据由js来控制,点击后加载数据
                true_page = driver.page_source
                driver.close()
                return HtmlResponse(request.url,body = true_page,encoding = 'utf-8',request = request,)
            except:
                print ("get Qua data failed")