# -*- coding: utf-8 -*-
import argparse

from scrapy.crawler import CrawlerProcess

# 执行一个spider脚本
from ugcVgtime.spiders import ugcArtSpider

'注意SpiderName必须是一个元组'


def runSpider(spiderName, userAgent):
    process = CrawlerProcess({'USER_AGENT': userAgent})

    for i in spiderName:
        process.crawl(i)
    process.start()


def runSingleSpider(spider, UA):
    process = CrawlerProcess({'USER_AGENT': UA})
    process.crawl(spider)
    process.start()

# parser = argparse.ArgumentParser(description='Running multiple spiders in the same process.')
# args = parser.parse_args()
# if args.crawler:
#     for each_crawler in args.crawler:
#         runSpider(each_crawler, "")
# pass

# runSingleSpider("ugcArtSpider", "")
