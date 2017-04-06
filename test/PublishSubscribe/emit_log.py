#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672 ))
channel = connection.channel()

#定义一个exchange，并定义其类型为fanout：把message分发给指定给该exchange的所有queue。
channel.exchange_declare(exchange='logs',type='fanout')

#定义传送的消息
message = ' '.join(sys.argv[1:]) or 'info: Hello World!'

#因为这个exchange要将一个message发送给多个queue，所以这里不指定queue的名称。
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print "[x] Sent %r" % message
connection.close()