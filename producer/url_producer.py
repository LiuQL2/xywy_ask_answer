# /usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json

from configuration.settings import PAGE_NUMBER as page_number
from configuration.settings import DATA_YEAR as data_year
from configuration.settings import MASTER_INFO as master_info


class DayUrlProducer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=master_info['host'],
                                                                            port=master_info['port']))
        self.channel = self.connection.channel()

    def declare(self):
        pass

    def close(self):
        self.connection.close()