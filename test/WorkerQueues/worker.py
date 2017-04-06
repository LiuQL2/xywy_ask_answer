#! /usr/bin/env python
# -*-coding:utf-8 -*-

import pika
import time
import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

#定义一个用来接收message的queue，同时为了保证消息不丢失，durable决定该queue进行持久化。
channel.queue_declare(queue='task_queue', durable=True)
print "[*] Waiting for messages. To exit press CTRL+C"


def callback(ch, method, properties, body):
    print "[x] Received %r" % body
    time.sleep(body.count(b'.'))
    print datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")," [x] Done"
    #每当这个任务完成之后，这个comsumer就会给RabbitMQ发送一个确认信息，确保这个任务不会因该
    #consumer的突然停止而丢失。
    ch.basic_ack(delivery_tag=method.delivery_tag)

#为了让各个worker均衡负载，将prefetch_count设为1。
channel.basic_qos(prefetch_count=1)#fair dispatch.
channel.basic_consume(callback, queue='task_queue')


channel.start_consuming()