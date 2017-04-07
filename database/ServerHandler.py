# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika

from configuration.settings import MASTER_INFO as master_info


class ServerHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def add_message(message, routing_key, queue,durable=False, exchange='',type=None):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=master_info['host'],
                                                                       port=master_info['port']))
        channel = connection.channel()
        # 定义一个用来接收message的queue，同时为了保证消息不丢失，durable决定该queue进行持久化。
        channel.queue_declare(queue=queue, durable=durable)

        # 定义一个exchange，用来传输message
        if exchange != '':
            channel.exchange_declare(exchange=exchange,type=type)
            channel.queue_bind(exchange=exchange, routing_key=routing_key, queue=queue)

        else:
            pass

        # 将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=message,
                              properties=pika.BasicProperties(delivery_mode=2)  # make the message persistent.
                              )
        print "[x] Sent %r" % message

        connection.close()