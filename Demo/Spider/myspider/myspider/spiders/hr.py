# -*- coding: utf-8 -*-
import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            item = {}
            item["title"] = tr.xpath("./td[1]/a/text()").extract_first()
            item["position"] = tr.xpath("./td[2]/text()").extract_first()
            item["publish_date"] = tr.xpath("./td[5]/a/text()").extract_first()
            yield item
        # 找到下一页的url
        next_url= response.xpath("//a[@id='next'/@href]").extract_first()
        if next_url != "javascript":
            yield scrapy.Request(
                next_url,
                callback=self.parse  # 下一页处理方式一样，所以返给自己
                # 如果处理方式不一样，可以另外写一个回调函数
            )
