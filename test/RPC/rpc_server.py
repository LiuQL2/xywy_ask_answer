#! /usr/bin/env python
# -*-coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

#定义一个queue，用来存储request请求，且该queue不进行持久化。
channel.queue_declare(queue='rpc_queue')

#计算斐波那契数列的函数
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)

    print "[.] fib(%s)" % n
    response = fib(n)

    #将计算得到的斐波那契结果publish到rabbitMQ中
    ch.basic_publish(exchange='',
                     routing_key = props.reply_to,
                     properties = pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request,queue='rpc_queue')

print "[x] Awaiting RPC requests"
channel.start_consuming()