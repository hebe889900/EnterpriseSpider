# -*- coding: utf-8 -*-
import scrapy


class UbaikeSpider(scrapy.Spider):
    name = 'ubaike'
    allowed_domains = ['ubaike.cn']
    start_urls = ['http://ubaike.cn/']

    def parse(self, response):
        pass
