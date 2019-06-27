# /usr/bin/env python

import json
import sys
import os
sys.path.append(os.getcwd().replace("statistic",""))

from database.IOHandler import FileIO

month_list = [u'201601',u'201602',u'201603',u'201604',u'201605',u'201606',u'201607',u'201608',u'201609',u'201610',u'201611',u'201612',]



def load_line(record):
    count = record['count']
    for month in month_list:
        if month not in count.keys():
            count[month] = ''
        else:
            pass
    # line = record[u'department']['department_name'] + ','
    line = record[u'disease']['disease_name'] + ','
    for month in month_list:
        line = line + str(count[month]) + ','
    return line[0:len(line) - 1]

def load_file(filename):
    file = open(filename,'r')
    line = 'department,201601,201602,201603,201604,201605,201606,201607,201608,201609,201610,201611,201612'
    line = 'disease,201601,201602,201603,201604,201605,201606,201607,201608,201609,201610,201611,201612'
    # FileIO.writeToFile(text=line,filename='./../result/department_count_2.csv')
    FileIO.writeToFile(text=line, filename='./../result/disease_count_2.csv')
    for line in file:
        line = json.loads(line)
        print(type(line),line)
        line = load_line(line)
        FileIO.writeToFile(text=line,filename='./../result/disease_count_2.csv')
    file.close()

load_file('./../result/disease_count.json')