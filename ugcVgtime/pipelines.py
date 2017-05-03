# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

import time

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import run

reload(sys)
sys.setdefaultencoding('utf-8')

import json
from string import join

from scrapy.log import logger

from ugcVgtime.items import UgcvgtimeItem, ArticleItem
from ugcVgtime.spiders import Constant


class MainPipelines(object):
    def process_item(self, item, spider):
        if isinstance(item, UgcvgtimeItem):
            # 处理topic条目数据
            self.parse_topicItem(item, spider)
        elif isinstance(item, ArticleItem):
            # 处理topic文章详情数据
            self.parse_artclieItem(item, spider)

        return item

    def parse_topicItem(self, item, spider):
        topicList = []

        images = item['image']
        urls = item['url']
        titles = item['title']
        for index in range(len(images)):
            image = images[index]
            url = urls[index]
            title = titles[index]
            topicItem = {'title': title, 'image': image, 'url': url}
            topicList.append(topicItem)

        jsonOutPut = json.dumps(topicList, ensure_ascii=True, encoding='utf-8')
        fileName = "vgtime-topic/" + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".json"
        filePath = Constant.jsonOutPath + "/" + fileName
        jsonFile = open(filePath, 'wb')
        jsonOutPut.replace(" ", "")
        jsonFile.write(jsonOutPut.__str__())
        jsonFile.close()
        # 连接下一个文章详情爬虫启动,通过json数据指定所有的startUrls
        Constant.ugcUrlJsonFile = filePath
        process = CrawlerProcess(get_project_settings())
        process.crawl('ugcArtSpider')
        process.start()

    def parse_artclieItem(self, item, spider):
        article = dict()
        title = join(item['title']).replace(" ", "")
        auther = join(item['auther']).replace(" ", "")
        source = join(item['source']).replace(" ", "")
        catalog = join(item['catalog']).replace(" ", "")
        art_url = join(item['artUrl']).replace(" ", "")
        create_time = item['createTime']
        artTime = join(item['artTime']).replace(" ", "")
        artFromUrl = join(item['artFromUrl']).replace(" ", "")
        artImageUrl = join(item['artImageUrl']).replace(" ", "")
        conList = item['content']
        # allhtml = join(item['xpathTag'])

        # artInfo头部文章标识信息
        article['artInfo'] = {'catalog': catalog, 'title': title, 'source': source, 'art_url': art_url,
                              'auther': auther, 'create_time，': create_time, 'artTime': artTime,
                              'artFromUrl': artFromUrl, 'artImageUrl': artImageUrl}

        # artTypeInfo 文章内容成分
        isString = item['isString']
        isImage = item['isImage']
        isVideo = item['isVideo']

        article['artTypeInfo'] = {'isString': isString, 'isImage': isImage, 'isVideo': isVideo}

        # artContent 文章具体内容list
        article['artContent'] = {'content': conList}

        logger.info(
            "pipelines->parse_artclieItem=" + article.__str__() + "\n itemlen=" + article.__len__().__str__())

        print "pipelines->parse_artclieItem=" + article.__str__() + "\n itemlen=" + article.__len__().__str__()

        jsonOutPut = json.dumps(article, ensure_ascii=True, encoding='utf-8')

        logger.info(
            "pipelines->parse_artclieItem=" + jsonOutPut + "\n itemlen=" + article.__len__().__str__())

        # 输出路径 指定目录下->json文件
        fileName = "vgtime/" + title + ".json"
        filePath = Constant.jsonOutPath + "/" + fileName
        jsonFile = open(filePath, 'wb')
        jsonOutPut.replace(" ", "")
        jsonFile.write(jsonOutPut.__str__())
        jsonFile.close()

        # allhtml单独成立一个文件存储
        # unicode(allhtml, errors='ignore')
        # htmlFile = open(Constant.jsonOutPath + "/vgtime/" + title + ".html", 'wb')
        # htmlFile.write(allhtml)
        # htmlFile.close()
