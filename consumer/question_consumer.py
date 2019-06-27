# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd().replace("consumer",""))

from database.RabbitMQ import RabbitmqConsumer
from database.IOHandler import FileIO
from configuration.settings import QUESTION_SAVE_FILE as question_save_file
from configuration.settings import QUESTION_QUEUE_EXCHANGE as question_queue_exchange
from configuration.settings import DATA_YEAR as data_year


class QuestionConsumer(RabbitmqConsumer):
    """
    将抓取到并保存在rabbitmq服务器中的问题读取出来保存到磁盘文件中
    """
    def __init__(self,queue, queue_durable):
        super(QuestionConsumer,self).__init__(queue=queue,queue_durable=queue_durable)

    def callback(self,ch,method,properties, body):
        question_file = '/mnt/qianlong/data/xywy/' + data_year + "/" + question_save_file
        print(type(body), body)
        FileIO.writeToFile(text=body,filename=question_file)
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    consumer = QuestionConsumer(queue=question_queue_exchange['queue'],
                                queue_durable=question_queue_exchange['queue_durable'])
    consumer.start_consuming()