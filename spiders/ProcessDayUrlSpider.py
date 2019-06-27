# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
import json
import sys
import os
sys.path.append(os.getcwd().replace("spiders",""))

from spiders.BaseSpider import BaseSpider
from database.IOHandler import FileIO
from database.RabbitMQ import RabbitmqServer
from configuration.settings import DAY_URL_QUEUE_EXCHANGE as day_queue_exchange
from configuration.settings import PAGE_URL_QUEUE_EXCHANGE as page_queue_exchange
from configuration.settings import QUESTION_QUEUE_EXCHANGE as question_queue_exchange
from configuration.settings import URL_TRY_NUMBER as url_try_number


class ProcessDayUrl(BaseSpider):
    """
    用来处理某一天url的爬虫，主要是获得该日期下每一个页面的url，并将每一个页面的url保存到rabbitmq服务器中。
    """
    def __init__(self,url_count,use_proxy=False):
        self.url_count = url_count
        self.use_proxy = use_proxy
        self.selector = self.process_url_request(url=self.url_count['url'],xpath_type=True,whether_decode=True,
                                                 encode_type='GBK',use_proxy=use_proxy)
        try_number = int(self.url_count['try_number'])
        self.url_count['try_number'] = try_number + 1

    def parse(self):
        """
        处理某一天的url，这里将获取一天有多少页，并将这些页面的url保存到一个queue中，
        :return:
        """
        try:
            page_numer_content = self.selector.xpath('//div[@class="club_page"]/div/text()')[-1]
            mode = re.compile(r'\d+')
            page_numer = (mode.findall(page_numer_content)[0]).encode('utf-8')
            page_numer = int(page_numer)
            print(self.url_count['url'], type(page_numer), page_numer)
            url_preffix = self.url_count['url'][0:len(self.url_count['url']) - 6]
            # 成功获取页面数，将页面url保存到对应的queue中
            for number in range(1, page_numer + 1, 1):
                url = url_preffix + str(number) + '.html'
                print('page url:', url)
                url_count = {}
                url_count['url'] = url
                url_count['try_number'] = 0
                RabbitmqServer.add_message(message=json.dumps(url_count),
                                          routing_key=page_queue_exchange['routing_key'],
                                          queue=page_queue_exchange['queue'],
                                          queue_durable=page_queue_exchange['queue_durable'],
                                          exchange=page_queue_exchange['exchange'],
                                          exchange_type=page_queue_exchange['exchange_type'])
        except Exception as e:
            print(traceback.format_exc(),e.args[0], e.args[1])
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + str(e.args[0]) + str(e.args[1]))
            # 本次失败且尝试次数小于10次，将这一天的url重新放回保存日期url的queue中，等待下一次尝试。
            if self.url_count['try_number'] <= url_try_number:
                RabbitmqServer.add_message(message=json.dumps(self.url_count),
                                          routing_key=day_queue_exchange['routing_key'],
                                          queue=day_queue_exchange['queue'],
                                          queue_durable=day_queue_exchange['queue_durable'],
                                          exchange=day_queue_exchange['exchange'],
                                          exchange_type=day_queue_exchange['exchange_type']
                                           )
            else:
                pass




class GetOnePageQuestion(BaseSpider):
    """
    用来处理一个页面的url，这里一个页面有20个问题，将抓取到的问题保存到rabbitmq服务器中。
    对于每一个问题，这里抓取到的一个例子如下：

{
  "question_url": "http://club.xywy.com/htm/2/623.htm",
  "post_month": "2004-12",
  "question_title": "丙肝问题",
  "disease": "饮食营养",
  "question_body": "慢性丙肝可以治愈吗",
  "post_date": "2004-12-31",
  "disease_url": "http://club.xywy.com/small_347.htm"
}
    """
    def __init__(self,url_count,use_proxy=False):
        self.url_count = url_count
        self.selector = self.process_url_request(url=self.url_count['url'],xpath_type=True,whether_decode=True,
                                                 encode_type='GBK',use_proxy=use_proxy)
        try_number = int(self.url_count['try_number'])
        self.url_count['try_number'] = try_number + 1

    def parse(self):
        day_question_list = []
        try:
            question_content_list = self.selector.xpath('//div[@class="bc mt15 DiCeng"]/div[@class="club_dic"]')
            for question_content in question_content_list:
                question = {}
                try:
                    question['disease'] = question_content.xpath('h4/var/a/text()')[0]
                    question['disease_url'] = question_content.xpath('h4/var/a/@href')[0]
                except:
                    question['disease'] = ''
                    question['disease_url'] = ''

                try:
                    question['question_url'] = question_content.xpath('h4/em/a/@href')[0]
                    question['question_title'] = question_content.xpath('h4/em/a/text()')[0]
                except:
                    question['question_url'] = ''
                    question['question_title'] = ''

                try:
                    question['question_body'] = question_content.xpath('div/p/text()')[0]
                except:
                    question['question_body'] = ''
                post_date = self.url_count['url'].split('/')[4]
                question['post_date'] = post_date
                question['post_month'] = post_date[0:7]
                day_question_list.append(question)
                #将抓取的问题信息保存到对应的queue中。
                RabbitmqServer.add_message(message=json.dumps(question),
                                          routing_key=question_queue_exchange['routing_key'],
                                          queue=question_queue_exchange['queue'],
                                          queue_durable=question_queue_exchange['queue_durable'],
                                          exchange=question_queue_exchange['exchange'],
                                          exchange_type=question_queue_exchange['exchange_type'])
        except Exception as e:
            print(traceback.format_exc(),e.args[0], e.args[1])
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + str(e.args[0]) + str(e.args[1]))
            #本次尝试失败且尝试次数小于10次，将这个页面的url放回原来的queue中，待下一次尝试。
            if int(self.url_count['try_number']) <= url_try_number:
                RabbitmqServer.add_message(message=self.url_count,
                                          routing_key=page_queue_exchange['routing_key'],
                                          queue=page_queue_exchange['queue'],
                                          queue_durable=page_queue_exchange['queue_durable'],
                                          exchange=page_queue_exchange['exchange'],
                                          exchange_type=page_queue_exchange['exchange_type'])
            else:
                pass