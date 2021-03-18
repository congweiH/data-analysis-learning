# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['https://www.mzitu.com/189982']

    def parse(self, response):
        '''
        do something
        '''
        item = {}
        item["title"] = "xxx"
        item["href"] = "xxx"
        yield item
        # 通过一系列操作获取到url
        next_url = "http://www.xxx.com"
        yield scrapy.Request(
            next_url,
            callback=self.parse1,
            meta = {"item":item }
        )

    def parse1(self, response):
        response.meta["item"]  # 获取上面的item
