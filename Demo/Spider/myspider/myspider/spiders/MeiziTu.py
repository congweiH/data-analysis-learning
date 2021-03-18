# -*- coding: utf-8 -*-
import scrapy
import time
import os

class MeizituSpider(scrapy.Spider):
    name = 'MeiziTu'
    allowed_domains = ['mzitu.com','i5.meizitu.net']
    start_urls = ['https://www.mzitu.com/201554']

    def parse(self, response):
        item = {}
        item["title"] = response.xpath("//div[@class='currentpath']//text()").extract()[4].replace(" » ","")
        item["img_url"] = response.xpath("//div[@class='main-image']//a/img/@src").extract_first()
        item["img_name"] = item["img_url"].split("/")[-1]
        if item["img_url"] !=None:
            time.sleep(0.3)
            yield scrapy.Request(
                item["img_url"],
                callback=self.save_img,
                meta={"item":item}
            )
        # 构造下一页的请求
        next_url = response.xpath("//div[@class='pagenavi']//a[span[text()='下一页»']]/@href").extract_first()
        print(next_url)
        if next_url != None:
            time.sleep(0.3)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def save_img(self, response):
        item = response.meta["item"]
        dir = item["title"]
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(dir+"/"+item["img_name"],"wb") as f:
            f.write(response.body)

