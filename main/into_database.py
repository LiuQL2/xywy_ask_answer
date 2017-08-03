# /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.getcwd().replace("main",""))

from database.MysqlDatabaseClass import MySQLDatabaseClass



def into_database(file_name):
    data_file = open(file_name,'r')
    file_name = file_name.split('/')[-1]
    mysql = MySQLDatabaseClass()
    index = 0
    number = 0
    for line in data_file:
        record = json.loads(line)
        record['file_name'] = file_name
        print file_name,number, record
        mysql.insert(table='question',record=record)
        index = index + 1
        number = number + 1
        if index > 100000:
            mysql.close()
            mysql = MySQLDatabaseClass()
            index = 0
        else:
            pass
    data_file.close()

if __name__ == '__main__':
    path = './../result/'
    file_list = os.listdir(path)
    print file_list
    for file_name in file_list:
        into_database(path + file_name)