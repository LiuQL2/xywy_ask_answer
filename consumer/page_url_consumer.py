# /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
sys.path.append(os.getcwd().replace("consumer",""))

import datetime
import pika.exceptions

from database.RabbitMQ import RabbitmqConsumer
from spiders.ProcessDayUrlSpider import GetOnePageQuestion
from configuration.settings import USE_PROXY as use_proxy
from configuration.settings import PAGE_URL_QUEUE_EXCHANGE as page_queue_exchange
from configuration.settings import TIME_SLEEP as time_sleep


class PageUrlConsumer(RabbitmqConsumer):
    """
    将获得并保存在rabbitmq服务器中的每一个页面url取出来，进行获得该页面上的20个问题信息。
    """
    def __init__(self, queue, queue_durable=False):
        super(PageUrlConsumer, self).__init__(queue=queue,queue_durable=queue_durable)

    def callback(self, ch, method, properties, body):
        print('body',body)
        url_count = json.loads(body)
        get_one_page_question = GetOnePageQuestion(url_count=url_count,use_proxy=use_proxy)
        get_one_page_question.parse()#该方法将获得的20个问题信息保存到rabbitmq服务器上对应的queue中。
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('sleeping..',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.connection.sleep(time_sleep)


if __name__ == '__main__':
    consumer = PageUrlConsumer(
                              queue=page_queue_exchange['queue'],
                              queue_durable=page_queue_exchange['queue_durable']
                              )
    consumer.start_consuming()