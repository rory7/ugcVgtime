# -*- coding: utf-8 -*-
import json
from string import join

import scrapy
import time

from scrapy import Request
from scrapy import log
from scrapy.log import logger

from ugcVgtime.items import ArticleItem
from ugcVgtime.spiders import Constant
from ugcVgtime.spiders import cookie
from ugcVgtime.spiders.cookie import cookies

'''vgtime文章内容详情爬取'''


class UgcartSpider(scrapy.Spider):
    name = "ugcArtSpider"
    allowed_domains = ["new.vgtime.com"]
    start_urls = []

    def __init__(self):
        jf = open(Constant.ugcUrlJsonFile, "rb")
        data = json.load(jf)

        for item in data:
            self.start_urls.append(item['url'])

    # def start_requests(self):
    #     yield Request(self.start_urls[0], callback=self.parse, headers=cookie.headers, cookies=cookie.cookies,
    #                   meta=cookie.meta)

    def start_requests(self):
        for url in self.start_urls:
            logger.info("VGTIME-URL=" + url.__str__())
            yield scrapy.Request(url, self.parse, headers=cookie.headers)

    def parse(self, response):
        item = ArticleItem()
        sel = scrapy.Selector(response)

        catalog = ""
        title = join(sel.xpath("//h1[@class='art_tit']/text()").extract())
        source = "vgtime"
        art_url = ""  # 物理存放地址
        auther = join(sel.xpath("//div[@class='editor_name']/span[1]/text()").extract())
        create_time = time.altzone
        artTime = join(sel.xpath("//span[@class='time_box']/text()").extract())
        artFromUrl = response.url
        artImageUrl = ""  # 来list同级下的展示图片下载地址
        allhtml = response.body

        # content内容摘要信息
        isString = False
        isImage = False
        isVideo = False

        # 解析具体内容到 list中
        conList = []
        com = sel.xpath("//div[@class='topicContent front_content']/*")
        '''有序抓取'''
        for index, content in enumerate(com):  # 拿到所有内容
            # logger.info("spider!!!=" + content.extract() + index.__str__())

            pSel = "//div[@class='topicContent front_content']/p[" + (index + 1).__str__() + "]"
            imgMvSel = "//div[@class='topicContent front_content']/div[" + (
                index + 1).__str__() + "]/figure"  # 图片和视频，根据figure后的标签判断是图片还是视频
            pCon = sel.xpath(pSel)
            ivCon = sel.xpath(imgMvSel)
            # logger.info("spider!!!=" + ivCon.extract().__str__() + index.__str__())

            if len(pCon.extract()) > 0:  # 文字
                pText = pCon.xpath('string(.)').extract()
                conList.append(join(pText))
                isString = True
                # logger.info("text!!!=" + pText.__str__() + index.__str__())

            if len(ivCon.extract()) > 0:  # 图片和视频
                imgCon = ivCon.xpath("img")
                mvCon = ivCon.xpath("embed")
                mvCon_iframe = ivCon.xpath("iframe")
                if len(imgCon) > 0:  # 图片
                    imgUrl = imgCon.xpath("@src").extract()
                    imgWidth = imgCon.xpath("@style").re("[1-9]\d*")  # px
                    type = Constant.typeImg
                    imgObj = {"src": join(imgUrl), "width": join(imgWidth), "type": str(type)}
                    conList.append(imgObj)
                    isImage = True
                    # logger.info("image_!!!=" + imgObj.__str__())
                    if len(ivCon.xpath("figcation")) > 0:  # 图片下方介绍文字
                        imgDes = ivCon.xpath("figcation/text()").extract()
                        conList.append(join(imgDes))
                        logger.info("image_!!!=" + imgDes)
                elif len(mvCon.extract()) > 0:  # 视频
                    mvUrl = mvCon.xpath("@src").extract()
                    mvParams = mvCon.xpath("@flashvars").extract()
                    mvUrl.append(mvParams)  # 这里是 url+params拼接
                    mvWidth = mvCon.xpath("@width").extract()
                    mvHeight = mvCon.xpath("@height").extract()
                    type = Constant.typeVideo
                    mvObj = {"src": join(mvUrl), "type": str(type), "width": join(mvWidth), "height": join(mvHeight)}
                    conList.append(mvObj)
                    # logger.info("image_!!!=" + mvObj.__str__())
                elif len(mvCon_iframe.extract()) > 0:  # 视频-iframe
                    mvUrl = mvCon_iframe.xpath("@src").extract()
                    mvWidth = "-1"
                    mvHeight = "-1"
                    if len(mvCon_iframe.xpath("@width").extract()):
                        mvWidth = mvCon_iframe.xpath("@width").extract()
                    if len(mvCon_iframe.xpath("@height").extract()) > 0:
                        mvHeight = mvCon_iframe.xpath("@height").extract()
                    type = Constant.typeVideo
                    mvObj = {"src": join(mvUrl), "type": str(type), "width": join(mvWidth), "height": join(mvHeight)}
                    conList.append(mvObj)
                    isVideo = True
                    # logger.info("image_!!!=" + mvObj.__str__())

        # logger.info("spider!!!=" + conList.__str__())
        # logger.info("spider!!!=" + conList.__len__().__str__())

        # 构造返回item
        item['title'] = title
        item['auther'] = auther
        item['source'] = source
        item['catalog'] = catalog
        item['artUrl'] = art_url
        item['createTime'] = create_time
        item['artTime'] = artTime
        item['artFromUrl'] = artFromUrl
        item['artImageUrl'] = artImageUrl
        item['content'] = conList
        # item['xpathTag'] = allhtml
        item['isString'] = str(isString)
        item['isImage'] = str(isImage)
        item['isVideo'] = str(isVideo)

        yield item
