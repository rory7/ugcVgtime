# -*- coding: utf-8 -*-
cookies = {}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.2063810249.1493779822; _gid=GA1.2.1317513627.1493806356; Hm_lvt_0efa32d5d3a6960eea5a730b9346ed44=1493779822,1493783496,1493805283; Hm_lpvt_0efa32d5d3a6960eea5a730b9346ed44=1493806356; JSESSIONID=B59AE9521ED0B474D7234DAFD141F3BA; _gat=1",
    "Host": "www.vgtime.com",
    "Referer": "http://new.vgtime.com/topic/index.jhtml",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}

meta = {
    'dont_redirect': True,  # 禁止网页重定向
    'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
}
