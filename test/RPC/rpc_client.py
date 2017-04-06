#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            port=5672,
        ))
        self.channel = self.connection.channel()

        #生成一个queue，并随机命名。用来存储返回的结果。
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        #用来从返回队列中取回返回结果
        self.channel.basic_consume(self.on_response,no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """
        如果返回的correlation_id与一个request的id相同，说明这个结果是对应request的。
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            self.response = body
        else:
            pass

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print "[x] Resquesting fib(30)"
response = fibonacci_rpc.call(20)
print "[.] Got %r" % response