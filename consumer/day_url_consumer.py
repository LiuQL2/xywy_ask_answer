# /usr/bin/env python
# -*-coding:utf-8 -*-

import sys
import os
import json
sys.path.append(os.getcwd().replace("consumer",""))

from configuration.settings import DAY_URL_QUEUE_EXCHANGE as day_url_queue_exchange
from configuration.settings import USE_PROXY as use_proxy
from configuration.settings import TIME_SLEEP as time_sleep
from database.RabbitMQ import RabbitmqConsumer
from spiders.ProcessDayUrlSpider import ProcessDayUrl


class DayUrlConsumer(RabbitmqConsumer):
    """
    将rabbitmq服务器中日期的url读取出来进行下一步处理
    """
    def __init__(self, queue, queue_durable=False):
        super(DayUrlConsumer, self).__init__(queue=queue, queue_durable=queue_durable)

    def callback(self, ch, method, properties, body):
        print '[X] get url: %s' % body
        url_count = json.loads(body)
        #将该日期的url读取出来，获得该日期下所有页面的url，一个页面包含20个问题。
        process_day_url = ProcessDayUrl(url_count = url_count,use_proxy=use_proxy)
        process_day_url.parse()#该方法将获得页面url保存到rabbitmq服务器对应的队列中。
        # 每当这个任务完成之后，这个comsumer就会给RabbitMQ发送一个确认信息，确保这个任务不会因该
        # consumer的突然停止而丢失。
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print 'sleeping...'
        self.connection.sleep(time_sleep)


if __name__ == '__main__':
    consumer = DayUrlConsumer(
                              queue=day_url_queue_exchange['queue'],
                              queue_durable=day_url_queue_exchange['queue_durable'])
    consumer.start_consuming()