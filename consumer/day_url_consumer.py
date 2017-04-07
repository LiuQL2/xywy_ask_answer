# /usr/bin/env python
# -*-coding:utf-8 -*-

import pika

from configuration.settings import MASTER_INFO as master_info
from configuration.settings import DATA_YEAR as data_year


class DayUrlConsumer(object):
    def __init__(self, routing_key, queue, queue_durable=False, exchange='',exchange_type=None):
        self.queue=queue
        self.routing_key = routing_key
        self.exchange = exchange
        self.queue_durable = queue_durable
        self.exchange_type = exchange_type
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=master_info['host'],
                                                                            port=master_info['port']))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=queue_durable)
        # 定义一个exchange，用来传输message
        if exchange != '':
            self.channel.exchange_declare(exchange=exchange,type=exchange_type)
            self.channel.queue_bind(exchange=exchange, routing_key=routing_key, queue=queue)

        else:
            pass

    def callback(self, ch, method, properties, body):
        print '[X] get url: %s' % body
        # 每当这个任务完成之后，这个comsumer就会给RabbitMQ发送一个确认信息，确保这个任务不会因该
        # consumer的突然停止而丢失。
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # 为了让各个worker均衡负载，将prefetch_count设为1。
        self.channel.basic_qos(prefetch_count=1)  # fair dispatch.
        self.channel.basic_consume(self.callback, queue=self.queue, no_ack=True)
        self.channel.start_consuming()


if __name__ == '__main__':
    exchange = data_year + '_day_url_exchange'
    routing_key = data_year + '_day_url_routing_key'
    queue = data_year + '_day_url_queue'
    exchange_type = 'direct'
    queue_durable = False
    consumer = DayUrlConsumer(exchange=exchange, routing_key=routing_key,queue=queue,exchange_type=exchange_type,
                              queue_durable=queue_durable)
    consumer.start_consuming()