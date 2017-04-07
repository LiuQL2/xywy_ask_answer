# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json

from configuration.settings import PAGE_NUMBER as page_number
from configuration.settings import DATA_YEAR as data_year
from spiders.get_day_url import GetDayUrl
from database.ServerHandler import ServerHandler


class DayUrlProducer(object):
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
            get_day_url = GetDayUrl(url = url,use_proxy=True)
            temp_url_list = get_day_url.parse()
            for day_url in temp_url_list:
                if data_year in day_url:
                    url_list.append(day_url)
                    print day_url
                    ServerHandler.add_message(message=day_url,
                                              routing_key=self.routing_key,
                                              queue=self.queue,
                                              durable=self.queue_durable,
                                              exchange=self.exchange,
                                              type=self.exchange_type)
                else:
                    pass
            first_day_url = 'http://club.xywy.com/keshi/' + data_year + '-01-01/1' + '.html'
            print first_day_url
            if first_day_url in url_list:
                break
            else:
                pass


if __name__ == '__main__':
    exchange = data_year + '_day_url_exchange'
    routing_key = data_year + '_day_url_routing_key'
    queue = data_year + '_day_url_queue'
    exchange_type = 'direct'
    queue_durable = False
    producer = DayUrlProducer(exchange=exchange, routing_key=routing_key,queue=queue,exchange_type=exchange_type,queue_durable=queue_durable)
    producer.produce_day_url()
