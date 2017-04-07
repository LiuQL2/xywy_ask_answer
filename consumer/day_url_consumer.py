# /usr/bin/env python
# -*-coding:utf-8 -*-

import pika
import traceback
import sys

from configuration.settings import MASTER_INFO as master_info
from configuration.settings import DAY_URL_QUEUE_EXCHANGE as queue_exchange
from configuration.settings import USE_PROXY as use_proxy
from database.IOHandler import FileIO
from spiders.ProcessDayUrlSpider import ProcessDayUrl


class DayUrlConsumer(object):
    def __init__(self, routing_key, queue, queue_durable=False, exchange='',exchange_type=None):
        url = 'amqp://' + master_info['user'] + ':' + master_info['password'] + '@' + master_info['host'] + ':' + str(master_info['port'])
        self.queue=queue
        self.routing_key = routing_key
        self.exchange = exchange
        self.queue_durable = queue_durable
        self.exchange_type = exchange_type
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(url=url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue, durable=queue_durable)
            # 定义一个exchange，用来传输message
            if exchange != '':
                self.channel.exchange_declare(exchange=exchange,type=exchange_type)
                self.channel.queue_bind(exchange=exchange, routing_key=routing_key, queue=queue)
            else:
                pass
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)
            sys.exit(1)


    def callback(self, ch, method, properties, body):
        print '[X] get url: %s' % body
        process_day_url = ProcessDayUrl(url = body,use_proxy=use_proxy)
        process_day_url.parse()
        # 每当这个任务完成之后，这个comsumer就会给RabbitMQ发送一个确认信息，确保这个任务不会因该
        # consumer的突然停止而丢失。
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # 为了让各个worker均衡负载，将prefetch_count设为1。
        self.channel.basic_qos(prefetch_count=1)  # fair dispatch.
        self.channel.basic_consume(self.callback, queue=self.queue)
        self.channel.start_consuming()


if __name__ == '__main__':
    consumer = DayUrlConsumer(exchange=queue_exchange['exchange'],
                              routing_key=queue_exchange['routing_key'],
                              queue=queue_exchange['queue'],
                              exchange_type=queue_exchange['exchange_type'],
                              queue_durable=queue_exchange['queue_durable'])
    consumer.start_consuming()