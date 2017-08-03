# /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd().replace("spiders",""))

import traceback
from BaseSpider import BaseSpider
from database.IOHandler import FileIO

class GetDayUrl(BaseSpider):
    def __init__(self,url,use_proxy=False):
        self.url = url
        self.selector = self.process_url_request(url=url,xpath_type=True,whether_decode=True,encode_type='GBK',
                                                 use_proxy=use_proxy)

    def parse(self):
        try:
            day_url = self.selector.xpath('//ul[@class="club_Date clearfix"]/li/a/@href')
            return day_url
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + '   ' + e.message)
            return None