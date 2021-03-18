# -*- coding: utf-8 -*-
import scrapy


class BaidufanyiSpider(scrapy.Spider):
    name = 'BaiduFanyi'
    allowed_domains = ['219.230.159.132','jwcas.cczu.edu.cn']
    start_urls = ['http://219.230.159.132/web_jxrw/cx_kb_xsgrkb.aspx']

    def start_requests(self):
        # cookies = "ASP.NET_SessionId=cnnceln3g2ldis55lhjuyxrw"
        # cookies = {i.split("=")[0]:i.split("="[1]) for i in cookies.split("; ")}
        cookies = {"ASP.NET_SessionId":"cnnceln3g2ldis55lhjuyxrw"}
        yield scrapy.FormRequest(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        print("*"*200)
