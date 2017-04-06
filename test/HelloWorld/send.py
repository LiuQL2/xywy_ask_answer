# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json.dumps({'name':'qianlong'}))

print ('[x] set hello world')
connection.close()

