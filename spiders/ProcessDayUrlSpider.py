# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
import json

from BaseSpider import BaseSpider
from database.IOHandler import FileIO
from database.RabbitMQ import RabbitmqServer
from configuration.settings import DAY_URL_QUEUE_EXCHANGE as day_queue_exchange
from configuration.settings import PAGE_URL_QUEUE_EXCHANGE as page_queue_exchange
from configuration.settings import QUESTION_URL_QUEUE_EXCHANGE as question_queue_exchange


class ProcessDayUrl(BaseSpider):
    """
    用来处理某一天url的爬虫，主要是获得该日期下每一个页面的url，并将每一个页面的url保存到rabbitmq服务器中。
    """
    def __init__(self,url,use_proxy=False):
        self.url = url
        self.use_proxy = use_proxy
        self.selector = self.process_url_request(url=self.url,xpath_type=True,whether_decode=True,
                                                 encode_type='GBK',use_proxy=use_proxy)

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
            print self.url, type(page_numer), page_numer
            url_preffix = self.url[0:len(self.url) - 6]
            # 成功获取页面数，将页面url保存到对应的queue中
            for number in range(1, page_numer + 1, 1):
                url = url_preffix + str(number) + '.html'
                print 'page url:', url
                RabbitmqServer.add_message(message=url,
                                          routing_key=page_queue_exchange['routing_key'],
                                          queue=page_queue_exchange['queue'],
                                          queue_durable=page_queue_exchange['queue_durable'],
                                          exchange=page_queue_exchange['exchange'],
                                          exchange_type=page_queue_exchange['exchange_type'])
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)
            # 本次失败，将这一天的url重新放回保存日期url的queue中，等待下一次尝试。
            RabbitmqServer.add_message(message=self.url,
                                      routing_key=day_queue_exchange['routing_key'],
                                      queue=day_queue_exchange['queue'],
                                      queue_durable=day_queue_exchange['queue_durable'],
                                      exchange=day_queue_exchange['exchange'],
                                      exchange_type=day_queue_exchange['exchange_type']
                                       )




class GetOnePageQuestion(BaseSpider):
    """
    用来处理一个页面的url，这里一个页面有20个问题，将抓取到的问题保存到rabbitmq服务器中。
    """
    def __init__(self,url,use_proxy=False):
        self.url = url
        self.selector = self.process_url_request(url=self.url,xpath_type=True,whether_decode=True,
                                                 encode_type='GBK',use_proxy=use_proxy)

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
                post_date = self.url.split('/')[4]
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
        except Exception, e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)
            #本次尝试失败，将这个页面的url放回原来的queue中，待下一次尝试。
            RabbitmqServer.add_message(message=self.url,
                                      routing_key=page_queue_exchange['routing_key'],
                                      queue=page_queue_exchange['queue'],
                                      queue_durable=page_queue_exchange['queue_durable'],
                                      exchange=page_queue_exchange['exchange'],
                                      exchange_type=page_queue_exchange['exchange_type'])