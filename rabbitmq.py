# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika

from configuration.settings import MASTER_INFO as master_info

url = 'amqp://' + master_info['user'] + ':' + master_info['password'] + '@' + master_info['host'] + ':' + str(
    master_info['port'])
connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()
# channel.queue_delete(queue='2016_day_url_queue')
channel.queue_delete(queue='2016_page_url_routing_key')
connection.close()