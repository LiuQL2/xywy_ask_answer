# /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import datetime
sys.path.append(os.getcwd().replace("consumer",""))

from database.RabbitMQ import RabbitmqConsumer
from database.RabbitMQ import RabbitmqServer
from configuration.settings import DETAIL_QUESTION_URL_QUEUE_EXCHANGE as question_url_queue_exchange
from configuration.settings import DETAIL_QUESTION_QUEUE_EXCHANGE as question_queue_exchange
from configuration.settings import USE_PROXY as use_proxy
from configuration.settings import TIME_SLEEP as time_sleep
from spiders.GetDetailQuestionSpider import DetailQuestionSpider


class DetailQuestionUrlConsumer(RabbitmqConsumer):
    """
    将获得并保存在rabbitmq服务器中的每一个页面url取出来，进行获得该页面上的20个问题信息。
    """
    def __init__(self, queue, queue_durable=False):
        super(DetailQuestionUrlConsumer, self).__init__(queue=queue,queue_durable=queue_durable)

    def callback(self, ch, method, properties, body):
        # print body
        question = json.loads(body)
        detail_question_spider = DetailQuestionSpider(url=question['question_url'],use_proxy=use_proxy)
        question = detail_question_spider.parse(question=question)#该方法将获得的20个问题信息保存到rabbitmq服务器上对应的queue中。

        # 将question的详细信息保存到RabbitMQ中
        if question is None:
            pass
        else:
            RabbitmqServer.add_message(message=json.dumps(question),
                                   routing_key=question_queue_exchange['routing_key'],
                                   queue=question_queue_exchange['queue'],
                                   queue_durable=question_queue_exchange['queue_durable'],
                                   exchange=question_queue_exchange['exchange'],
                                   exchange_type=question_queue_exchange['exchange_type'])

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('sleeping..',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.connection.sleep(time_sleep)


if __name__ == "__main__":
    consumer = DetailQuestionUrlConsumer(queue=question_url_queue_exchange['queue'],
                                         queue_durable=question_url_queue_exchange['queue_durable'])
    consumer.start_consuming()
