# /usr/bin/env python
# -*-coding:utf-8 -*-


from pymongo import MongoClient
import datetime
import sys
import traceback
import json

from database.IOHandler import FileIO
from configuration.settings import MongoDB_INFO as mongoDB_info

reload(sys)
sys.setdefaultencoding("UTF-8")

class Statistics(object):
    def __init__(self,db, question_collection,department_collection):
        self.host = mongoDB_info['host']
        self.port = mongoDB_info['port']
        self.db = db
        self.question_collection = question_collection
        self.department_collection = department_collection

    def get_distinct_disease(self):
        client = MongoClient(self.host,self.port)
        db = client[self.db]
        question_collection = db[self.question_collection]
        department_collection = db[self.department_collection]
        disease_list = list(department_collection.distinct("disease_url"))
        temp_dict_list = []
        for disease in disease_list:
            temp = {}
            temp['disease_url'] = disease
            temp['disease_name'] = (question_collection.find_one({"disease_url":disease},{"disease":1}))['disease']
            temp_dict_list.append(temp)
        client.close()
        print temp_dict_list
        return temp_dict_list

    def get_distinct_department(self):
        client = MongoClient(self.host,self.port)
        db = client[self.db]
        department_collection = db[self.department_collection]
        department_list = list(department_collection.distinct("first_name"))
        temp_dict_list = []
        for department in department_list:
            temp = {}
            temp['department_name'] = department
            temp['department_url'] = (department_collection.find_one({"first_name":department},{"first_url":1}))['first_url']
            temp_dict_list.append(temp)
        client.close()
        print temp_dict_list
        return temp_dict_list

    def disease_count(self):
        client = MongoClient(self.host,self.port)
        db = client[self.db]
        question_collection = db[self.question_collection]
        disease_list = self.get_distinct_disease()
        index = 0
        for disease in disease_list:
            index = index + 1
            result = {}
            result['disease'] = disease
            pipeline = [
                {"$match":{"disease_url":disease['disease_url']}},
                {"$group":{"_id":"$post_month","count":{"$sum":1}}},
                {"$sort":{"_id":1}}]
            count_list = list(question_collection.aggregate(pipeline))
            temp = {}
            for count in count_list:
                temp[count['_id']] = count['count']
            result['count'] = temp
            if index == 1:
                line = disease.keys() + temp.keys()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/disease_count.csv')
                line = disease.values() + temp.values()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/disease_count.csv')
            else:
                line = disease.values() + temp.values()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/disease_count.csv')
            print index,result
            FileIO.writeToFile(text=json.dumps(result),filename='./../result/disease_count.json')
        client.close()

    def department_count(self):
        client = MongoClient(self.host,self.port)
        db = client[self.db]
        question_collection = db[self.question_collection]
        department_list = self.get_distinct_department()
        index = 0
        for department in department_list:
            index = index + 1
            result = {}
            result['department'] = department
            pipeline = [
                {"$match":{"department_url":department['department_url']}},
                {"$group":{"_id":"$post_month","count":{"$sum":1}}},
                {"$sort":{"_id":1}}]
            count_list = list(question_collection.aggregate(pipeline))
            temp = {}
            for count in count_list:
                temp[count['_id']] = count['count']
            result['count'] = temp
            print index,result
            if index == 1:
                line = department.keys() + temp.keys()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/department_count.csv')
                line = department.values() + temp.values()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/department_count.csv')
            else:
                line = department.values() + temp.values()
                FileIO.writeToCsvFile(list_msg=line,filename='./../result/department_count.csv')
            FileIO.writeToFile(text=json.dumps(result),filename='./../result/department_count.json')
        client.close()


if __name__ == '__main__':
    statistic = Statistics(db='xywy',question_collection='question_all',department_collection='department')
    statistic.disease_count()
    # statistic.department_count()