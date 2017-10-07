# /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import json

from configuration.settings import DETAIL_DISEASE_URL as detail_disease_url
from configuration.settings import DETAIL_QUESTION_URL_QUEUE_EXCHANGE as question_url_queue_exchagne
from configuration.settings import DETAIL_YEAR_DIR as data_dir
from database.RabbitMQ import RabbitmqServer
from utilities import get_dirlist

sys.path.append(os.getcwd().replace("consumer",""))


class DetailQuestionURLProducer(object):
    """
    从已经得到的简要问题文件中筛选出需要详细信息的问题URL，并将URL保存到RabbitMQ中。
    """
    def __init__(self):
        self.file_name_list = get_dirlist(path=data_dir,key_word_list=["question",".json"],no_key_word_list=["sample_data"])
        # self.file_name_list = get_dirlist(path=data_dir,key_word_list=["question_"])
        print self.file_name_list

    def produce(self):
        for file_name in self.file_name_list:
            data_file = open(data_dir + file_name,mode="r")
            for line in data_file:
                question = json.loads(line)
                if question["disease_url"] in detail_disease_url:
                    RabbitmqServer.add_message(message=line,
                                               routing_key=question_url_queue_exchagne["routing_key"],
                                               queue=question_url_queue_exchagne["queue"],
                                               queue_durable=question_url_queue_exchagne["queue_durable"],
                                               exchange=question_url_queue_exchagne["exchange"],
                                               exchange_type=question_url_queue_exchagne["exchange_type"]
                                               )
                else:
                    pass
            data_file.close()


if __name__ == "__main__":
    producer = DetailQuestionURLProducer()
    producer.produce()