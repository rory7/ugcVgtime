# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.log import logger

from ugcVgtime.items import UgcvgtimeItem
from ugcVgtime.spiders import cookie

'''vgtime-topic首页目录item爬取'''
'''这个爬虫还有些许问题需要解决，但是目前可以正常使用'''


class TopicSpider(scrapy.Spider):
    name = "topicSpider"
    allowed_domains = ["new.vgtime.com"]
    start_urls = ['http://new.vgtime.com/topic/index.jhtml',
                  'http://new.vgtime.com/topic/index/load.jhtml?page=2&pageSize=12',
                  'http://new.vgtime.com/topic/index/load.jhtml?page=3&pageSize=12']

    '''post 请求更多页面-目前每次多请求 3 页'''
    isFristRequest = False
    comTitle = []
    comUrl = []
    comIamge = []

    def parse(self, response):
        item = UgcvgtimeItem()

        if response.url == self.start_urls[0]:
            sel = scrapy.Selector(response)
            title = sel.xpath("//li/div[@class='info_box']/a/h2/text()").extract()
            url = sel.xpath("//li/div[@class='info_box']/a/@href").extract()
            finalUrl = []
            for u in url:
                if u.startswith("http://"):
                    finalUrl.append(u)
                else:
                    u = "http://new.vgtime.com" + u
                    finalUrl.append(u)

            image = sel.xpath("//li/div[@class='img_box']/a/img/@src").extract()

            self.comTitle.extend(title)
            self.comIamge.extend(image)
            self.comUrl.extend(finalUrl)

            # logger.info("11111!!!!=" + self.comUrl.__str__())
        else:
            data = response.body
            jsonData = json.loads(data)
            retcode = jsonData['retcode']
            htmlData = jsonData['data']

            # logger.info("reqeuest!!!=" + retcode.__str__() + "\n" + htmlData)

            if retcode == 200:
                sel = scrapy.Selector(text=htmlData)

                title = sel.xpath("//li/div[@class='info_box']/a/h2/text()").extract()
                url = sel.xpath("//li/div[@class='info_box']/a/@href").extract()
                finalUrl = []
                for u in url:
                    if u.startswith("http://"):
                        finalUrl.append(u)
                    else:
                        u = "http://new.vgtime.com" + u
                        finalUrl.append(u)

                image = sel.xpath("//li/div[@class='img_box']/a/img/@src").extract()

                self.comTitle.extend(title)
                self.comIamge.extend(image)
                self.comUrl.extend(finalUrl)
                # logger.info("11111!!!!=" +self.comUrl.__str__())
                if response.url == self.start_urls[2]:
                    item['title'] = self.comTitle
                    item['url'] = self.comUrl
                    item['image'] = self.comIamge
                    yield item
                else:
                    pass
        pass
