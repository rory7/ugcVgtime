# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

'''vgtime-tiopic条目数据'''


class UgcvgtimeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image = scrapy.Field()  # 条目展示图片地址
    url = scrapy.Field()  # 条目跳转链接
    title = scrapy.Field()  # 条目标题


'''vgtime-topic文章详情'''


class ArticleItem(Item):
    # info
    title = Field()
    auther = Field()
    source = Field()
    catalog = Field()
    artUrl = Field()
    createTime = Field()
    artTime = Field()
    artFromUrl = Field()
    artImageUrl = Field()
    # content list ->conList
    content = Field()
    # html tags
    xpathTag = Field()  # 抓取页面的html

    # content内容摘要信息
    isString = Field()
    isImage = Field()
    isVideo = Field()
