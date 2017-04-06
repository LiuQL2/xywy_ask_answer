#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

#定义一个exchange，并定义其类型为fanout：把message分发给指定给该exchange的所有queue。
channel.exchange_declare(exchange='logs', type='fanout')

#随机产生一个queue，并获取该queue的名字
#其中exclusive为True决定的是当这个consumer断开连接后，该queue也应该被删除
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

#把这个队列指定给这个exchange
channel.queue_bind(exchange='logs',queue=queue_name)

print "[*] Waiting for logs. To exit press CTR+C"

#获得消息后的函数
def callback(ch, method, properties, body):
    print " [x] %r" % body

#将该函数利用该channel进行访问服务器，并且当任务完成之后不给RabbitMQ返回确认信息。
channel.basic_consume(callback, queue=queue_name,no_ack=True)

channel.start_consuming()