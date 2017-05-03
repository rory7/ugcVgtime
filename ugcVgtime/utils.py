# -*- coding: utf-8 -*-

import json

from requests.packages.urllib3 import request
from scrapy.utils import log


# # 没写完
# def dealReq(reqUrl, params):
#     r = request.Get(reqUrl, data=params)
#     log.logger.info("requestGet:" + r.url)


# 这里传入json文件路径。返回json字符串对象
def readJson(jsonFile):
    dicList = [json.loads(line) for line in open(jsonFile)]

    log.logger.info("jsonParser", dicList.__str__())
    # print dicList.__str__() + "/n"
    # print dicList[0]
    return dicList[0]


readJson("/Users/RoryHe/Desktop/ugcVgtime/spider.json")
