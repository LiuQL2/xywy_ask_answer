#! /usr/bin/env python
# -*-coding:utf-8 -*-

import pika
import sys
import datetime

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
connection = pika.BlockingConnection(pika.URLParameters('amqp://longer:longer@127.0.0.1:5672'))
channel = connection.channel()

#定义一个用来接收message的queue，同时为了保证消息不丢失，durable决定该queue进行持久化。
channel.queue_declare(queue='task_queue', durable=True)


message = ' '.join(sys.argv[1:]) or "Hello World!"
#将message任务发送到服务器，同时为了保证每一个在做的message任务不丢失，delivery_mode参数决定将消息进行持久化。
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2)#make the message persistent.
                      )
print "[x] Sent %r" % message

connection.close()