# -*- coding: utf-8 -*-
import scrapy


class ClassSpider(scrapy.Spider):
    name = 'class'
    allowed_domains = ['219.230.159.132','jwcas.cczu.edu.cn']
    start_urls = ['http://219.230.159.132/web_jxrw/cx_kb_xsgrkb.aspx']

    def start_requests(self):
        cookies = "ASP.NET_SessionId=cnnceln3g2ldis55lhjuyxrw"
        cookies = {i.split("=")[0]:i.split("="[1]) for i in cookies}
        # cookies = {"ASP.NET_SessionId":"cnnceln3g2ldis55lhjuyxrw"}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        tr_list = response.xpath("//div[@id='UpdatePanel4']//tr[@class='dg1-item']")
        jie = 1
        item = [[0 for i in range(6)] for i in range(10)]
        print(item)
        for tr in tr_list:
            item[jie][1] = tr.xpath("./td[2]/text()").extract_first()
            item[jie][2] = tr.xpath("./td[3]/text()").extract_first()
            item[jie][3] = tr.xpath("./td[4]/text()").extract_first()
            item[jie][4] = tr.xpath("./td[5]/text()").extract_first()
            item[jie][5] = tr.xpath("./td[6]/text()").extract_first()
            jie +=1
        for i in range(9):
            for j in range(5):
                print(item[i+1][j+1],end="     ")
            print()