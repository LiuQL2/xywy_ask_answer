# /usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import traceback
import json

from database.RabbitMQ import RabbitmqServer
from configuration.settings import DISEASE_URL_QUEUE_EXCHANGE as disease_url_queue_exchange

client = MongoClient('localhost', 27017)
db = client.xywy
collection = db.question1
url_list = collection.distinct("disease_url")
print len(url_list), url_list
for url in url_list:
    if url != u'':
        print '****', url
        RabbitmqServer.add_message(message=url,
                                   routing_key=disease_url_queue_exchange['routing_key'],
                                   queue=disease_url_queue_exchange['queue'],
                                   queue_durable=disease_url_queue_exchange['queue_durable'],
                                   exchange=disease_url_queue_exchange['exchange'],
                                   exchange_type=disease_url_queue_exchange['exchange_type'])
client.close()