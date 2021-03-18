# coding:utf-8
import requests
from lxml import etree
import json
import os
import time

class MeiziTu:
    def __init__(self,start_url=None,categry="default",):
        self.start_url = start_url
        self.categry = categry
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "Referer": start_url,
        }

    def get_menu_list(self,main_url):
        html_str = self.parse_url(main_url).decode()
        html = etree.HTML(html_str)
        li_list = html.xpath("//ul[@id='menu-nav']//li[position()>1]")
        total_menu_list = []
        for li in li_list:
            item = {}
            item["categry"] = li.xpath("./a/@title")[0]
            item["href"] = li.xpath("./a/@href")[0]
            total_menu_list.append(item)
        return total_menu_list

    def parse_url(self,url):  # 发送请求，获取响应
        print(url)
        time.sleep(0.3)
        r = requests.get(url,headers=self.headers)
        return r.content

    def get_page_num(self,url):
        html_str = self.parse_url(url)
        html = etree.HTML(html_str)
        page_num = html.xpath("//div[@class='pagenavi']//a[last()-1]/span/text()")[0]
        return int(page_num)

    def get_content_list(self,html_str): # 提取数据
        html = etree.HTML(html_str)
        div_list = html.xpath("//ul[@id='pins']/li") #分组
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./span/a/text()")[0] if len(div.xpath("./span/a/text()"))>0 else None
            item["href"] = div.xpath("./span/a/@href")[0] if len(div.xpath("./span/a/@href"))>0 else None
            item["img_list"] = self.get_img_list(item["href"])
            self.save_content(item)
            self.save_img(item["title"],item["img_list"])

        next_url = html.xpath("//a[text()='下一页»']/@href")[0] if len(html.xpath("//a[text()='下一页»']/@href"))>0 else None
        return next_url

    def get_img_list(self,detail_url):
        img_url_list = []
        page_num = self.get_page_num(detail_url)
        url_list = [detail_url+"/{}".format(i+1) for i in range(page_num)]
        for url in url_list:
            html_str = self.parse_url(url).decode()
            html = etree.HTML(html_str)
            img_url = html.xpath("//div[@class='main-image']//img/@src")[0]
            img_url_list.append(img_url)
        return img_url_list

    def save_img(self,title,img_list):
        file_path = "./src/"+self.categry+"/"+title
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for img_url in img_list:
            if len(img_url) > 0:
                text_byte = self.parse_url(img_url)
                with open(file_path+"/"+img_url.split("/")[-1],"wb") as f:
                    f.write(text_byte)

    def save_content(self,content):
        file_path = "./meizi.txt"
        with open(file_path,"a") as f:
            f.write(json.dumps(content,ensure_ascii=False,indent=2))
            f.write("\n")

    def run(self): # 实现主要逻辑
        next_url = self.start_url
        while next_url is not None:
            # 2.获取请求
            html_str = self.parse_url(next_url)
            # 3.爬取数据,提取下一页的url
                # 3.1提取列表单的url
                # 3.2提取列表的url
            next_url = self.get_content_list(html_str)

    def run_detail(self):
        html_str = self.parse_url(self.start_url).decode()
        html = etree.HTML(html_str)
        title = html.xpath("//h2[@class='main-title']/text()")[0]
        img_url_list = self.get_img_list(self.start_url)
        self.save_img(title,img_url_list)

if __name__ == '__main__':
    # tmp = MeiziTu()
    # # 获取菜单分类
    # menu_list = tmp.get_menu_list("https://www.mzitu.com/")
    # # 对每个分类分别请求url
    # for menu in menu_list:
    #     print(menu)
    #     mezi = MeiziTu(menu["href"],menu["categry"])
    #     mezi.run()
    tmp = MeiziTu("https://www.mzitu.com/189982")
    tmp.run_detail()
