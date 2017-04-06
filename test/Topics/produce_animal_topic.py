#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
channel = connection.channel()

channel.exchange_declare(exchange='animal_topic',type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else '<celerity>.<colour>.<species>'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='animal_topic',
                      routing_key=routing_key,
                      body=message)
print "[x] Sent %r:%r" % (routing_key,message)
connection.close()