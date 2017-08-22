# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import os
import sys
sys.path.append(os.getcwd().replace("producer",""))

from configuration.settings import PAGE_NUMBER as page_number
from configuration.settings import DATA_YEAR as data_year
from configuration.settings import USE_PROXY as use_proxy
from configuration.settings import DAY_URL_QUEUE_EXCHANGE as day_queue_exchange
from spiders.GetDayUrlSpider import GetDayUrl
from database.RabbitMQ import RabbitmqServer


class DayUrlProducer(object):
    """
    获得每一个日期的url，并将获得日期url保存到rabbitma服务器对应的queue中。
    """
    def __init__(self, routing_key, queue, queue_durable=False, exchange='',exchange_type=None):
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue = queue
        self.queue_durable = queue_durable
        self.exchange_type = exchange_type

    def produce_day_url(self):
        url_list = []
        for number in range(1, page_number + 1, 1):
            url = 'http://club.xywy.com/keshi/' + str(number) + '.html'
            get_day_url = GetDayUrl(url = url,use_proxy=use_proxy)
            temp_url_list = get_day_url.parse()
            for day_url in temp_url_list:
                if data_year in day_url:
                    url_list.append(day_url)
                    print day_url
                    url_count = {}
                    url_count['url'] = day_url
                    url_count['try_number'] = 0
                    RabbitmqServer.add_message(message=json.dumps(url_count),
                                              routing_key=self.routing_key,
                                              queue=self.queue,
                                              queue_durable=self.queue_durable,
                                              exchange=self.exchange,
                                              exchange_type=self.exchange_type)
                else:
                    pass
            first_day_url = 'http://club.xywy.com/keshi/' + data_year + '-01-01/1' + '.html'
            print first_day_url
            if first_day_url in url_list:
                break
            else:
                pass


if __name__ == '__main__':
    producer = DayUrlProducer(exchange=day_queue_exchange['exchange'],
                              routing_key=day_queue_exchange['routing_key'],
                              queue=day_queue_exchange['queue'],
                              exchange_type=day_queue_exchange['exchange_type'],
                              queue_durable=day_queue_exchange['queue_durable'])
    producer.produce_day_url()
