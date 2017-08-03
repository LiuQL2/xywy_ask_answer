# /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd().replace("spiders",""))

import traceback
import json
from pymongo import MongoClient
from BaseSpider import BaseSpider
from database.IOHandler import FileIO


class FirstDepartment(BaseSpider):
    def __init__(self,url,use_proxy=True):
        self.url = url
        self.use_proxy = use_proxy

    def parse(self):
        first = {}
        first['disease_url'] = self.url
        try:
            selector = self.process_url_request(url=self.url, xpath_type=True, whether_decode=True, encode_type="GBK",
                                                use_proxy=self.use_proxy)
            try:
                first['first_name'] = selector.xpath('//p[@class="pt5 pb5 lh180 f12 blue-a"]/a[3]/text()')[0]
                first['first_url'] = 'http://club.xywy.com' + selector.xpath('//p[@class="pt5 pb5 lh180 f12 blue-a"]/a[3]/@href')[0]
            except:
                first['first_name'] = selector.xpath('//li[@class="hd_family on"]/a/text()')[0]
                first['first_url'] = selector.xpath('//li[@class="hd_family on"]/a/@href')[0]
        except:
            first['first_name'] = ''
            first['first_url'] = ''
        return first

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.xywy
    collection = db.question1
    url_list = collection.distinct("disease_url")
    for url in url_list:
        if url != u'':
            spider = FirstDepartment(url=url)
            first = spider.parse()
            print '**',first
            FileIO.writeToFile(text=json.dumps(first),filename='./../result/first_department.json')
    client.close()