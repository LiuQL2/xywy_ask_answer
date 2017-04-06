# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json

from configuration.settings import PAGE_NUMBER as page_number
from configuration.settings import DATA_YEAR as data_year
from configuration.settings import MASTER_INFO as master_info
from spiders.get_day_url import GetDayUrl


class DayUrlProducer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=master_info['host'],
                                                                            port=master_info['port']))
        self.channel = self.connection.channel()
        self.exchange = data_year + '_day_url_exchange'
        self.routing_key = data_year + '_day_url_routing_key'
        self.queue = data_year + '_day_url_queue'

    def declare(self):
        self.channel.exchange_declare(exchange=self.exchange,type='direct')
        self.channel.queue_declare(queue=self.queue)

        pass

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
                    self.channel.basic_publish(exchange=self.exchange,
                                               routing_key=self.routing_key,
                                               body=day_url,
                                               properties=pika.BasicProperties(delivery_mode=2)
                                               )
                else:
                    pass
            if data_year + '-01-01' in url_list:
                break
            else:
                pass

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    producer = DayUrlProducer()
    producer.declare()
    producer.produce_day_url()
    producer.close()