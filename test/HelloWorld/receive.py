#/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672))
channel = connection.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print("[X] Received %s" % json.loads(body)['name'])


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()