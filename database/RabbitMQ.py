# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import traceback
import os
import time
import sys
sys.path.append(os.getcwd().replace("database",""))

from configuration.settings import RABBITMQ_CONNECTION_PARA as connection_parameter
from database.IOHandler import FileIO


class RabbitmqServer(object):
    def __init__(self):
        pass

    @staticmethod
    def get_connection(try_number=100):
        success = False
        for index in range(0, try_number, 1):
            print 'number', index
            try:
                connection = pika.BlockingConnection(connection_parameter)
                success = True
                return connection
            except Exception,e:
                print traceback.format_exc(), e.message
                FileIO.exceptionHandler(message=traceback.format_exc() + '  ' + e.message)
            if success == True:
                break
            else:
                pass
        if success == False:
            sys.exit(1)
        else:
            pass

    @staticmethod
    def add_message(message, routing_key, queue,queue_durable=False, exchange='',exchange_type=None,try_number=100):
        try:
            connection = RabbitmqServer.get_connection()
            channel = connection.channel()
            # 定义一个用来接收message的queue，同时为了保证消息不丢失，durable决定该queue进行持久化。
            channel.queue_declare(queue=queue, durable=queue_durable)
            # 定义一个exchange，用来传输message
            if exchange != '':
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
                channel.queue_bind(exchange=exchange, routing_key=routing_key, queue=queue)
                # 将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
                channel.basic_publish(exchange=exchange,
                                  routing_key=routing_key,
                                  body=message,
                                  properties=pika.BasicProperties(delivery_mode=2)
                                  # make the message persistent.
                                  )
                print "[x] Sent %r" % message
            else:
                # 将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
                channel.basic_publish(exchange=exchange,
                                  routing_key=queue,
                                  body=message,
                                  properties=pika.BasicProperties(delivery_mode=2)
                                  # make the message persistent.
                                  )
                print "[x] Sent %r" % message
            connection.close()
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)

    @staticmethod
    def queue_delete(queue):
        try:
            connection = RabbitmqServer.get_connection()
            channel = connection.channel()
            channel.queue_delete(queue=queue)
            connection.close()
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)


    @staticmethod
    def exchange_delete(exchange):
        try:
            connection = RabbitmqServer.get_connection()
            channel = connection.channel()
            channel.exchange_delete(exchange=exchange)
            connection.close()
        except Exception,e:
            print traceback.format_exc(),e.message
            FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)


class RabbitmqConsumer(object):
    def __init__(self, queue, queue_durable=False,try_number=100):
        self.queue=queue
        self.queue_durable = queue_durable
        success = False
        for index in range(0, try_number,1):
            try:
                self.connection = pika.BlockingConnection(connection_parameter)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=queue, durable=queue_durable)
                success = True
            except Exception, e:
                print traceback.format_exc(), e.message
                FileIO.exceptionHandler(message=traceback.format_exc() + ' ' + e.message)
            if success:
                break
            else:
                pass
        if success==False:
            sys.exit(1)
        else:
            pass


    def callback(self, ch, method, properties, body):
        print '[X] get url: %s' % body
        # 每当这个任务完成之后，这个comsumer就会给RabbitMQ发送一个确认信息，确保这个任务不会因该
        # consumer的突然停止而丢失。
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print 'sleeping...'
        time.sleep(5)

    def start_consuming(self):
        # 为了让各个worker均衡负载，将prefetch_count设为1。
        self.channel.basic_qos(prefetch_count=1)  # fair dispatch.
        # self.channel.basic_consume(self.callback, queue=self.queue)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self.channel.start_consuming()

if __name__ == "__main__":
    RabbitmqServer.queue_delete(queue='2013_day_url_queue')
    # RabbitmqServer.queue_delete(queue='post_url_queue')
    # RabbitmqServer.queue_delete(queue='pubmed_article_queue')

    # connection = RabbitmqServer.get_connection()
    # channel = connection.channel()
    # channel.queue_declare(queue="test", durable=False)
    # sys.path.append(os.getcwd())
    # print os.getcwd()