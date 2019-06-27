# /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd().replace("spiders",""))

import traceback
from spiders.BaseSpider import BaseSpider
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
        except Exception as e:
            print(traceback.format_exc(),e.args[0], e.args[1])
            FileIO.exceptionHandler(message=traceback.format_exc() + '   ' + str(e.args[0]) + str(e.args[1]))
            return None