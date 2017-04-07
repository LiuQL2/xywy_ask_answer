# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import traceback
import sys

from configuration.settings import MASTER_INFO as master_info
from database.IOHandler import FileIO


class ServerHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def add_message(message, routing_key, queue,queue_durable=False, exchange='',exchange_type=None):
        try:
            url = 'amqp://' + master_info['user'] + ':' + master_info['password'] + '@' + master_info[
                'host'] + ':' + str(master_info['port'])
            connection = pika.BlockingConnection(pika.URLParameters(url=url))

            channel = connection.channel()
            # 定义一个用来接收message的queue，同时为了保证消息不丢失，durable决定该queue进行持久化。
            channel.queue_declare(queue=queue, durable=queue_durable)

            # 定义一个exchange，用来传输message
            if exchange != '':
                channel.exchange_declare(exchange=exchange, type=exchange_type)
                channel.queue_bind(exchange=exchange, routing_key=routing_key, queue=queue)
                # 将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
                channel.basic_publish(exchange=exchange,
                                      routing_key=routing_key,
                                      body=message,
                                      properties=pika.BasicProperties(delivery_mode=2)  # make the message persistent.
                                      )
                print "[x] Sent %r" % message
            else:
                # 将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
                channel.basic_publish(exchange=exchange,
                                      routing_key=queue,
                                      body=message,
                                      properties=pika.BasicProperties(delivery_mode=2)  # make the message persistent.
                                      )
                print "[x] Sent %r" % message
            connection.close()
        except Exception, e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message = traceback.format_exc() + ' ' + e.message)
            sys.exit('Rabbitmq Server Wrong.')
